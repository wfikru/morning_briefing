import requests
import os

token = os.getenv('TELEGRAM_BOT_TOKEN')
print('Token exists:', bool(token))
if token:
    r = requests.get(f'https://api.telegram.org/bot{token}/getMe')
    print('Bot check:', r.json())
else:
    print('TELEGRAM_BOT_TOKEN not set')