import requests
import json

params = {}

body = {
  "verifyType": 0,
  "address": "0x3498F456645270eE003441df82C718b56c0e6666",
  "message": "Access Login",
  "signature": "0x1d5b31445b992a87b3f13bf686a48da291d2f332ae173b8948efbff2466824cd2a860eca1c22f45e63d819353b23fcdcae0195fd64b8e0308b629fd41f54bcf91b"
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

print("Sending request to:")

print(">>>>>>>>>>>>>>>>>>>")

print(response.url)

print(">>>>>>>>>>>>>>>>>>>")

print()

print("Getting response:")

print("<<<<<<<<<<<<<<<<<<<")

print(response.text)

print()

print("Returned with headers:")

print(response.headers)

print("<<<<<<<<<<<<<<<<<<<")

print()

print("See more docs here:")

print("===================")

print("https://github.com/ZKEX/orderbook-apis#register")

print("===================")


