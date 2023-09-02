import requests
import pickledb
import json

params = {}

jwt = pickledb.load('jwt.db', False).get("jwt")

# So here we need to attach the jwt token which we obtained from step 5 to the request headers,
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
    "Access-Token": jwt
    
}

response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/users/self",
    params = params, 
    headers = headers
)

db = pickledb.load("account.db", False)
db.set("l2userId", json.loads(response.text).get("l2userId"))
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

print("https://github.com/ZKEX/orderbook-apis#getselfinfo")

print("===================")


