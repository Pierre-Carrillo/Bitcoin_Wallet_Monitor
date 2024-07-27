import requests

def get_btc_to_usd():
    try:
        response = requests.get('https://blockchain.info/ticker')
        data = response.json()
        return data['USD']['last']
    except Exception as e:
        print("Error al obtener el valor de BTC en USD:", e)
        return None

def get_last_transaction(target_address):
    url = f"https://blockchain.info/rawaddr/{target_address}"
    response = requests.get(url)
    data = response.json()
    if 'txs' in data and len(data['txs']) > 0:
        return data['txs'][0]
    return None
