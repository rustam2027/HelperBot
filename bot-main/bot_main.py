import telebot
from telebot import types

# import Manager

TOKEN: str = '6924911833:AAEkGGKgCG-F91EWpJqXOnB7XqYJvhQ0wlA'

bot = telebot.TeleBot(TOKEN)


# manager = new Manager()


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

    # TODO: check 4 groups
    # groups_list = manager.get_groups()
    groups_list = ["22126", "23126"]
    markup = types.InlineKeyboardMarkup()
    for group in groups_list:
        btn = types.InlineKeyboardButton(text=group, callback_data=group)
        # btn = types.InlineKeyboardButton(text=group.number, callback_data=group.number)
        markup.add(btn)

    bot.send_message(message.chat.id, "Выбери свою группу:", reply_markup=markup)


@bot.callback_query_handler(func=lambda button: str.isdigit(button.data))
def get_group(group: types.CallbackQuery):
    # students = manager.get_students(group.data)
    markup = types.InlineKeyboardMarkup()
    students = ["Mark Boe", "Maria Vasko", "Taisia Petruneva", "Baldeem"]

    for student in students:
        btn = types.InlineKeyboardButton(text=student, callback_data=student)
        # btn = types.InlineKeyboardButton(text=student.name, callback_data=student.name)
        markup.add(btn)

    bot.send_message(message.chat.id, "Выбери себя:", reply_markup=markup)

    # match group.data:
    #     case "22126":
    #         bot.send_message(group.message.chat.id, "22126")
    #     case "23126":
    #         bot.send_message(group.message.chat.id, "23126")
    msg = "Good job!"
    bot.send_message(group.message.chat.id, msg)


bot.polling(none_stop=True, interval=0)
