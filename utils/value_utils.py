from monitor.blockchain import get_btc_to_usd

def format_btc_amount(amount):
    return f"{amount:.8f}"

def get_usd_value(btc_amount):
    btc_to_usd = get_btc_to_usd()
    if btc_to_usd is not None:
        return btc_amount * btc_to_usd
    else:
        return None
