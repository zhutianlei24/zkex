import requests
import pickledb
import inquirer

params = {}
jwt = pickledb.load('jwt.db', False).get("jwt")
tokenId = input("Please input the token id:")
chainId = ""
options = [
      inquirer.List("option",
                     message="Select an product: ",
                    choices=["transfer", "withdraw", "changepubkey"],
          ),
]
txType = inquirer.prompt(options).get("option")

if (txType != "transfer"):
    chainId = input("For withdraw and changepubkey transaction please also insert chainId:")
    params = {
    "tokenId": tokenId,
    "chainId": chainId,
    "txType": 3 if txType == "withdraw" else 6
    }  
else:
    params = {
    "tokenId": tokenId,
    "txType": 4
    }  

# So here we need to attach the jwt token which we obtained from step 5 to the request headers,
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Access-Token": jwt,
}

response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/layer2/estimateTxFee",
    headers = headers,
    params = params
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

print("https://github.com/ZKEX/orderbook-apis#l2EstimateTxFee")

print("===================")


