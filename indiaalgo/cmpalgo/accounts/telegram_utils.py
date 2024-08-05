import requests


def send_telegram_message(chat_id, message):
    bot_token = 'AAH-5IS_kMwluO8QQRQgbQr1uTSsdb34emY'
    send_text = f'https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={message}'
    response = requests.get(send_text)
    return response.json()