#flash does not have the concept of token pairs, it will not be shown on the dashboard neither. The request goes through a specific endpoint. baseExchange/quoteExchange will only affect the final price (not the "calculated price" that you need to pay in oder to buy such an amount of token)
import requests
import json
import inquirer
import pickledb
from web3 import Account
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Order, Token

params = {}
private_key = pickledb.load('key.db', False).get("private_key")
l2userId = pickledb.load('account.db', False).get("l2userId")

jwt = pickledb.load('jwt.db', False).get("jwt")

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "content-type": "application/json",
    "Access-Token": jwt
}

# get slot and nounce, we need to get it dynamically
slotAndNouce = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/slot",
    params = params, 
    headers = headers
)

slot = json.loads(slotAndNouce.text).get("slot")
nonce = json.loads(slotAndNouce.text).get("nonce")

# initiate the product by asking user to select one of the supported products
choices=[]
products = pickledb.load('products.db', False)

for product in json.loads(products.get("products")):
    choices.append(product.get("id"))

# user select product to trade
options = [
      inquirer.List("option",
                     message="Select an product: ",
                    choices=choices,
          ),
]
productId = inquirer.prompt(options).get("option")

# based on the product user selected, we need to query its tokenId
tokens = pickledb.load('tokens.db', False)
baseTokenId = tokens.get(productId.split("-")[0]).get("id")
quoteTokenId = tokens.get(productId.split("-")[1]).get("id")

# user select buy or sell
options = [
      inquirer.List("option",
                     message="Select an action: ",
                    choices=["buy", "sell"],
          ),
]
side = inquirer.prompt(options).get("option")

size = str(int(float(input("Please input the size of buying/selling: ")) * (10 ** 18)))

if (side == "buy"):
    params = {
        "baseTokenId": baseTokenId,
        "quoteTokenId": quoteTokenId,
        "quoteExchange": size
    }
else:
    params = {
        "baseTokenId": baseTokenId,
        "quoteTokenId": quoteTokenId,
        "baseExchange": size
    }
askPrice = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/flashExchange/askPrice",
    headers = headers,
    params =  params
)
price = json.loads(askPrice.text).get("price")

# user select time in force
options = [
      inquirer.List("option",
                     message="Select an product: ",
                    choices=["GTC", "IOC", "GTX"],
          ),
]
timeInForce = inquirer.prompt(options).get("option")


account = Account.from_key(private_key)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

# If the user want to buy for example wETH, then we need to swap the baseTokenId with quoteTokenId -> sell USD for wETH
if (side == "buy"):
    temp = baseTokenId
    baseTokenId = quoteTokenId
    quoteTokenId = temp

order = Order(
        account_id=l2userId,
        price=int(price),
        amount=int(size),
        sub_account_id=1,
        slot=int(slot),
        nonce=int(nonce),
        base_token=Token(id=int(baseTokenId), chain_id=0, address='', symbol='', decimals=18),
        quote_token=Token(id=int(quoteTokenId), chain_id=0, address='', symbol='', decimals=18),
        is_sell=1,
        taker_fee_ratio=255,
        maker_fee_ratio=255
    )
order_signature_hex = zksigner.sign_order(order).signature

# construct the post body
body = {
  "productId": productId,
  "type": "limit",
  "side": "sell",
  "price": price,
  "size": size,
  "funds": str(int(price) * int(size) / (10 ** 18)),                  
  "l2UserId": l2userId,
  "slot": int(slot),
  "nonce": int(nonce),
  "l2baseCurrencyId": int(baseTokenId),             # layer2 base token id
  "l2quoteCurrencyId": int(quoteTokenId),            # layer2 quote token id
  "makerFeeRatio": 255,                # maker fee ratio, should be hard coded
  "takerFeeRatio": 255,               # taker fee ratio, should be hard coded
  "pubkey": pubkey_hex[2:] if pubkey_hex[0:2] == "0x" else pubkey_hex,
  "signature": order_signature_hex[2:] if order_signature_hex[0:2] == "0x" else order_signature_hex
}

print(body)

params = {}
response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/flashExchange/placeFlashOrder",
    params = params, 
    data = json.dumps(body),
    headers = headers
)

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

print("https://github.com/ZKEX/orderbook-apis#placeorder")

print("===================")


