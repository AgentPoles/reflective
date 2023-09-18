from web3 import Web3
from web3.middleware import geth_poa_middleware
from scripts import jsonproducer
# Ethereum node URL (replace with your Ethereum node URL)
ethereum_node_url = 'https://eth-sepolia.g.alchemy.com/v2/T-sxo_sufcaSBdl7ww2U6FoOZwnpyNnU'

# Sender's wallet private key (replace with your private key)
private_key = '5913466bb0971661e17b14fa96b75fe9917bf94bb2cc983eeb35df256005e321'

# ERC-20 token contract address (replace with your contract address)
token_contract_address = '0xA530d751b2145d77386d9bbA8fB321E48729dE28'

# Sender's wallet address (replace with your address)
sender_wallet_address = '0xe459c175e06FFcE758CE14Ed7C4d016a6d9a858F'

# Recipient's wallet address (replace with recipient's address)
recipient_wallet_address = '0xf72F68301bd9E9DD1b7d48550A94E8A6EdF79145'

# Connect to Ethereum node
w3 = Web3(Web3.HTTPProvider(ethereum_node_url))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# Check if the private key is valid
if not w3.is_address(sender_wallet_address):
    print("Invalid sender wallet address.")
    exit(1)

# Check if the recipient address is valid
if not w3.is_address(recipient_wallet_address):
    print("Invalid recipient wallet address.")
    exit(1)

your_erc20_abi = [
    {
        "constant": False,
        "inputs": [
            {"name": "_to", "type": "address"},
            {"name": "_value", "type": "uint256"}
        ],
        "name": "transfer",
        "outputs": [{"name": "", "type": "bool"}],
        "type": "function"
    }
]
# Create a contract instance
contract = w3.eth.contract(address=token_contract_address, abi=your_erc20_abi)

# Amount of tokens to send

# Convert private key to bytes
private_key_bytes = bytes.fromhex(private_key)

def get_balance():
            
            token_abi = [
                {
                        "constant": True,
                        "inputs": [{"name": "_owner", "type": "address"}],
                        "name": "balanceOf",
                        "outputs": [{"name": "balance", "type": "uint256"}],
                        "type": "function",
                }
            ]

            # Create a contract instance
            contractb = w3.eth.contract(address=token_contract_address, abi=token_abi)

            # Get the balance of the wallet address
            token_balance = contractb.functions.balanceOf(sender_wallet_address).call()

            # Convert the balance from wei to the token's decimal places
            # Replace with the correct decimal places for the token
            decimal_places = 18
            token_balance /= 10 ** decimal_places

            print(f"Token Balance for {sender_wallet_address}: {token_balance} tokens")
            return token_balance


def get_brand_balance():
            
            token_abi = [
                {
                        "constant": True,
                        "inputs": [{"name": "_owner", "type": "address"}],
                        "name": "balanceOf",
                        "outputs": [{"name": "balance", "type": "uint256"}],
                        "type": "function",
                }
            ]

            # Create a contract instance
            contractb = w3.eth.contract(address=token_contract_address, abi=token_abi)

            # Get the balance of the wallet address
            token_balance = contractb.functions.balanceOf(recipient_wallet_address).call()

            # Convert the balance from wei to the token's decimal places
            # Replace with the correct decimal places for the token
            decimal_places = 18
            token_balance /= 10 ** decimal_places

            print(f"Token Balance for {sender_wallet_address}: {token_balance} tokens")
            return token_balance

def send_transaction(reward_amount):
    # Create a transaction
    amount_to_send = wei_amount = w3.to_wei(reward_amount, 'ether')
    nonce = w3.eth.get_transaction_count(sender_wallet_address)
    tx_params = {
        'nonce': nonce,
        'gasPrice': w3.to_wei('10', 'gwei'),  # Adjust gas price as needed
        'gas': 100000,  # Adjust gas limit as needed
        'to': token_contract_address,
        'value': 0,
        'data': contract.encodeABI(fn_name='transfer', args=[recipient_wallet_address, amount_to_send]),
        'chainId': 11155111,  # Mainnet
    }

    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx_params, private_key_bytes)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print(f"Transaction sent: https://etherscan.io/tx/{tx_hash.hex()}")

    brand_id = "0X12aed"
    transaction_hash = tx_hash.hex()
    print(transaction_hash)
    jsonproducer.produce_avro_message(brand_id, transaction_hash)
    return transaction_hash
   

    # Call the producer with the random brandId and transaction hash
    

if __name__ == "__main__":
    # Call the send_transaction function to initiate the transaction
    send_transaction()
