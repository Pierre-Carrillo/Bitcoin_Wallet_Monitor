# Bitcoin Wallet Monitor

This script monitors a Bitcoin address and sends notifications to a Telegram chat when transactions are detected.

## Requirements

- Python 3.x
- WebSocket-client
- Requests
- Pytz
- Python-dotenv

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/bitcoin-wallet-monitor.git
   cd bitcoin-wallet-monitor
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the root directory with the following content:
   ```env
   TELEGRAM_TOKEN=your_telegram_token
   CHAT_ID=your_chat_id
   TARGET_ADDRESS=your_bitcoin_address
   TIMEZONE=your_TZ_for_example_America/Santiago
   ```

## Usage

To run the script, use the following command:

```bash
python main.py
```

## Telegram Configuration

1. Create a bot on Telegram and get the token. You can do this by talking to [BotFather](https://t.me/BotFather).
2. Get your `chat_id` by sending a message to the bot and visiting the following URL:
   ```bash
   https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates
   ```

## License

This project is licensed under the MIT License.
