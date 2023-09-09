import pickledb
from web3 import Account
from zklink_sdk import EthereumSignerWeb3
from zklink_sdk import ZkLinkLibrary, ZkLinkSigner
from zklink_sdk.types import Token, Withdraw

private_key = pickledb.load('key.db', False).get("private_key")

account = Account.from_key(private_key)
ethereum_signer = EthereumSignerWeb3(account=account)
zksigner = ZkLinkSigner.from_account(account, ZkLinkLibrary())
pubkey_hex = zksigner.public_key.hex()

l1_target_token = Token(id=1, chain_id=0, address='', symbol='', decimals=18)
l2_source_token = Token(id=141, chain_id=0, address='', symbol='', decimals=18)

zk_data = Withdraw(
    to_chain_id = 1,
    account_id = 14721,
    sub_account_id = 1,
    to_address = "0x18C86896adE5841E2c81e5BcaFBF83B1c8d34281",
    l2_source_token = l2_source_token,
    l1_target_token = l1_target_token,
    amount = 10000000000000000,
    fee = 3000000000000000,
    nonce = 1,
    fast_withdraw = 1,
    withdraw_fee_ratio = 10000,
    timestamp = 1694093963
)

zk_signature = zksigner.sign_tx(zk_data).signature
print("the zk signature is:")
print(zk_signature)
print("the pubkey hex is:")
print(pubkey_hex)

eth_data = "Withdraw 0.01 wETH to: 0x18C86896adE5841E2c81e5BcaFBF83B1c8d34281\nFee: 0.003 wETH\nNonce: 1"

eth_signature = ethereum_signer.sign(eth_data.encode()).signature
print("the eth signature is:")
print(eth_signature)

