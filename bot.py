import telebot

TOKEN = "7975548569:AAF5fZCH4pRkg-35CHkAPsNxAbBwFJVreyc"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, 
    "Привет! Я бот салона красоты 💅\n\n"
    "Выбери что тебя интересует:\n"
    "/services - Наши услуги\n"
    "/prices - Цены\n"
    "/book - Записаться\n"
    "/address - Адрес и часы работы")

@bot.message_handler(commands=['services'])
def services(message):
    bot.reply_to(message,
    "Наши услуги:\n\n"
    "💇 Стрижка и укладка\n"
    "💅 Маникюр и педикюр\n"
    "🎨 Окрашивание\n"
    "✨ Уход за кожей\n\n"
    "Для записи напиши /book")

@bot.message_handler(commands=['prices'])
def prices(message):
    bot.reply_to(message,
    "Наши цены:\n\n"
    "Стрижка — от 30€\n"
    "Маникюр — от 25€\n"
    "Окрашивание — от 60€\n"
    "Уход за кожей — от 45€")

@bot.message_handler(commands=['book'])
def book(message):
    bot.reply_to(message,
    "Для записи напишите нам напрямую:\n\n"
    "📱 WhatsApp: +33 6 xx xx xx xx\n"
    "📞 Телефон: +33 6 xx xx xx xx\n\n"
    "Или напишите сюда имя и желаемое время — мы свяжемся с вами!")

@bot.message_handler(commands=['address'])
def address(message):
    bot.reply_to(message,
    "Мы находимся по адресу:\n\n"
    "📍 123 Rue de la Paix, Paris\n\n"
    "Часы работы:\n"
    "Пн-Пт: 9:00 - 19:00\n"
    "Сб: 10:00 - 17:00\n"
    "Вс: выходной")

@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, 
    "Я не понимаю эту команду 😊\n"
    "Напиши /start чтобы увидеть меню")

print("Бот запущен...")
bot.polling()