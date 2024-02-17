import telebot
from telebot import types
import re

from Student import Student

# import Manager

students_info: dict[str: Student] = {}

TOKEN: str = '6924911833:AAEkGGKgCG-F91EWpJqXOnB7XqYJvhQ0wlA'

bot = telebot.TeleBot(TOKEN)


# manager = new Manager()


@bot.message_handler(commands=['send pic'])
def send_pic(message: types.Message):
    bot.reply_to(message, "done. nice. hello")


@bot.message_handler(commands=['reset'])
def reset(message: types.Message):
    students_info[message.chat.id] = None


def send_message(user_message: types.Message, bot_message: str, markup=None):
    bot.send_message(user_message.from_user.id, bot_message, reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message: types.Message):
    students_info[message.chat.id] = Student(str(message.chat.id))

    send_message(message, "Привет!\nДобро пожаловать на Системное Программирование!\n"
                          "Это телеграм-бот для сдачи задач по курсам на нашем профиле.")
    send_message(message, "Для начала тебе нужно пройти регистрацию.")

    # groups_list = manager.get_groups()
    groups_list = ["22126", "23126"]
    markup = types.InlineKeyboardMarkup()
    for group in groups_list:
        btn = types.InlineKeyboardButton(text=group, callback_data=group)
        # btn = types.InlineKeyboardButton(text=group.number, callback_data=group.number)
        markup.add(btn)

    send_message(message, "Выбери свою группу:", markup)


@bot.callback_query_handler(func=lambda group_button: group_button.data.endswith("126"))
def get_group(group: types.CallbackQuery):
    # students = manager.get_students(group.data)
    students_info[group.message.chat.id].group = group.data

    markup = types.InlineKeyboardMarkup()
    students = ["Mark Boe", "Maria Vasko", "Taisia Petruneva", "Baldeem"]

    for student in students:
        btn = types.InlineKeyboardButton(text=student, callback_data=student)
        # btn = types.InlineKeyboardButton(text=student.name, callback_data=student.name)
        markup.add(btn)

    bot.send_message(group.message.chat.id, "Выбери себя:", reply_markup=markup)


def no_numbers(input_string: str):
    return not bool(re.search(r'\d', input_string))


@bot.callback_query_handler(func=lambda student_button: no_numbers(student_button.data))
def get_student(student: types.CallbackQuery):
    students_info[student.message.chat.id].name = student.data
    group_number = students_info[student.message.chat.id].group
    # courses = manager.groups[group_number].courses  # dict

    courses = {'Алгоритмы': None, "C++": None}
    # count = len(courses)
    # bot.register_next_step_handler(msg, repeat)
    # def repeat(message, count):
    #     text = message.text
    #     if count > 0:
    #         msg = bot.send_message(student.message.chat.id, 'Great! Next question!')
    #         count -= 1
    #         bot.register_next_step_handler(msg, repeat)
    #     else:
    #         bot.send_message(student.message.chat.id, "Вы успешно зарегистрировались!")

    for course in courses:
        msg = bot.send_message(student.message.chat.id, f"Скиньте ссылку на репозиторий по предмету {course}")
        bot.register_next_step_handler(msg, input_user_github)

    bot.send_message(student.message.chat.id, "Вы успешно зарегистрировались!")


@bot.message_handler(func=lambda c: True)
def input_user_github(message):
    x = message.text
    print(x)


bot.polling(none_stop=True, interval=0)
