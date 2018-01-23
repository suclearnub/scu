import requests

def get_price(coin):
    html = requests.get("https://api.coinmarketcap.com/v1/ticker/" + coin)
    data = html.json()[0]
    return int(data["price_usd"].split(".")[0])