import requests
from utils.statuschecker import check_status
import time
# Replace with your Etherscan API key
etherscan_api_key = '7UF5DDU7F2QK5E9IH557Z8T593TPY6HXTC'


def fetch_cost(transaction_hash="0x3ff14b22d3bba6fa882bf4c58f30147e145ea60c47320c37fe20a90756e33f23"):

    # Etherscan API endpoint for retrieving transaction details
    etherscan_url = f'https://api-sepolia.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={transaction_hash}&apikey={etherscan_api_key}'
    etherscan_url_b = f'https://api-sepolia.etherscan.io/api?module=proxy&action=eth_getTransactionReceipt&txhash={transaction_hash}&apikey={etherscan_api_key}'
    
         # Maximum number of retries
    max_retries = 2

        # Delay between retries in seconds
    retry_delay = 15 # Adjust as needed
    retry_count = 0
        
    while retry_count < max_retries:
                try:
                    # Make a GET request to the Etherscan API
                    if(check_status(transaction_hash,etherscan_api_key)):
                        response = requests.get(etherscan_url)
                        responseb = requests.get(etherscan_url_b)
                        data = response.json()
                        datab = responseb.json()
                    
                        gas_price_hex = '0x0'
                        gas_used_hex =  '0x0'
                        # Check if the API request was successful
                        if data['result']:
                            gas_price_hex = data['result']['gasPrice']
                        else:
                            print('API request failed. Check the transaction hash and API key....Retrying')
                    
                        if datab['result']:
                            gas_used_hex = datab['result']['gasUsed']
                        else:
                            print('API request failed. Check the transaction hash and API key...Retrying.')

                        # Convert 'gas' and 'gasPrice' from hexadecimal to decimal
                        gas_wei = int(gas_used_hex, 16)
                        gas_price_wei_per_unit = int(gas_price_hex, 16)

                        # Calculate the transaction fee in Wei
                        transaction_fee_wei = gas_wei * gas_price_wei_per_unit

                        # Convert the transaction fee from Wei to Ether
                        transaction_fee_eth = transaction_fee_wei / 1e18  # Convert fr om Wei to Ether
                        if(transaction_fee_eth == 0):
                            retry_count += 1
                            # Wait before the next retry
                            time.sleep(retry_delay)
                        
                        else:
                
                         return transaction_fee_eth

                except Exception as e:
                    print(f'Error: {e}')

if __name__ == "__main__":
    # Call the send_transaction function to initiate the transaction
    fetch_cost()
