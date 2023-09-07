import requests
import pickledb
import inquirer

jwt = pickledb.load('jwt.db', False).get("jwt")
params: {}

baseTokenId = input("Please input the base token id: ")
quoteTokenId = input("Please input the quote token id: ")
options = [
      inquirer.List("option",
                     message="You want to query for: ",
                    choices=["base token", "quote token"],
          ),
]
tokenType = inquirer.prompt(options).get("option")
# amount = str(int(input("With amount: ")) * 10 ** 18)
amount = str(int(float(input("Please input the size of buying/selling: ")) * (10 ** 18)))

if (tokenType == "base token"):
    params = {
        "baseTokenId": baseTokenId,
        "quoteTokenId": quoteTokenId,
        "baseExchange": amount
    }
else:
    params = {
        "baseTokenId": baseTokenId,
        "quoteTokenId": quoteTokenId,
        "quoteExchange": amount
    }

# So here we need to attach the jwt token which we obtained from step 5 to the request headers,
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Access-Token": jwt  
}

response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/flashExchange/askPrice",
    headers = headers,
    params =  params
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

print("https://github.com/ZKEX/orderbook-apis#askprice")

print("===================")


