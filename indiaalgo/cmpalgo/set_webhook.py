import requests

bot_token = 'AAH-5IS_kMwluO8QQRQgbQr1uTSsdb34emY'
webhook_url = 'http://ai.anvestors.com/telegram-webhook/'  # Replace with your actual domain and webhook endpoint
set_webhook_url = f'https://api.telegram.org/bot{bot_token}/setWebhook?url={webhook_url}'

response = requests.get(set_webhook_url)
print(response.json())
