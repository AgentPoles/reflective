import requests

def fetch_eth_price():
        # Replace with your CoinMarketCap API key
        api_key = 'cbd98ded-2b5a-4f53-9898-ddc25c13ee38'

        # CoinMarketCap API URL for Ethereum (ETH) data
        url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'

        # Parameters for the API request
        params = {
            'symbol': 'ETH',  # Symbol for Ethereum
            'convert': 'USD',  # Convert to US Dollar
        }

        # Headers with your API key
        headers = {
            'X-CMC_PRO_API_KEY': api_key,
        }

        try:
            # Send the GET request to CoinMarketCap API
            response = requests.get(url, params=params, headers=headers)

            # Check if the request was successful (status code 200)
            if response.status_code == 200:
                data = response.json()
                # Extract the current price of Ethereum in USD
                eth_price_usd = data['data']['ETH']['quote']['USD']['price']
                
                print(f'Current Ethereum (ETH) price in USD: ${eth_price_usd:.2f}')
                return eth_price_usd
            else:
                print(f'Failed to retrieve data. Status code: {response.status_code}')
                return 0
        except Exception as e:
            print(f'An error occurred: {str(e)}')
            return 0
