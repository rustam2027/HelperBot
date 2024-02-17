import telebot
from telebot import types

TOKEN: str = '6924911833:AAEkGGKgCG-F91EWpJqXOnB7XqYJvhQ0wlA'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['send pic'])
def send_pic(message: types.Message):
    bot.reply_to(message, "done. nice. hello")


def send_message(user_message: types.Message, bot_message: str):
    bot.send_message(user_message.from_user.id, bot_message)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    send_message(message, "Привет!\nДобро пожаловать на Системное Программирование!\n"
                          "Это телеграм-бот для сдачи задач по курсам на нашем профиле.")
    send_message(message, "Для начала тебе нужно пройти регистрацию.")

    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(text='22126', callback_data="22126")
    btn2 = types.InlineKeyboardButton(text='23126', callback_data="23126")

    markup.add(btn1, btn2)

    bot.send_message(message.chat.id, "Выбери свою группу:", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def sendText(callback: types.CallbackQuery):
    msg = "aljalefjerfj"

    bot.send_message(callback.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
