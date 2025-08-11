# main.py
import telebot
from config import TOKEN
import database.database as db

from handlers.users.commands import register_start_handlers
from handlers.admin.admins import register_admin_handlers
from handlers.users.text_handler import register_user_handlers

def main():
    db.init_db()
    bot = telebot.TeleBot(TOKEN)

    # register handlers
    register_start_handlers(bot)
    register_admin_handlers(bot)
    register_user_handlers(bot)

    print("Bot ishga tushdi...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
