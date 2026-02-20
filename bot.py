import telebot
import os
from telebot import types

TOKEN = os.environ.get("TOKEN")
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
    bot.send_message(message.chat.id,
    "Для записи напишите нам:\n\n"
    "📱 WhatsApp: +33 6 xx xx xx xx\n"
    "📞 Телефон: +33 6 xx xx xx xx\n\n"
    "Или напишите сюда имя и желаемое время — мы свяжемся с вами!",
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
