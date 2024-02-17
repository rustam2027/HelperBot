import telebot
from telebot.types import Message

TOKEN: str = '6924911833:AAEkGGKgCG-F91EWpJqXOnB7XqYJvhQ0wlA'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['send pic'])
def send_pic(message: Message):
    bot.reply_to(message, "done. nice. hello")


@bot.message_handler(commands=['start'])
def start(message: Message):
    bot.send_message(message.from_user.id, "hello")


def __main__():
    bot.polling(none_stop=True, interval=0)
