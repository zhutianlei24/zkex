import pickledb

private_key = input("Please input your private key: ")
address = input("Please input your address: ")

db = pickledb.load("key.db", False)
db.set("private_key", private_key)
db.dump()

db = pickledb.load("account.db", False)
db.set("address", address)
db.dump()

print("Saved")