import pickledb
from web3 import Account
from zklink_sdk import EthereumSignerWeb3
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Token, Transfer

private_key = pickledb.load('key.db', False).get("private_key")

account = Account.from_key(private_key)
ethereum_signer = EthereumSignerWeb3(account=account)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

token = Token(id=141, chain_id=0, address='', symbol='', decimals=18)

zk_data = Transfer(
  account_id = 14721, ##l2userid???
  from_sub_account_id = 1,
  to_address = "0xdf705349D44903d7932026811Af8F256c2453228",
  to_sub_account_id = 1,
  token = token,
  amount = 10000000000000000,
  fee = 3000000000000000,
  nonce = 0,
  timestamp = 1694093962
)
zk_signature = zksigner.sign_tx(zk_data).signature
print("the zk signature is:")
print(zk_signature)
print("the pubkey hex is:")
print(pubkey_hex)

eth_data = "Transfer 0.01 wETH to: 0xdf705349d44903d7932026811af8f256c2453228\nFee: 0.003 wETH\nNonce: 0"

eth_signature = ethereum_signer.sign(eth_data.encode()).signature
print("the eth signature is:")
print(eth_signature)

