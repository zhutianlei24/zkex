import requests
import json
import pickledb
from zklink_sdk import EthereumSignerWeb3
from web3 import Account
# from zklink_sdk.ethereum_signer import ZkLinkLibrary, ZkLinkSigner
# from zklink_sdk.types import Order, Token

params = {}
private_key = pickledb.load('key.db', False).get("private_key")
address = pickledb.load('account.db', False).get("address")

msg = "Access Login"
account = Account.from_key(private_key)
ethereum_signer = EthereumSignerWeb3(account=account)
signature = ethereum_signer.sign(msg.encode()).signature

body = {
  "verifyType": 0,
  "address": address,
  "message": "Access Login",
  "signature": signature
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "content-type": "application/json"
}

response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/users",
    params = params, 
    data = json.dumps(body),
    headers = headers
)

db = pickledb.load("jwt.db", False)
db.set("jwt", response.headers.get("Access-Token"))
db.dump()

print("Sending request to:")

print(">>>>>>>>>>>>>>>>>>>")

print(response.url)

print(">>>>>>>>>>>>>>>>>>>")

print()

print("Getting response:")

print("<<<<<<<<<<<<<<<<<<<")

print(response.text)

print("<<<<<<<<<<<<<<<<<<<")

print()

print("See more docs here:")

print("===================")

print("https://github.com/ZKEX/orderbook-apis#register")

print("===================")


