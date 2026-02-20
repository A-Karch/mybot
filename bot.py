import telebot
import os
from telebot import types
from database import get_available_times, add_booking, confirm_booking, get_booking, get_next_7_days

TOKEN = os.environ.get("TOKEN")
OWNER_ID = 7415299809
bot = telebot.TeleBot(TOKEN)

SERVICES = {
    "💇 Стрижка": 30,
    "💅 Маникюр": 25,
    "🎨 Окрашивание": 60,
    "✨ Уход за кожей": 45
}

MASTERS = ["👩 Анна", "👩 Мария", "👩 София"]

user_data = {}

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📅 Записаться"))
    markup.add(types.KeyboardButton("💰 Цены"), types.KeyboardButton("📍 Адрес и часы"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
    "Привет! Добро пожаловать в салон красоты Beauty 💅\n\n"
    "Я помогу вам записаться к мастеру быстро и удобно.",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "💰 Цены")
def prices(message):
    text = "Наши цены:\n\n"
    for service, price in SERVICES.items():
        text += f"{service} — от {price}€\n"
    bot.send_message(message.chat.id, text, reply_markup=main_menu())

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
    choose_date(message)

# ШАГ 3 — ВЫБОР ДАТЫ
def choose_date(message):
    days = get_next_7_days()
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for day in days:
        row.append(types.KeyboardButton(day))
        if len(row) == 2:
            markup.add(*row)
            row = []
    if row:
        markup.add(*row)
    markup.add(types.KeyboardButton("🔙 Назад"))
    bot.send_message(message.chat.id, "Выберите дату:", reply_markup=markup)
    bot.register_next_step_handler(message, process_date)

def process_date(message):
    if message.text == "🔙 Назад":
        choose_master(message)
        return
    days = get_next_7_days()
    if message.text not in days:
        bot.send_message(message.chat.id, "Пожалуйста выберите дату из меню")
        bot.register_next_step_handler(message, process_date)
        return
    user_data[message.chat.id]["date"] = message.text
    choose_time(message)

# ШАГ 4 — ВЫБОР ВРЕМЕНИ
def choose_time(message):
    data = user_data[message.chat.id]
    available = get_available_times(data["master"], data["date"])

    if not available:
        bot.send_message(message.chat.id,
        "😔 К сожалению на эту дату у выбранного мастера нет свободного времени.\n\n"
        "Выберите другую дату.")
        choose_date(message)
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    row = []
    for time in available:
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
        choose_date(message)
        return
    data = user_data[message.chat.id]
    available = get_available_times(data["master"], data["date"])
    if message.text not in available:
        bot.send_message(message.chat.id, "Пожалуйста выберите время из меню")
        bot.register_next_step_handler(message, process_time)
        return
    user_data[message.chat.id]["time"] = message.text
    confirm_booking_step(message)

# ШАГ 5 — ПОДТВЕРЖДЕНИЕ
def confirm_booking_step(message):
    data = user_data[message.chat.id]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("✅ Подтвердить"))
    markup.add(types.KeyboardButton("🔙 Назад"))
    price = SERVICES[data["service"]]
    text = (
        f"Проверьте вашу запись:\n\n"
        f"💅 Услуга: {data['service']}\n"
        f"👩 Мастер: {data['master']}\n"
        f"📅 Дата: {data['date']}\n"
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

    booking_id = add_booking(
        message.chat.id, client_name, client_username,
        data["service"], data["master"], data["date"], data["time"]
    )

    # Уведомление владельцу с кнопками подтверждения
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("✅ Подтвердить", callback_data=f"confirm_{booking_id}"),
        types.InlineKeyboardButton("❌ Отменить", callback_data=f"cancel_{booking_id}")
    )

    bot.send_message(OWNER_ID,
    f"🔔 Новая запись №{booking_id}!\n\n"
    f"👤 Клиент: {client_name} ({client_username})\n"
    f"💅 Услуга: {data['service']}\n"
    f"👩 Мастер: {data['master']}\n"
    f"📅 Дата: {data['date']}\n"
    f"🕐 Время: {data['time']}\n"
    f"💰 Стоимость: от {SERVICES[data['service']]}€",
    reply_markup=markup)

    bot.send_message(message.chat.id,
    "⏳ Ваша заявка отправлена!\n\n"
    "Ожидайте подтверждения от салона. Мы свяжемся с вами в ближайшее время. 💅",
    reply_markup=main_menu())

    user_data.pop(message.chat.id, None)

# ВЛАДЕЛЕЦ ПОДТВЕРЖДАЕТ ИЛИ ОТМЕНЯЕТ
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    action, booking_id = call.data.split("_")
    booking_id = int(booking_id)
    booking = get_booking(booking_id)

    if not booking:
        bot.answer_callback_query(call.id, "Запись не найдена")
        return

    client_id = booking[1]

    if action == "confirm":
        confirm_booking(booking_id)
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"✅ Запись №{booking_id} подтверждена")
        bot.send_message(client_id,
        f"✅ Ваша запись подтверждена!\n\n"
        f"💅 Услуга: {booking[4]}\n"
        f"👩 Мастер: {booking[5]}\n"
        f"📅 Дата: {booking[6]}\n"
        f"🕐 Время: {booking[7]}\n\n"
        "Ждём вас! До встречи 💅")

    elif action == "cancel":
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
        bot.send_message(call.message.chat.id, f"❌ Запись №{booking_id} отменена")
        bot.send_message(client_id,
        "😔 К сожалению ваша запись была отменена.\n\n"
        "Пожалуйста запишитесь на другое время.")

    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id, "Нажми кнопку в меню 😊", reply_markup=main_menu())

print("Бот запущен...")
bot.polling()
