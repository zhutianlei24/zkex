import requests
import json
import inquirer
import pickledb

params = {}

jwt = input("Please input the JWT token which can be obtained in step 5: ")

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
                     message="Select an product: ",
                    choices=["buy", "sell"],
          ),
]
side = inquirer.prompt(options).get("option")

# ordinary inputs
price = input("Please input the price of buying/selling: ") # *???

size = input("Please input the size of buying/selling: ") # *???

# user select time in force
options = [
      inquirer.List("option",
                     message="Select an product: ",
                    choices=["GTC", "IOC", "GTX"],
          ),
]
timeInForce = inquirer.prompt(options).get("option")


# construct the post body
body = {
  "productId": productId,
  "side": side,
  "type": "limit",   # what else? other type may trigger a different input flow
  "price": price,
  "size": size,
  "funds": "70000000",  # what does this mean?                     
  "l2UserId": 2,                  # layer2上的用户id, should be hard coded
  "slot": int(slot),
  "nonce": int(nonce),
  "l2baseCurrencyId": int(baseTokenId),             # layer2交易对base资产id
  "l2quoteCurrencyId": int(quoteTokenId),            # layer2交易对quote资产id
  "makerFeeRatio": 5,                # maker交易手续费费率, 单位   万分之一, should be hard coded
  "takerFeeRatio": 10,               # taker交易手续费费率, 单位   万分之一, should be hard coded
  "validFrom": 1000000,              # no clue
  "validUntil": 1000000,             # no clue
  "pubkey": "0dd4f603531bd78bbecd005d9e7cc62a794dcfadceffe03e269fbb6b72e9c724",   # 用户的layer2 pubkey, should be hard coded
  "signature": "6f7538765f174de449b3e618bf1fe94714638a4cd8d35fecdc42e34860a291a5f470e2cdd2fbf196c3a6953fecb15b093c86b6e00c412522a6ff399c211b8503", # how to get this?
  "timeInForce": timeInForce,               # GTC: 订单会一直有效, 直到被成交或者取消     IOC: 无法立即成交的部分就撤销     GTX:  只挂单提供流动性不成交，如果失败的话则撤销挂单
  "isStop": 1,                        # 是否stop limit单, no clue
  "stopCondition": "gt",              # stop limit 挂单匹配条件   gt 大于  ge 大于等于  lt小于  le小于等于, no clue
  "stopPrice": "100000000",            # stop limit 挂单匹配价格, no clue
  "isIceberg": 1,                     # 是否冰山单, no clue
  "exposedSize": "80000000000000000"    # 冰山单可见委托大小, no clue
}

print(body)

response = requests.post(
    "https://aws-test-1.zkex.com/api-v1/api/orders",
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


