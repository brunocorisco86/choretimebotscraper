import requests
import logging
from config import TELEGRAM_TOKEN, CHAT_ID

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def send_telegram_message(message):
    if not TELEGRAM_TOKEN or not CHAT_ID:
        logging.warning("TELEGRAM_TOKEN ou CHAT_ID não configurados. Não foi possível enviar mensagem via Telegram.")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Levanta um erro para códigos de status HTTP ruins (4xx ou 5xx)
        logging.info(f"Mensagem Telegram enviada com sucesso: {message}")
        return True
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro ao enviar mensagem via Telegram: {e}")
        return False
