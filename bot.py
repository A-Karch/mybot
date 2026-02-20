import telebot
import os
from telebot import types

TOKEN = os.environ.get("TOKEN")
OWNER_ID = 7415299809
bot = telebot.TeleBot(TOKEN)

# Данные салона
SERVICES = {
    "💇 Стрижка": 30,
    "💅 Маникюр": 25,
    "🎨 Окрашивание": 60,
    "✨ Уход за кожей": 45
}

MASTERS = ["👩 Анна", "👩 Мария", "👩 София"]

TIMES = ["10:00", "11:00", "12:00", "13:00", "14:00", "15:00", "16:00", "17:00", "18:00"]

# Хранилище данных пользователя во время записи
user_data = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📅 Записаться"))
    markup.add(types.KeyboardButton("💰 Цены"), types.KeyboardButton("📍 Адрес и часы"))
    return markup

# СТАРТ
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
    "Привет! Добро пожаловать в салон красоты Beauty 💅\n\n"
    "Я помогу вам записаться к мастеру быстро и удобно.",
    reply_markup=main_menu())

# ЦЕНЫ
@bot.message_handler(func=lambda message: message.text == "💰 Цены")
def prices(message):
    text = "Наши цены:\n\n"
    for service, price in SERVICES.items():
        text += f"{service} — от {price}€\n"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

# АДРЕС
@bot.message_handler(func=lambda message: message.text == "📍 Адрес и часы")
def address(message):
    bot.send_message(message.chat.id,
    "📍 123 Rue de la Paix, Paris\n\n"
    "Часы работы:\n"
    "Пн-Пт: 9:00 - 19:00\n"
    "Сб: 10:00 - 17:00\n"
    "Вс: выходной",
    reply_markup=main_menu())

# ШАГ 1 — ВЫБОР УСЛУГИ
@bot.message_handler(func=lambda message: message.text == "📅 Записаться")
def choose_service(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for service in SERVICES:
        markup.add(types.KeyboardButton(service))
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите услугу:", reply_markup=markup)
    bot.register_next_step_handler(message, process_service)

def process_service(message):
    if message.text == "🔙 Назад":
        send_welcome(message)
        return
    if message.text not in SERVICES:
        bot.send_message(message.chat.id, "Пожалуйста выберите услугу из меню")
        bot.register_next_step_handler(message, process_service)
        return
    user_data[message.chat.id] = {"service": message.text}
    choose_master(message)

# ШАГ 2 — ВЫБОР МАСТЕРА
def choose_master(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for master in MASTERS:
        markup.add(types.KeyboardButton(master))
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите мастера:", reply_markup=markup)
    bot.register_next_step_handler(message, process_master)

def process_master(message):
    if message.text == "🔙 Назад":
        choose_service(message)
        return
    if message.text not in MASTERS:
        bot.send_message(message.chat.id, "Пожалуйста выберите мастера из меню")
        bot.register_next_step_handler(message, process_master)
        return
    user_data[message.chat.id]["master"] = message.text
    choose_time(message)

# ШАГ 3 — ВЫБОР ВРЕМЕНИ
def choose_time(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for time in TIMES:
        row.append(types.KeyboardButton(time))
        if len(row) == 3:
            markup.add(*row)
            row = []
    if row:
        markup.add(*row)
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите удобное время:", reply_markup=markup)
    bot.register_next_step_handler(message, process_time)

def process_time(message):
    if message.text == "🔙 Назад":
        choose_master(message)
        return
    if message.text not in TIMES:
        bot.send_message(message.chat.id, "Пожалуйста выберите время из меню")
        bot.register_next_step_handler(message, process_time)
        return
    user_data[message.chat.id]["time"] = message.text
    confirm_booking(message)

# ШАГ 4 — ПОДТВЕРЖДЕНИЕ
def confirm_booking(message):
    data = user_data[message.chat.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("✅ Подтвердить"))
    markup.add(types.KeyboardButton("🔙 Назад"))

    price = SERVICES[data["service"]]
    text = (
        f"Проверьте вашу запись:\n\n"
        f"💅 Услуга: {data['service']}\n"
        f"👩 Мастер: {data['master']}\n"
        f"🕐 Время: {data['time']}\n"
        f"💰 Стоимость: от {price}€\n\n"
        f"Всё верно?"
    )
    bot.send_message(message.chat.id, text, reply_markup=markup)
    bot.register_next_step_handler(message, process_confirm)

def process_confirm(message):
    if message.text == "🔙 Назад":
        choose_time(message)
        return
    if message.text != "✅ Подтвердить":
        bot.register_next_step_handler(message, process_confirm)
        return

    data = user_data[message.chat.id]
    client_name = message.from_user.first_name
    client_username = f"@{message.from_user.username}" if message.from_user.username else "без username"

    # Уведомление владельцу
    bot.send_message(OWNER_ID,
    f"🔔 Новая запись!\n\n"
    f"👤 Клиент: {client_name} ({client_username})\n"
    f"💅 Услуга: {data['service']}\n"
    f"👩 Мастер: {data['master']}\n"
    f"🕐 Время: {data['time']}\n"
    f"💰 Стоимость: от {SERVICES[data['service']]}€")

    # Ответ клиенту
    bot.send_message(message.chat.id,
    "✅ Ваша запись принята!\n\n"
    f"💅 Услуга: {data['service']}\n"
    f"👩 Мастер: {data['master']}\n"
    f"🕐 Время: {data['time']}\n\n"
    "Мы пришлём напоминание за день до визита. До встречи! 💅",
    reply_markup=main_menu())

    # Очищаем данные
    user_data.pop(message.chat.id, None)

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id,
    "Нажми кнопку в меню 😊",
    reply_markup=main_menu())

print("Бот запущен...")
bot.polling()
