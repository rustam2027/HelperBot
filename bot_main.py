import telebot
from telebot import types
import re

from Student import Student

# import Manager

students_info: dict[str: Student] = {}

TOKEN: str = '6924911833:AAEkGGKgCG-F91EWpJqXOnB7XqYJvhQ0wlA'

bot = telebot.TeleBot(TOKEN)


# manager = Manager()


@bot.message_handler(commands=['send_pic'])
def send_pic(message: types.Message):
    bot.reply_to(message, "done. nice. hello")


@bot.message_handler(commands=['help'])
def send_message_help(message: types.Message):
    bot.reply_to(message, "Если вы ошиблись при вводе данных, напишите /reset, чтобы начать все сначала.")


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

    # groups_list = manager.groups.keys()
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
    current_student = students_info[student.message.chat.id]
    current_student.name = student.data

    # students_info[student.message.chat.id].name = student.data
    # group_number = students_info[student.message.chat.id].group
    # courses = manager.groups[group_number].courses  # dict

    courses = {'Алгоритмы': None, "C++": None}
    courses = ["Алгоритмы", "С++", "ИОС"]
    count = len(courses) - 1
    msg = bot.send_message(student.message.chat.id, "Время скинуть ссылки на репозитории!")

    get_repositories(msg, courses, count, current_student)

    students_info[student.message.chat.id] = current_student

    # print_student(current_student)


def get_repositories(message, courses, count, student: Student):
    if message.text != "Время скинуть ссылки на репозитории!":
        user_url = message.text
        ex_count = count + 1
        student.github_urls[courses[ex_count]] = user_url

    # if check_github_url(message, courses, count, student):
    #     print("valid!!")

    if count >= 0:
        msg = bot.send_message(message.chat.id, f"Скинь ссылку на репозиторий по предмету {courses[count]}")
        count -= 1
        bot.register_next_step_handler(msg, get_repositories, courses, count, student)
    else:
        bot.send_message(message.chat.id, "Все заполнено, вы успешно зарегистрировались!")
        students_info[student.chat_id] = student
        print_student(student)
        # TODO: function in manager to give them Student


# Function to provide a poll with multiple answering options for users
@bot.poll_answer_handler(func=lambda x: True)
def provide_multiple_answer_poll(chat_id):
    poll_question = "Which programming languages do you know?"
    options = ["Python", "JavaScript", "Java", "C++", "Ruby", "ИОС", "фцувфцувуцв", "выацувфцв"]

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, selective=True)
    for option in options:
        button = types.KeyboardButton(option)
        markup.add(button)

    bot.send_message(chat_id, poll_question, reply_markup=markup)


# Handler for the command /multiple_answer_poll
@bot.message_handler(commands=['multiple_answer_poll'])
def handle_multiple_answer_poll(message):
    chat_id = message.chat.id
    provide_multiple_answer_poll(chat_id)


# Handler for processing user answers in the poll
@bot.message_handler(func=lambda message: True)
def handle_user_answers(message):
    user_answers = message.text.split('\n')
    response = f"Your answers: {', '.join(user_answers)}"
    bot.reply_to(message, response)


# TODO: make it work correctly
def check_github_url(user_message: types.Message, courses, count, student: Student):
    github_link_regex = r'^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9](?:-?[a-zA-Z0-9])*(?:\/[a-zA-Z0-9](?:-?[a-zA-Z0-9])*)*$'
    # github_link_regex = "https://github.com/rustam2027/HelperBot/blob/google_connection/Manager.py"

    if not re.match(github_link_regex, user_message.text):
        # send_message(user_message, "Ссылка невалидная! Попробуй еще раз!")
        msg = bot.send_message(user_message.chat.id, "Ссылка невалидная! Попробуй еще раз!")
        bot.register_next_step_handler(msg, get_repositories, courses, count, student)
        return False
    return True


def print_student(student: Student):
    print("Имя: ", student.name)
    print("Группа: ", student.group)
    print("Репозитории: ", student.github_urls)
    print("ID: ", student.chat_id)


bot.polling(none_stop=True, interval=0)
