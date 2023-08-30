import requests
import json
import pickledb

params = {}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
}

response = requests.get(
    "https://aws-test-1.zkex.com/api-v1/api/tokens",
    params = params, 
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

print("Saving to database:")

print("*******************")

db = pickledb.load("tokens.db", False)

results = json.loads(response.text).get("result")

for tokenId in results:
    db.set(results.get(tokenId).get("symbol"), results.get(tokenId))

db.dump()

print("Saved")

print("*******************")

print()

print("See more docs here:")

print("===================")

print("https://github.com/ZKEX/orderbook-apis#gettokens")

print("===================")


