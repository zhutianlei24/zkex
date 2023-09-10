import pickledb
from web3 import Account
from zklink_sdk import EthereumSignerWeb3
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Token, Transfer
from datetime import datetime
import requests
import json

## Load the private key from database
private_key = pickledb.load('key.db', False).get("private_key")

## Generate account, eth signer, zk signer and public key hex string
account = Account.from_key(private_key)
ethereum_signer = EthereumSignerWeb3(account=account)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

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

# we want to transfer wETH
t = Token(id=141, chain_id=0, address='', symbol='', decimals=18)

# Construct the to be signed transaction body
zk_data = Transfer(
  account_id = account_id,
  from_sub_account_id = 1, # hard coded as always the first sub account
  to_address = "0xdf705349D44903d7932026811Af8F256c2453228", # just an example here, also hard coded
  to_sub_account_id = 1, # hard coded as always the first sub account
  token = t,
  amount = 10000000000000000, # we want to transfer 0.01 wETH
  fee = 3000000000000000, # hard coded
  nonce = subnonce,
  timestamp = timestamp
)
zk_signature = zksigner.sign_tx(zk_data).signature
print("the zk signature is:")
print(zk_signature)
print("the pubkey hex is:")
print(pubkey_hex)

eth_data = "Transfer 0.01 wETH to: 0xdf705349d44903d7932026811af8f256c2453228\nFee: 0.003 wETH\nNonce: " + str(subnonce)
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
             "accountId": account_id,
             "fromSubAccountId": 1,
             "toSubAccountId": 1,
             "from": address,
             "to": "0xdf705349D44903d7932026811Af8F256c2453228",
             "tokenId": 141,
             "amount": "10000000000000000",
             "fee": "3000000000000000",
             "nonce": subnonce,
             "ts": timestamp,
             "type": "Transfer",
             "token": 141,
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
print("Your transfer request to 0xdf705349D44903d7932026811Af8F256c2453228 with amount 0.01 wETH has been made")
print("See more detail from: https://test-scan.zk.link/tx/"+ resultTx)
