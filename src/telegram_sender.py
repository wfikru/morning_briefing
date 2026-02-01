import os
from telegram import Bot

def send_to_telegram(message):
    bot = Bot(token=os.environ["TELEGRAM_BOT_TOKEN"])
    channel_id = os.environ["TELEGRAM_CHANNEL_ID"]

    bot.send_message(
        chat_id=channel_id,
        text=message
    )
