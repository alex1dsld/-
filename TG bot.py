import io
import random
import requests
import numpy as np
import matplotlib.pyplot as plt
import telebot
from telebot import types

TELEGRAM_TOKEN = "7542966845:AAG_CPnIVPVIT4PrEeKvVABwqqa28mmxu8A"
OWM_API_KEY     = "e9938fb4f28c49a0a44ec92c44adc703"
CITY            = "Moscow"

STICKERS = [
    "CAACAgQAAxkBAAEOd-VoAnZ_UyVBKfP6Q8MDUEJdXCDA8gACgwADuMQfA0L-daGhD18cNgQ",
    "CAACAgIAAxkBAAEOd-doAnagWhW4TJFZ3E3z270oazsv5wACV0YAAmn2mEpt1Xo80t0aSTYE",
    "CAACAgEAAxkBAAEOd-loAna3NqSz59-0OnfUHyfFlzTbhAACKwIAAjbd2UeL36EJdj6f4jYE",
]

bot = telebot.TeleBot(TELEGRAM_TOKEN)
user_state = {}


@bot.message_handler(commands=['start'])
def start(message):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.row("Текущая погода")
    kb.row("Стикер")
    kb.row("График")
    bot.send_message(
        message.chat.id,
        "Выберите действие:",
        reply_markup=kb
    )

@bot.message_handler(regexp="^(Привет|привет)$")
def greet(message):
    bot.send_message(message.chat.id, "Привет, человек")

@bot.message_handler(func=lambda m: m.text == "Текущая погода")
def weather(message):
    url = (
        "http://api.openweathermap.org/data/2.5/weather"
        f"?q={CITY}&appid={OWM_API_KEY}&units=metric&lang=ru"
    )
    data = requests.get(url).json()
    if main := data.get("main"):
        temp = main["temp"]
        bot.send_message(message.chat.id, f"Сейчас в {CITY}: {temp:.1f}°C")
    else:
        bot.send_message(message.chat.id, "Не удалось получить погоду.")

@bot.message_handler(func=lambda m: m.text == "Стикер")
def sticker(message):
    bot.send_sticker(message.chat.id, random.choice(STICKERS))

@bot.message_handler(func=lambda m: m.text == "График")
def graph_start(message):
    bot.send_message(message.chat.id, "Введите коэффициенты k1, k2, k3 через пробел:")
    user_state[message.chat.id] = "WAIT_GRAPH"

@bot.message_handler(func=lambda m: user_state.get(m.chat.id) == "WAIT_GRAPH")
def graph_draw(message):
    parts = message.text.split()
    try:
        k1, k2, k3 = map(float, parts)
    except ValueError:
        bot.send_message(message.chat.id, "Формат неверный, введите три числа через пробел.")
        return

    x = np.linspace(0, 100, 500)
    y = k1 * x**2 + k2 * x + k3

    plt.figure()
    plt.plot(x, y)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"y = {k1}·x² + {k2}·x + {k3}")

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    bot.send_photo(message.chat.id, buf)
    buf.close()

    user_state.pop(message.chat.id, None)

if name == "main":
    bot.infinity_polling()
