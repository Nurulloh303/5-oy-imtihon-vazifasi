# handlers/start.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from config import ADMIN_ID

def register_start_handlers(bot):
    @bot.message_handler(commands=["start"])
    def start(message):
        is_admin = (message.from_user.id == ADMIN_ID)
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("📚 Janrlar"))
        if is_admin:
            markup.add(KeyboardButton("🛠 Admin Buyruqlari"))
        bot.send_message(message.chat.id, "Salom! Kutubxonamizga xush kelibsiz.", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "⬅️ Orqaga")
    def back_to_main(message):
        start(message)
