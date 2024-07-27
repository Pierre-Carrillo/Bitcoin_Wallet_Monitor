from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')
TARGET_ADDRESS = os.getenv('TARGET_ADDRESS')
MAX_RECONNECT_ATTEMPTS = int(os.getenv('MAX_RECONNECT_ATTEMPTS', 3))
TIMEZONE = os.getenv('TIMEZONE', 'America/Santiago')
