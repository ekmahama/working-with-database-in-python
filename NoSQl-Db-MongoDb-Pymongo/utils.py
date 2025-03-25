import datetime, random, requests

def get_random_datetime():
    return datetime.datetime.now() - datetime.timedelta(days=random.randint(1,7))

def get_coin_price(coin_id:str, currency:str):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(coin_id)}&vs_currencies={currency}"
    data = requests.get(url).json()
    coin_prices = dict([(coin_id, data[coin_id][currency]) for coin_id in data])
    return coin_prices

def util_seed_data(collection):
    collection.insert_many([
        {
            "name": "Bulls",
            "metadata": {
                "description": "Coins to buy",
                "currency":"usd",
                "data_created": get_random_datetime()
            },
            "coins": [
                {"coin": "bitcoin", "note": "The most popular coin", "date_added": get_random_datetime()},
                {"coin": "ethereum", "note": "The second most popular coin", "date_added": get_random_datetime()}
            ]
        },
        {
            "name": "Bears",
            "metadata": {
                "description": "Coins to buy",
                "currency":"usd",
                "data_created": get_random_datetime()
            },
            "coins": [
                {"coin": "dogecoin", "note": "The most popular meme coin", "date_added": get_random_datetime()},
                {"coin": "solana", "note": "Another meme coin", "date_added": get_random_datetime()}
            ]
        },
        {
            "name": "Sharks",
            "metadata": {
                "description": "High-risk coins",
                "currency": "usd",
                "date_created": get_random_datetime()
            },
            "coins": [
                {"coin": "ripple", "note": "A controversial coin", "date_added": get_random_datetime()},
                {"coin": "litecoin", "note": "An older coin", "date_added": get_random_datetime()}
            ]
        },
        {
            "name": "Whales",
            "metadata": {
                "description": "Large investments",
                "currency": "usd",
                "date_created": get_random_datetime()
            },
            "coins": [
                {"coin": "bitcoin", "note": "The most popular coin", "date_added": get_random_datetime()},
                {"coin": "ethereum", "note": "The second most popular coin", "date_added": get_random_datetime()},
                {"coin": "cardano", "note": "A promising coin", "date_added": get_random_datetime()}
            ]
        },
        {
            "name": "Dolphins",
            "metadata": {
                "description": "Medium-risk coins",
                "currency": "usd",
                "date_created": get_random_datetime()
            },
            "coins": [
                {"coin": "polkadot", "note": "A new coin", "date_added": get_random_datetime()},
                {"coin": "chainlink", "note": "A coin with potential", "date_added": get_random_datetime()}
            ]
        }
    ])