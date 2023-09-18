from web3 import Web3
from web3.middleware import geth_poa_middleware

# Initialize a Web3 provider (replace with your Ethereum node URL)
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/T-sxo_sufcaSBdl7ww2U6FoOZwnpyNnU'))

# Add middleware for handling PoA networks (for Ganache, etc.)
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Replace with your private key, token contract address, and wallet address
private_key = '5913466bb0971661e17b14fa96b75fe9917bf94bb2cc983eeb35df256005e321'
token_contract_address = '0xA530d751b2145d77386d9bbA8fB321E48729dE28'
wallet_address = '0xf72F68301bd9E9DD1b7d48550A94E8A6EdF79145'
amount_to_send = 2  # Adjust this to the desired amount

# Convert private key to bytes
private_key_bytes = bytes.fromhex(private_key)

# Create a transaction
transaction = {
    'to': token_contract_address,
    'value': 0,
    'gasPrice': w3.toWei('10', 'gwei'),  # Adjust gas price as needed
    'gas': 100000,  # Adjust gas limit as needed
    'nonce': w3.eth.getTransactionCount(wallet_address),
    'chainId': 1,  # Mainnet
}

# Sign the transaction
signed_transaction = w3.eth.account.signTransaction(transaction, private_key_bytes)

# Send the transaction
tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)

print(f"Transaction sent: https://etherscan.io/tx/{tx_hash.hex()}")
