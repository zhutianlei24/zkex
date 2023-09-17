import pickledb
from web3 import Account
from zklink_sdk import EthereumSignerWeb3
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Token, Order, OrderMatching
import requests
import json

# Load the private keys from database
private_key_taker = pickledb.load('key.db', False).get("private_key")
private_key_maker = pickledb.load('key.db', False).get("private_key_submitter")

# Hard coded as wETH-USD flash order
base_token=Token(id=141, chain_id=0, address='', symbol='', decimals=18)
quote_token=Token(id=1, chain_id=0, address='', symbol='', decimals=18)

# Init taker signer
account_taker = Account.from_key(private_key_taker)
zksigner_taker = ZkLinkSigner.from_account(account_taker, ZkLinkLibrary())
ethereum_signer_taker = EthereumSignerWeb3(account=account_taker)
pubkey_hex_taker = zksigner_taker.public_key.hex()
address_taker = ethereum_signer_taker.address()

# Init taker maker
account_maker = Account.from_key(private_key_maker)
zksigner_maker = ZkLinkSigner.from_account(account_maker, ZkLinkLibrary())
ethereum_signer_maker = EthereumSignerWeb3(account=account_maker)
pubkey_hex_maker = zksigner_maker.public_key.hex()
address_maker = ethereum_signer_maker.address()

# Perform two times login in order to get two different jwts
params = {}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "content-type": "application/json"
}
msg = "Access Login"

# Perform the first request to get the jwt of taker
signature_taker = ethereum_signer_taker.sign(msg.encode()).signature
body = {
  "verifyType": 0,
  "address": address_taker,
  "message": "Access Login",
  "signature": signature_taker
}
response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/users",
    params = params, 
    data = json.dumps(body),
    headers = headers
)
jwt_taker = response.headers.get("Access-Token")

# Perform the second request to get the jwt of taker
signature_maker = ethereum_signer_maker.sign(msg.encode()).signature
body = {
  "verifyType": 0,
  "address": address_maker,
  "message": "Access Login",
  "signature": signature_maker
}
response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/users",
    params = params, 
    data = json.dumps(body),
    headers = headers
)
jwt_maker = response.headers.get("Access-Token")

# Get slot and nounce for taker, we need to get it dynamically
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "content-type": "application/json",
    "Access-Token": jwt_taker
}
slotAndNouce = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/slot",
    params = params, 
    headers = headers
)
slot_taker = json.loads(slotAndNouce.text).get("slot")
nonce_taker = json.loads(slotAndNouce.text).get("nonce")

# Get slot and nounce for maker, we need to get it dynamically
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "content-type": "application/json",
    "Access-Token": jwt_maker
}
slotAndNouce = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/slot",
    params = params, 
    headers = headers
)
slot_maker = json.loads(slotAndNouce.text).get("slot")
nonce_maker = json.loads(slotAndNouce.text).get("nonce")

# Construct the taker's order
order_taker = Order(
        account_id=14721,
        price= 1500000000000000000000, # 1500
        amount= 10000000000000000, # 0.01
        sub_account_id=1,
        slot=int(slot_taker),
        nonce=int(nonce_taker),
        base_token=base_token,
        quote_token=quote_token,
        is_sell=1,
        taker_fee_ratio=255,
        maker_fee_ratio=255
    )
# ZK sign the taker's order
order_signature_hex_taker = zksigner_taker.sign_order(order_taker).signature

# Construct the maker's order
order_maker = Order(
        account_id=19450,
        price= 1500000000000000000000, # 1500
        amount= 10000000000000000, # 0.01
        sub_account_id=1,
        slot=int(slot_maker),
        nonce=int(nonce_maker),
        base_token=base_token,
        quote_token=quote_token,
        is_sell=0,
        taker_fee_ratio=255,
        maker_fee_ratio=255
    )
# ZK sign the maker's order
order_signature_hex_maker = zksigner_maker.sign_order(order_maker).signature
# Construct the order matching
# Ordermatching's account_id and sub_account_id is from submitter
# We need to calculate the base amount and quote amount accordingly
order_matching = OrderMatching(account_id=19450, sub_account_id=1, taker=order_taker,
                           maker=order_maker, fee=405000000000000,
                           fee_token=quote_token,
                           expect_base_amount=10000000000000000,
                           expect_quote_amount=15000000000000000000)

# ZK sign the order matching object
order_matching_signature = zksigner_maker.sign_tx(order_matching).signature
# ZK sign the order matching object as submitter 
order_matching_signature_submitter = zksigner_maker.sign_tx_as_submitter(order_matching)

# Payload params contain three parts
# 1. Ordermacthing object (signer by the submitter)
# 2. None, which should be a eth signature, but in order matching this is not needed
# 3. A submitter's signature, it is roughly similar as the #1 signature, but with one more hash on the serialized ordermatching object
payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "sendTransaction",
    "params": [
        {
            "type": "OrderMatching",
            "accountId": 19450,
            "subAccountId": 1,
            "taker": {
                "accountId": 14721,
                "subAccountId": 1,
                "slotId": slot_taker,
                "nonce": nonce_taker,
                "baseTokenId": 141,
                "quoteTokenId": 1,
                "amount": "10000000000000000",
                "price": "1500000000000000000000",
                "isSell": 1,
                "feeRatio1": 255,
                "feeRatio2": 255,
                "signature": {
                    "pubKey": pubkey_hex_taker,
                    "signature": order_signature_hex_taker
                }
            },
            "maker": {
                "accountId": 19450,
                "subAccountId": 1,
                "slotId": slot_maker,
                "nonce": nonce_maker,
                "baseTokenId": 141,
                "quoteTokenId": 1,
                "amount": "10000000000000000",
                "price": "1500000000000000000000",
                "isSell": 0,
                "feeRatio1": 255,
                "feeRatio2": 255,
                "signature": {
                    "pubKey": pubkey_hex_maker,
                    "signature": order_signature_hex_maker
                }
            },
            "fee": "405000000000000",
            "feeToken": 1,
            "expectBaseAmount": "10000000000000000",
            "expectQuoteAmount": "15000000000000000000",
            "signature": {
                "pubKey": pubkey_hex_maker,
                "signature": order_matching_signature
            }
        },
        None,
        {
            "pubKey": pubkey_hex_maker,
            "signature": order_matching_signature_submitter
        }
    ]
}

response = requests.post(
    "https://aws-gw-v2.zk.link/sendTransaction",
    data = json.dumps(payload),
    headers = headers
)

resultTx = json.loads(response.text).get("result")
print("Flash order matching")
print("See more detail from: https://test-scan.zk.link/tx/"+ resultTx)