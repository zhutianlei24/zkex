import pickledb
from web3 import Account
from zklink_sdk import EthereumSignerWeb3
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Token, Withdraw
from datetime import datetime
import requests
import json

private_key = pickledb.load('key.db', False).get("private_key")

account = Account.from_key(private_key)
ethereum_signer = EthereumSignerWeb3(account=account)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

# 这里涉及到token融合概念
# Token融合分为两种情况:
# 1. Merge -> 即不同链的同一种token，到达2层链后会merge，表现为使用同一种tokenid
# 2. Mapping -> 即一种token到达二层后会被映射到另一种token上面去。 例如不同的usd类的token可以映射到同一种token，目前只有usdc映射到了 usd。为此tokenid中的1-17号被预留给mapping功能
# 本例中提取的token为wETH不存在映射关系，所以不管在l1还是l2使用的都是同一个tokenid
l1_target_token = Token(id=141, chain_id=4, address='', symbol='', decimals=18)
l2_source_token = Token(id=141, chain_id=0, address='', symbol='', decimals=18)

## Load the account id from database
account_id = int(pickledb.load('account.db', False).get("l2userId"))
## Load the address from database
address = pickledb.load('account.db', False).get("address")

# Load the jwt for making request
jwt = pickledb.load('jwt.db', False).get("jwt")
# So here we need to attach the jwt token which we obtained from step 5 to the request headers,
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Access-Token": jwt  
}
# Requests the subnonce
response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/layer2/users/subNonce",
    headers = headers
)
subnonce = int(json.loads(response.text).get("subNonce"))

# get the current timestamp
timestamp = int(datetime.now().timestamp())

zk_data = Withdraw(
    to_chain_id = 4, #goerli在zklink上的chain id，具体可用4-get-supported-chains.py查询
    account_id = account_id,
    sub_account_id = 1,
    to_address = address,
    l2_source_token = l2_source_token,
    l1_target_token = l1_target_token,
    amount = 10000000000000000,
    fee = 3000000000000000,
    nonce = subnonce,
    fast_withdraw = 1,
    withdraw_fee_ratio = 10000,
    timestamp = timestamp
)

zk_signature = zksigner.sign_tx(zk_data).signature
print("the zk signature is:")
print(zk_signature)
print("the pubkey hex is:")
print(pubkey_hex)

eth_data = "Withdraw 0.01 wETH to: " + address.lower() + "\nFee: 0.003 wETH\nNonce: " + str(subnonce)

eth_signature = ethereum_signer.sign(eth_data.encode()).signature
print("the eth signature is:")
print(eth_signature)

# Construct the request body to submitter
payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "sendTransaction",
    "params": [
        {
             "type": "Withdraw",
             "toChainId": 4,
             "accountId": account_id,
             "subAccountId": 1,
             "to": address,
             "l2SourceToken": 141,
             "l1TargetToken": 141,
             "amount": "10000000000000000",
             "fee": "3000000000000000",
             "withdrawFeeRatio": 10000,
             "fastWithdraw": 1,
             "ts": timestamp,
             "nonce": subnonce,
             "signature": {
                 "pubKey": pubkey_hex,
                 "signature": zk_signature
             }
        },
        {
            "type": "EthereumSignature",
            "signature": eth_signature
        }
    ]
}
print(payload)
# Send the request
response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/layer2/repeater",
    data = json.dumps(payload),
    headers = headers
)

resultTx = json.loads(response.text).get("result")
print("Your withdraw request with amount 0.01 wETH has been made")
print("See more detail from: https://test-scan.zk.link/tx/"+ resultTx)

