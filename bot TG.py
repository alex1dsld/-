import telebot
from telebot import types

TOKEN = '7284942709:AAHt_jE7z1fHWJlWX99IIgQmBIzioN_HGWM'
bot = telebot.TeleBot(TOKEN)
tasks = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,
        "Привет! Я помогу тебе вести список задач. Используй команды:\n"
        "/addtask — добавить новую задачу\n"
        "/showtasks — показать список задач\n"
        "/deltask — удалить задачу"
    )

@bot.message_handler(commands=['addtask'])
def add_task(message):
    bot.send_message(message.chat.id, "Введите текст задачи:")
    bot.register_next_step_handler(message, process_add_task)

def process_add_task(message):
    user_id = message.from_user.id
    text = message.text.strip()
    if not text:
        bot.send_message(message.chat.id, "Текст задачи не может быть пустым. Попробуйте ещё раз.")
        return
    tasks.setdefault(user_id, []).append(text)
    bot.send_message(message.chat.id, "Задача добавлена!")

@bot.message_handler(commands=['showtasks'])
def show_tasks(message):
    user_id = message.from_user.id
    user_tasks = tasks.get(user_id)
    if not user_tasks:
        bot.send_message(message.chat.id, "Список задач пуст.")
        return
    response = 'Ваши задачи:'
    for idx, task in enumerate(user_tasks, start=1):
        response += f"\n{idx}. {task}"
    bot.send_message(message.chat.id, response)

@bot.message_handler(commands=['deltask'])
def delete_task(message):
    user_id = message.from_user.id
    user_tasks = tasks.get(user_id)
    if not user_tasks:
        bot.send_message(message.chat.id, "Нет задач для удаления.")
        return
    response = 'Выберите номер задачи для удаления:'
    for idx, task in enumerate(user_tasks, start=1):
        response += f"\n{idx}. {task}"
    bot.send_message(message.chat.id, response)
    bot.register_next_step_handler(message, process_delete_task)

def process_delete_task(message):
    user_id = message.from_user.id
    user_tasks = tasks.get(user_id)
    if not user_tasks:
        bot.send_message(message.chat.id, "Список задач пуст.")
        return
    try:
        index = int(message.text.strip()) - 1
        if index < 0 or index >= len(user_tasks):
            raise ValueError
    except ValueError:
        bot.send_message(message.chat.id, "Неверный номер задачи. Попробуйте ещё раз.")
        return
    removed = user_tasks.pop(index)
    bot.send_message(message.chat.id, f"Задача '{removed}' удалена.")
    if not user_tasks:
        tasks.pop(user_id, None)

if __name__ == '__main__':
    bot.infinity_polling()
