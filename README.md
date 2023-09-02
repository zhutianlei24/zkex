# Install Dependencies
## Installation
My python version is 3.9.*, before you run this repository, you need to install dependencies by running the following commands:
```
pip install pickledb
pip install requests
pip install json
pip install inquirer
```
Besides, you need to install the zklink sdk (non-official):
```
git clone https://github.com/kinglear007/zklink-python
python setup.py install
```
The sdk needs rust and zk signer library support, you can install it by:
```
# Install rust
Find more info here: https://www.rust-lang.org/tools/install, you will need to install MSVC/GNU to successfully install rust.

# Build the zks-crypto-c library
git clone https://github.com/zksync-sdk/zksync-crypto-c
cd zks-crypto-c
# I am using MSVC so I use nmake to make the file
nmake
```
Last but not least, you need to set the dll (which is built above) absolute path in your PATH (```ZK_LINK_LIBRARY_PATH = ...\target\release\zks_crypto.dll```).

## Known Issues
### Unable to install zklink sdk
If you feel the dependency downloading takes forever (especially when you are physically located in Mainland China), you can change your pip source by add the following codes into ```setup.cfg``` file:
```
[easy_install]
index_url = https://pypi.tuna.tsinghua.edu.cn/simple
```
It is noticed that in Ubuntu 18, the build succeeds but the sdk can not be auto-detected by python. The solution is to write a for loop to manually add all egg files into sys.path.

When you are builing the zklink sdk in Windows, you need to install VC++ 2015. It is recommanded to install it (even though it is large) because you will need the MSVC later when you are installing rust.
### Unable to install rust
If you feel the rust initialization steps take forever (especially when you are physically located in Mainland China), you can change your rust downloading source to solve this issue. 

# Scripts Execution Order
Generally the scripts should be executed in the order, some scripts will register necessary infos in pickledb and those infos will be reused in some other scripts. A script which is marked as optional below means it is a pure GET script.

In order to successfully execute the following scripts, you need to initiate your layer 2 account in ```testnet.app.zkex.com```.
## Record Account
Register your private key in db.
## Get Server Time [Optional]
Get the server time in linux epoch time format.
## Get Supported Tokens
Get the supported token pairs from server. This step will register those token pairs in db.
## Get Supported Chains [Optional]
Get the supported chains (with chain id) from server.
## Post Signup/Login
Signup/Login for/into your account. This step will register a jwt-like token in db for future access.
## Get User Info
Get the your account info. This step will register your layer 2 user id in db.
## Get Orders [Optional]
Get the orders list which is made by you.
## Get Previous Orders [Optional]
Get the orders list which is made by you (with pagniation).
## Get Trades [Optional]
Get the trade history of your account.
## Get Previous Trades [Optional]
Get the trade history of your account (with pagniation).
## Get User Slot [Optional]
Query your next available slot.
## Post Place Order
Place an order with your account. For ```timeInForce``` please select GTC, the other options are not tested yet. Once your order is made, you can view it in ```testnet.app.zkex.com```.