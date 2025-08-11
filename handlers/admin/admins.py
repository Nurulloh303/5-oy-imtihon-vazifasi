# handlers/admin.py
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import database.database as db
from config import ADMIN_ID

def register_admin_handlers(bot):

    # ADMIN main
    @bot.message_handler(func=lambda m: m.text == "🛠 Admin Buyruqlari" and m.from_user.id == ADMIN_ID)
    def admin_main(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("📂 Janrlar"), KeyboardButton("📖 Kitoblar"))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Admin menyusi:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "📂 Janrlar" and m.from_user.id == ADMIN_ID)
    def admin_genres_menu(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("➕ Janr qo'shish"))
        markup.add(KeyboardButton("➖ Janr o'chirish"))
        markup.add(KeyboardButton("✏️ Janr o'zgartirish"))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Janrlar bo'limi:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "➕ Janr qo'shish" and m.from_user.id == ADMIN_ID)
    def ask_add_genre(message):
        bot.send_message(message.chat.id, "Yangi janr nomini kiriting:")
        bot.register_next_step_handler(message, process_add_genre)

    def process_add_genre(message):
        name = message.text.strip()
        try:
            db.add_genre(name)
            bot.send_message(message.chat.id, f"✅ Janr qo'shildi: {name}")
        except Exception:
            bot.send_message(message.chat.id, "❌ Bu janr allaqachon mavjud yoki xatolik yuz berdi.")

    @bot.message_handler(func=lambda m: m.text == "➖ Janr o'chirish" and m.from_user.id == ADMIN_ID)
    def ask_delete_genre(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janrlar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "O'chiriladigan janrni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, process_delete_genre)

    def process_delete_genre(message):
        name = message.text.strip()
        gid = db.get_genre_id_by_name(name)
        if not gid:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return
        db.delete_genre_by_id(gid)
        bot.send_message(message.chat.id, f"✅ Janr o'chirildi: {name}")

    @bot.message_handler(func=lambda m: m.text == "✏️ Janr o'zgartirish" and m.from_user.id == ADMIN_ID)
    def ask_edit_genre(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janrlar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "O'zgartiriladigan janrni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, process_edit_genre_choose)

    def process_edit_genre_choose(message):
        old_name = message.text.strip()
        gid = db.get_genre_id_by_name(old_name)
        if not gid:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return
        bot.send_message(message.chat.id, "Yangi nomni kiriting:")
        bot.register_next_step_handler(message, process_save_genre_name, gid)

    def process_save_genre_name(message, gid):
        new_name = message.text.strip()
        try:
            db.update_genre_name(gid, new_name)
            bot.send_message(message.chat.id, f"✅ Janr nomi yangilandi: {new_name}")
        except Exception:
            bot.send_message(message.chat.id, "❌ Yangilashda xatolik yuz berdi.")

    @bot.message_handler(func=lambda m: m.text == "📖 Kitoblar" and m.from_user.id == ADMIN_ID)
    def admin_books_menu(message):
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("➕ Kitob qo'shish"))
        markup.add(KeyboardButton("➖ Kitob o'chirish"))
        markup.add(KeyboardButton("✏️ Kitob o'zgartirish"))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Kitoblar bo'limi:", reply_markup=markup)

    @bot.message_handler(func=lambda m: m.text == "➕ Kitob qo'shish" and m.from_user.id == ADMIN_ID)
    def ask_genre_for_new_book(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "❌ Kitob qo'shish uchun janrlar yo'q. Avval janr qo'shing.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Qaysi janrga kitob qo'shasiz?", reply_markup=markup)
        bot.register_next_step_handler(message, process_new_book_genre)

    def process_new_book_genre(message):
        genre_name = message.text.strip()
        gid = db.get_genre_id_by_name(genre_name)
        if not gid:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return
        bot.send_message(message.chat.id, "Kitob nomini kiriting:")
        bot.register_next_step_handler(message, process_new_book_title, gid)

    def process_new_book_title(message, gid):
        title = message.text.strip()
        bot.send_message(message.chat.id, "Muallifni kiriting:")
        bot.register_next_step_handler(message, process_new_book_author, gid, title)

    def process_new_book_author(message, gid, title):
        author = message.text.strip()
        bot.send_message(message.chat.id, "Qisqacha tavsifni kiriting (yoki bo'sh qoldiring):")
        bot.register_next_step_handler(message, process_new_book_description, gid, title, author)

    def process_new_book_description(message, gid, title, author):
        description = message.text.strip() if message.text else None
        bot.send_message(message.chat.id, "Rasm URL kiriting (yoki bo'sh qoldiring):")
        bot.register_next_step_handler(message, process_new_book_image, gid, title, author, description)

    def process_new_book_image(message, gid, title, author, description):
        image_url = message.text.strip() if message.text else None
        try:
            db.add_book(title, author, description, image_url, gid)
            bot.send_message(message.chat.id, f"✅ Kitob qo'shildi: {title} — {author}")
        except Exception:
            bot.send_message(message.chat.id, "❌ Kitob qo'shishda xatolik yuz berdi.")

    @bot.message_handler(func=lambda m: m.text == "➖ Kitob o'chirish" and m.from_user.id == ADMIN_ID)
    def ask_genre_for_delete_book(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janrlar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Qaysi janrdan kitob o'chirasiz?", reply_markup=markup)
        bot.register_next_step_handler(message, process_delete_book_show)

    def process_delete_book_show(message):
        genre_name = message.text.strip()
        gid = db.get_genre_id_by_name(genre_name)
        if not gid:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return
        books = db.get_books_by_genre(gid)
        if not books:
            bot.send_message(message.chat.id, "❌ Bu janrda kitoblar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for bid, title, author in books:
            markup.add(KeyboardButton(title))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "O'chiriladigan kitobni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, process_delete_book_confirm, gid)

    def process_delete_book_confirm(message, gid):
        title = message.text.strip()
        book = db.get_book_by_title_and_genre(title, gid)
        if not book:
            bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
            return
        bid = book[0]
        db.delete_book_by_id(bid)
        bot.send_message(message.chat.id, f"✅ Kitob o'chirildi: {title}")

    @bot.message_handler(func=lambda m: m.text == "✏️ Kitob o'zgartirish" and m.from_user.id == ADMIN_ID)
    def ask_genre_for_edit_book(message):
        rows = db.get_all_genres()
        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janrlar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for gid, name in rows:
            markup.add(KeyboardButton(name))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Qaysi janrdagi kitobni o'zgartirasiz?", reply_markup=markup)
        bot.register_next_step_handler(message, process_edit_book_show)

    def process_edit_book_show(message):
        genre_name = message.text.strip()
        gid = db.get_genre_id_by_name(genre_name)
        if not gid:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return
        books = db.get_books_by_genre(gid)
        if not books:
            bot.send_message(message.chat.id, "❌ Bu janrda kitoblar yo'q.")
            return
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        for bid, title, author in books:
            markup.add(KeyboardButton(title))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "O'zgartiriladigan kitobni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, process_edit_book_choose, gid)

    def process_edit_book_choose(message, gid):
        title = message.text.strip()
        book = db.get_book_by_title_and_genre(title, gid)
        if not book:
            bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
            return
        bid = book[0]
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Nomi"), KeyboardButton("Muallif"), KeyboardButton("Tavsifi"), KeyboardButton("Rasm URL"))
        markup.add(KeyboardButton("⬅️ Orqaga"))
        bot.send_message(message.chat.id, "Qaysi maydonni o'zgartirasiz?", reply_markup=markup)
        bot.register_next_step_handler(message, process_edit_field_choice, bid)

    def process_edit_field_choice(message, bid):
        choice = message.text.strip()
        if choice == "Nomi":
            bot.send_message(message.chat.id, "Yangi nomni kiriting:")
            bot.register_next_step_handler(message, process_save_new_title, bid)
            return
        if choice == "Muallif":
            bot.send_message(message.chat.id, "Yangi muallifni kiriting:")
            bot.register_next_step_handler(message, process_save_new_author, bid)
            return
        if choice == "Tavsifi":
            bot.send_message(message.chat.id, "Yangi tavsifni kiriting:")
            bot.register_next_step_handler(message, process_save_new_description, bid)
            return
        if choice == "Rasm URL":
            bot.send_message(message.chat.id, "Yangi rasm URLni kiriting (yoki bo'sh qoldiring):")
            bot.register_next_step_handler(message, process_save_new_image, bid)
            return
        bot.send_message(message.chat.id, "Bekor qilindi.")

    def process_save_new_title(message, bid):
        new_title = message.text.strip()
        db.update_book(bid, title=new_title)
        bot.send_message(message.chat.id, "✅ Kitob nomi yangilandi!")

    def process_save_new_author(message, bid):
        new_author = message.text.strip()
        db.update_book(bid, author=new_author)
        bot.send_message(message.chat.id, "✅ Kitob muallifi yangilandi!")

    def process_save_new_description(message, bid):
        new_desc = message.text.strip()
        db.update_book(bid, description=new_desc)
        bot.send_message(message.chat.id, "✅ Kitob tavsifi yangilandi!")

    def process_save_new_image(message, bid):
        new_image = message.text.strip() if message.text else None
        db.update_book(bid, image_url=new_image)
        bot.send_message(message.chat.id, "✅ Kitob rasmi yangilandi!")
