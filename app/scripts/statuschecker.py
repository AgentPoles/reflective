import requests
import time



def check_status(transaction_hash, api_key):
     
        # Maximum number of retries
        max_retries = 2

        # Delay between retries in seconds
        retry_delay = 15 # Adjust as needed

        etherscan_url = f"https://api-sepolia.etherscan.io/api?module=transaction&action=gettxreceiptstatus&txhash={transaction_hash}&apikey={api_key}"

        retry_count = 0
        while retry_count < max_retries:
            try:
                response = requests.get(etherscan_url)
                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == '1':
                        print(f"Transaction {transaction_hash} is confirmed.")
                        return True
                         # Transaction is confirmed, exit the loop
                    elif data['status'] == '0':
                        print(f"Transaction {transaction_hash} is not confirmed. Retrying...")
                    else:
                        print(f"Unable to determine the status of transaction {transaction_hash}. Retrying...")
                else:
                    print(f"Failed to retrieve transaction status. Status code: {response.status_code}. Retrying...")
            except Exception as e:
                print(f"An error occurred: {str(e)}. Retrying...")

            # Increment the retry count
            retry_count += 1

            # Wait before the next retry
            time.sleep(retry_delay)

        if retry_count >= max_retries:
            print(f"Reached maximum retry limit. Transaction {transaction_hash} status could not be determined.")
