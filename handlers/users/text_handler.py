# handlers/user.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import database.database as db

def register_user_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "📚 Janrlar")
    def show_genres(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "Hozircha janrlar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Janrni tanlang:", reply_markup=markup)

    @bot.message_handler(func=lambda m: db.get_genre_id_by_name(m.text) is not None)
    def show_books_by_genre(message):
        genre_name = message.text.strip()
        gid = db.get_genre_id_by_name(genre_name)
        if not gid:
            bot.send_message(message.chat.id, "Xatolik: janr topilmadi.")
            return
        books = db.get_books_by_genre(gid)
        if not books:
            bot.send_message(message.chat.id, "Bu janrda hali kitoblar yo'q.")
            return
        # show list with simple formatting
        lines = []
        for bid, title, author in books:
            if author:
                lines.append(f"• {title} — {author}")
            else:
                lines.append(f"• {title}")
        text = "\n".join(lines)
        bot.send_message(message.chat.id, text)
