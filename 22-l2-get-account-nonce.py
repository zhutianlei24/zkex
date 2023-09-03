#IMPORTANT: Get Account Nonce means get the main account's nonce, this nonce will only be used for ChangePubKey
import requests
import pickledb

jwt = pickledb.load('jwt.db', False).get("jwt")

# So here we need to attach the jwt token which we obtained from step 5 to the request headers,
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Access-Token": jwt  
}

response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/layer2/users/nonce",
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

print("https://github.com/ZKEX/orderbook-apis#l2accountnonce")

print("===================")


