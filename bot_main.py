from dataclasses import dataclass

import telebot
from telebot import types
import re
from typing import Dict

from DTO.Student import Student

from Manager import Manager
from logger import log
from config import TOKEN


bot = telebot.TeleBot(TOKEN)
manager = Manager()


@bot.message_handler(commands=['send_pic'])
def send_pic(message: types.Message):
    return
    with open("C:/Users/Home/Desktop/HelperBot/Pictures/cat.jpg", 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['send_gif'])
def send_gif(message: types.Message):
    return
    with open("C:/Users/Home/Desktop/HelperBot/Pictures/video.mp4", 'rb') as gif:
        bot.send_video(message.chat.id, gif)


@bot.message_handler(commands=['help'])
def send_message_help(message: types.Message):
    bot.reply_to(message,
                 "Этот бот создан, чтобы помочь студентам сдавать задачи по курсам нашего профиля. Вам доступны следующие команды:\n"
                 "/help - объяснение!\n"
                 "/tasks - вам будет предоставлен список задач по предметам\n"
                 "/reset - можете воспользоваться данной командой, если вы неправильно ввели свои данные при регистрации\n"
                 "/send_pic - отправляет фото)"
                 "/send_gif - отправляет video)")


def send_message(user_message: types.Message, bot_message: str, markup=None):
    bot.send_message(user_message.from_user.id,
                     bot_message, reply_markup=markup)


@bot.message_handler(commands=['start', 'reset'])
def start(message: types.Message):
    send_message(message, "Привет!\nДобро пожаловать на Системное Программирование!\n"
                          "Это телеграм-бот для сдачи задач по курсам на нашем профиле.")
    send_message(message, "Для начала тебе нужно пройти регистрацию.")

    groups_list = manager.groups.values()

    markup = types.InlineKeyboardMarkup()
    for group in groups_list:
        btn = types.InlineKeyboardButton(
            text=group.number, callback_data=group.number)
        markup.add(btn)

    send_message(message, "Выбери свою группу:", markup)


@bot.message_handler(commands=['tasks'])
def pass_tasks(message: types.Message):
    if (message.chat.id not in students_info):  # Check if user have registration
        send_message(message, "Ты еще не зарегестрировался!!!!")
        return

    student = students_info[message.chat.id]
    send_message(message, "О, ты готов сдавать задачи? Супер)")
    groups = manager.groups[student.group].courses
    markup = types.InlineKeyboardMarkup()
    for name, course in groups.items():
        btn = types.InlineKeyboardButton(
            text=name, callback_data=f'course {name}')
        markup.add(btn)
    bot.send_message(
        message.chat.id, "Тогда тебе нужно выбрать курс:", reply_markup=markup)


@bot.callback_query_handler(
    func=lambda course_button: course_button.data.startswith("course") and not str.isnumeric(course_button.data))
def get_tasks(course: types.CallbackQuery):
    bot.delete_message(course.from_user.id, course.message.message_id)
    student = students_info[course.from_user.id]
    course_current = course.data.split()[1]
    unresolved_tasks = manager.read_current_tasks(student, course_current)
    markup = types.InlineKeyboardMarkup()
    if len(unresolved_tasks) == 0:
        bot.send_message(course.from_user.id, "Все задачи сданы! Молодец!")
    else:
        for task in unresolved_tasks:
            btn = types.InlineKeyboardButton(
                text=task, callback_data=f'task {course_current} {task}')
            markup.add(btn)
        bot.send_message(course.from_user.id,
                         "Выбери задачу:", reply_markup=markup)


def check_correct_task(user_input: str):
    return user_input.startswith("task")


@bot.callback_query_handler(func=lambda task_button: check_correct_task(task_button.data))
def get_task(task: types.CallbackQuery):
    bot.delete_message(task.from_user.id, task.message.message_id)
    _, course_name, task_current = task.data.split()
    manager.receive(students_info[task.from_user.id],
                    task_current, course_name)
    bot.send_message(task.from_user.id,
                     f"Вы отправили {task_current} задачу по {course_name}!")


@bot.callback_query_handler(func=lambda group_button: group_button.data.endswith("126") and len(group_button.data) == 5)
def get_group(group: types.CallbackQuery):
    bot.delete_message(group.from_user.id, group.message.message_id)
    students: list[Student] = manager.get_students(group.data)
    markup = types.InlineKeyboardMarkup()

    for i, student in enumerate(students):
        btn = types.InlineKeyboardButton(
            text=student.name, callback_data=f"{i} {group.data}")
        markup.add(btn)

    bot.send_message(group.message.chat.id,
                     "Выбери себя:", reply_markup=markup)


def student_check(str_student: str):
    return len(str_student) > 5 and re.match("^[0-9 ]+$", str_student)


@bot.callback_query_handler(func=lambda student_button: student_check(student_button.data))
def get_student(student: types.CallbackQuery):
    bot.delete_message(student.from_user.id, student.message.message_id)
    student_number, group_number = student.data.split()
    student_number = int(student_number)
    student_tg = '@' + student.from_user.username
    courses = list(manager.groups[group_number].courses.keys())

    count = len(courses) - 1
    msg = bot.send_message(student.message.chat.id,
                           "Время скинуть ссылки на репозитории!")

    current_student = manager.groups[group_number].students[student_number]
    current_student.tg = student_tg
    get_repositories(msg, courses, count, current_student)

    manager.groups[group_number].students[student_number] = current_student
    students_info[student.from_user.id] = current_student


@dataclass
class Request:
    url: str | None


def get_repositories(message, courses: list, count: int, student: Student):
    if message.text != "Время скинуть ссылки на репозитории!":
        request = Request(None)
        check_github_url(message, request)
        while request.url is None:
            continue
        user_url = request.url
        ex_count = count + 1
        student.github[courses[ex_count]] = user_url

    if count >= 0:
        msg = bot.send_message(
            message.chat.id, f"Скинь ссылку на репозиторий по предмету {courses[count]}")
        count -= 1
        bot.register_next_step_handler(
            msg, get_repositories, courses, count, student)
    else:
        provide_multiple_answer_poll(
            message.chat.id, "Все заполнено, вы успешно зарегистрировались!")
        students_info[student.chat_id] = student
        log(f"Bot: user {student.name} registered")
        # TODO: function in manager to give them Student


# TODO: make it work correctly
def check_github_url(user_message: types.Message, request: Request):
    github_link_regex = r'(https?:\/\/)github\.com\/(.+?)\/'

    if not re.match(github_link_regex, user_message.text):
        msg = bot.send_message(user_message.chat.id,
                               "Ссылка невалидная! Попробуй еще раз!")
        bot.register_next_step_handler(msg, check_github_url, request)
    else:
        request.url = user_message.text


# Function to provide a poll with multiple answering options for users
@bot.poll_answer_handler(func=lambda x: True)
def provide_multiple_answer_poll(chat_id, message_text: str):
    options = ["/help", "/tasks", "/reset"]

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=False, selective=True)
    for option in options:
        button = types.KeyboardButton(option)
        markup.add(button)

    bot.send_message(chat_id, message_text, reply_markup=markup)


try:
    students_info: Dict[str, Student] = manager.get_chat_info()
    bot.polling(none_stop=True, interval=0)

finally:
    manager.save_chat_info(students_info)
