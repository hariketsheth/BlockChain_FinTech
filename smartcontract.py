from web3 import Web3
import json

matic = "https://testnetv3.matic.network/"


address = "0x692a70D2e424a56D2C6C27aA97D1a86395877b3A"

abi = json.loads('''[
{
"inputs": [
{
"internalType": "uint256",
"name": "id",
"type": "uint256"
},
{
"internalType": "address",
"name": "investorAdd",
"type": "address"
},
{
"internalType": "uint256",
"name": "_investment",
"type": "uint256"
}
],
"name": "addInvestor",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "id",
"type": "uint256"
},
{
"internalType": "address",
"name": "_buyer",
"type": "address"
},
{
"internalType": "uint256",
"name": "amount",
"type": "uint256"
}
],
"name": "setAmount",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "id",
"type": "uint256"
},
{
"internalType": "address",
"name": "_seller",
"type": "address"
},
{
"internalType": "uint256",
"name": "amount",
"type": "uint256"
}
],
"name": "setWorkingCapital",
"outputs": [],
"stateMutability": "nonpayable",
"type": "function"
},
{
"inputs": [
{
"internalType": "uint256",
"name": "id",
"type": "uint256"
}
],
"name": "getter",
"outputs": [
{
"internalType": "uint256",
"name": "",
"type": "uint256"
},
{
"internalType": "uint256",
"name": "",
"type": "uint256"
}
],
"stateMutability": "view",
"type": "function"
}
]
''')

web3 = Web3(Web3.HTTPProvider(matic))
contract = web3.eth.contract(address=address,abi=abi)

account = web3.eth.account.create()
print(account.address)


test = contract.functions.setAmount(1000,account.address,100).call()

print(contract.all_functions())
print(test)