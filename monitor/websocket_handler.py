import json
import time
import websocket
from datetime import datetime
from config import TARGET_ADDRESS, MAX_RECONNECT_ATTEMPTS, TIMEZONE
from monitor.blockchain import get_btc_to_usd, get_last_transaction
from monitor.notifier import send_telegram_message
from utils.value_utils import format_btc_amount, get_usd_value
from utils.time_utils import format_time

last_transaction_hash = None
reconnect_attempts = 0

def on_message(ws, message):
    global last_transaction_hash
    transaction = json.loads(message)
    tx_hash = transaction['x']['hash']
    if tx_hash == last_transaction_hash:
        return

    inputs = transaction['x']['inputs']
    outputs = transaction['x']['out']

    address_in_inputs = any(TARGET_ADDRESS in inp['prev_out']['addr'] for inp in inputs if 'prev_out' in inp)
    address_in_outputs = any(TARGET_ADDRESS in out['addr'] for out in outputs if 'addr' in out)

    transaction_time = format_time(transaction['x']['time'], TIMEZONE)

    btc_to_usd = get_btc_to_usd()

    if address_in_inputs:
        btc_amount = sum(inp['prev_out']['value'] for inp in inputs if 'prev_out' in inp and TARGET_ADDRESS in inp['prev_out']['addr']) / 100000000
        usd_value = get_usd_value(btc_amount)
        message = f"Venta detectada en la dirección {TARGET_ADDRESS}:\n\nCantidad: {format_btc_amount(btc_amount)} BTC (${usd_value:.2f} USD)\nPrecio de Bitcoin: ${btc_to_usd:.2f} USD\nTx Hash: {tx_hash}\nHora: {transaction_time} (Chile)\nEstado: {'Pendiente' if not transaction['x'].get('block_height') else 'Confirmada'}"
        send_telegram_message(message)
        print(message)  # Imprimir en consola

    if address_in_outputs:
        btc_amount = sum(out['value'] for out in outputs if 'addr' in out and TARGET_ADDRESS in out['addr']) / 100000000
        usd_value = get_usd_value(btc_amount)
        message = f"Compra detectada en la dirección {TARGET_ADDRESS}:\n\nCantidad: {format_btc_amount(btc_amount)} BTC (${usd_value:.2f} USD)\nPrecio de Bitcoin: ${btc_to_usd:.2f} USD\nTx Hash: {tx_hash}\nHora: {transaction_time} (Chile)\nEstado: {'Pendiente' if not transaction['x'].get('block_height') else 'Confirmada'}"
        send_telegram_message(message)
        print(message)  # Imprimir en consola

    last_transaction_hash = tx_hash

def on_error(ws, error):
    print("Error:", error)

def on_close(ws, close_status_code, close_msg):
    global reconnect_attempts
    print("### WebSocket cerrado ###", ws, close_status_code, close_msg)
    reconnect_attempts += 1
    if reconnect_attempts <= MAX_RECONNECT_ATTEMPTS:
        delay = min(2 ** reconnect_attempts, 60)
        print(f"Reconectando en {delay} segundos...")
        # send_telegram_message(f"Reconectando en {delay} segundos...")
        time.sleep(delay)
        connect()
    else:
        send_telegram_message("El script tiene problemas de conexión. Se ha intentado reconectar 3 veces sin éxito.")

def on_open(ws):
    global reconnect_attempts, last_transaction_hash
    reconnect_attempts = 0
    print("### Conexión WebSocket abierta ###")
    subscribe_message = json.dumps({
        "op": "addr_sub",
        "addr": TARGET_ADDRESS
    })
    ws.send(subscribe_message)

    last_transaction = get_last_transaction(TARGET_ADDRESS)
    if last_transaction:
        tx_hash = last_transaction['hash']
        inputs = last_transaction['inputs']
        outputs = last_transaction['out']

        address_in_inputs = any(TARGET_ADDRESS in inp['prev_out']['addr'] for inp in inputs if 'prev_out' in inp)
        address_in_outputs = any(TARGET_ADDRESS in out['addr'] for out in outputs if 'addr' in out)

        transaction_time = format_time(last_transaction['time'], TIMEZONE)

        btc_to_usd = get_btc_to_usd()

        if tx_hash != last_transaction_hash:
            if address_in_inputs:
                btc_amount = sum(inp['prev_out']['value'] for inp in inputs if 'prev_out' in inp and TARGET_ADDRESS in inp['prev_out']['addr']) / 100000000
                usd_value = get_usd_value(btc_amount)
                message = f"Última transacción: Venta\nCantidad: {format_btc_amount(btc_amount)} BTC (${usd_value:.2f} USD)\nPrecio de Bitcoin: ${btc_to_usd:.2f} USD\nHora: {transaction_time} (Chile)\nEstado: {'Pendiente' if not last_transaction.get('block_height') else 'Confirmada'}"
                send_telegram_message(message)
                print(message)  # Imprimir en consola

            if address_in_outputs:
                btc_amount = sum(out['value'] for out in outputs if 'addr' in out and TARGET_ADDRESS in out['addr']) / 100000000
                usd_value = get_usd_value(btc_amount)
                message = f"Última transacción: Compra\nCantidad: {format_btc_amount(btc_amount)} BTC (${usd_value:.2f} USD)\nPrecio de Bitcoin: ${btc_to_usd:.2f} USD\nHora: {transaction_time} (Chile)\nEstado: {'Pendiente' if not last_transaction.get('block_height') else 'Confirmada'}"
                send_telegram_message(message)
                print(message)  # Imprimir en consola

            last_transaction_hash = tx_hash

def connect():
    ws = websocket.WebSocketApp("wss://ws.blockchain.info/inv",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()

if __name__ == "__main__":
    connect()
