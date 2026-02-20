import telebot
import os
from telebot import types

TOKEN = os.environ.get("TOKEN")
OWNER_ID = 7415299809
bot = telebot.TeleBot(TOKEN)

def main_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("💅 Услуги"))
    markup.add(types.KeyboardButton("💰 Цены"))
    markup.add(types.KeyboardButton("📅 Записаться"))
    markup.add(types.KeyboardButton("📍 Адрес и часы"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id,
    "Привет! Я бот салона красоты 💅\n\nВыбери что тебя интересует:",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "💅 Услуги")
def services(message):
    bot.send_message(message.chat.id,
    "Наши услуги:\n\n"
    "💇 Стрижка и укладка\n"
    "💅 Маникюр и педикюр\n"
    "🎨 Окрашивание\n"
    "✨ Уход за кожей",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "💰 Цены")
def prices(message):
    bot.send_message(message.chat.id,
    "Наши цены:\n\n"
    "Стрижка — от 30€\n"
    "Маникюр — от 25€\n"
    "Окрашивание — от 60€\n"
    "Уход за кожей — от 45€",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📅 Записаться")
def book(message):
    msg = bot.send_message(message.chat.id,
    "Напишите ваше имя и желаемое время.\n\n"
    "Например: Анна, пятница 15:00",
    reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, process_booking)

def process_booking(message):
    client_name = message.from_user.first_name
    client_username = f"@{message.from_user.username}" if message.from_user.username else "без username"
    booking_text = message.text

    # Уведомление владельцу
    bot.send_message(OWNER_ID,
    f"🔔 Новая запись!\n\n"
    f"👤 Клиент: {client_name} ({client_username})\n"
    f"📝 Запрос: {booking_text}")

    # Ответ клиенту
    bot.send_message(message.chat.id,
    "Спасибо! Ваша заявка принята ✅\n\n"
    "Мы свяжемся с вами в ближайшее время для подтверждения.",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: message.text == "📍 Адрес и часы")
def address(message):
    bot.send_message(message.chat.id,
    "📍 123 Rue de la Paix, Paris\n\n"
    "Часы работы:\n"
    "Пн-Пт: 9:00 - 19:00\n"
    "Сб: 10:00 - 17:00\n"
    "Вс: выходной",
    reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.send_message(message.chat.id,
    "Нажми кнопку в меню 😊",
    reply_markup=main_menu())

print("Бот запущен...")
bot.polling()