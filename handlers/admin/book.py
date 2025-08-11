# handlers/book_handler.py
from config import ADMIN_ID
from database.database import get_genres, add_book, get_books_by_genre, get_book_details, delete_book_by_id, update_book

from keyboards.default import admin_book_menu, genres_menu, books_menu_for_genre, admin_genre_menu
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

def register_book_handlers(bot):

    @bot.message_handler(func=lambda m: m.text == "Kitoblar" and m.from_user.id == ADMIN_ID)
    def admin_books_menu(message):
        bot.send_message(
            message.chat.id,
            "Kitoblar bilan ishlash:",
            reply_markup=admin_book_menu()
        )

    # ===== Kitob qo'shish (janr tanlash kerak) =====
    @bot.message_handler(func=lambda m: m.text == "Kitob qo'shish" and m.from_user.id == ADMIN_ID)
    def choose_genre_for_book(message):
        rows = get_genres()

        if not rows:
            bot.send_message(
                message.chat.id,
                "❌ Hozir kitob qo'shish uchun janr yo'q.\nIltimos, avval janr qo'shing."
            )
            return

        bot.send_message(
            message.chat.id,
            "Qaysi janrga kitob qo'shasiz?",
            reply_markup=genres_menu()
        )

        bot.register_next_step_handler(message, ask_book_title)

    def ask_book_title(message):
        if message.from_user.id != ADMIN_ID:
            return

        selected_genre_id = None

        rows = get_genres()

        for g_id, g_name in rows:
            if g_name == message.text.strip():
                selected_genre_id = g_id
                break

        if not selected_genre_id:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return

        bot.send_message(message.chat.id, "Kitob nomini kiriting:")
        bot.register_next_step_handler(message, ask_book_description, selected_genre_id)

    def ask_book_description(message, genre_id):
        if message.from_user.id != ADMIN_ID:
            return

        title = message.text.strip()

        bot.send_message(message.chat.id, "Kitob tavsifini kiriting:")
        bot.register_next_step_handler(message, ask_book_image, genre_id, title)

    def ask_book_image(message, genre_id, title):
        if message.from_user.id != ADMIN_ID:
            return

        description = message.text.strip()

        bot.send_message(
            message.chat.id,
            "Kitob rasmini URL ko‘rinishida kiriting (yoki bo‘sh qoldiring):"
        )

        bot.register_next_step_handler(message, save_book_to_db, genre_id, title, description)

    def save_book_to_db(message, genre_id, title, description):
        if message.from_user.id != ADMIN_ID:
            return

        image_url = message.text.strip() if message.text.strip() else None

        try:
            add_book(title, description, image_url, genre_id)
            bot.send_message(
                message.chat.id,
                f"✅ Kitob '{title}' muvaffaqiyatli qo'shildi!",
                reply_markup=admin_book_menu()
            )
        except Exception:
            bot.send_message(
                message.chat.id,
                "❌ Kitob qo'shishda xatolik yuz berdi!",
                reply_markup=admin_book_menu()
            )

    # ===== Kitob o'chirish =====
    @bot.message_handler(func=lambda m: m.text == "Kitob o'chirish" and m.from_user.id == ADMIN_ID)
    def ask_genre_for_book_delete(message):
        rows = get_genres()

        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janr mavjud emas.")
            return

        bot.send_message(message.chat.id, "Qaysi janrdan kitob o'chirasiz?", reply_markup=genres_menu())
        bot.register_next_step_handler(message, show_books_for_delete)

    def show_books_for_delete(message):
        if message.from_user.id != ADMIN_ID:
            return

        chosen_genre_id = None

        rows = get_genres()

        for g_id, g_name in rows:
            if g_name == message.text.strip():
                chosen_genre_id = g_id
                break

        if not chosen_genre_id:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return

        books = get_books_by_genre(chosen_genre_id)

        if not books:
            bot.send_message(message.chat.id, "❌ Bu janrda kitoblar topilmadi.")
            return

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for b_id, title in books:
            # biz oson tanlash uchun faqat title ko'rsatamiz
            markup.add(KeyboardButton(title))

        markup.add(KeyboardButton("Orqaga"))

        bot.send_message(message.chat.id, "O'chiriladigan kitobni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, process_delete_book, chosen_genre_id)

    def process_delete_book(message, genre_id):
        if message.from_user.id != ADMIN_ID:
            return

        chosen_title = message.text.strip()
        found_book_id = None

        books = get_books_by_genre(genre_id)

        for b_id, title in books:
            if title == chosen_title:
                found_book_id = b_id
                break

        if not found_book_id:
            bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
            return

        delete_book_by_id(found_book_id)

        bot.send_message(
            message.chat.id,
            f"✅ Kitob '{chosen_title}' o'chirildi!",
            reply_markup=admin_book_menu()
        )

    # ===== Kitob o'zgartirish (soddalashtirilgan) =====
    @bot.message_handler(func=lambda m: m.text == "Kitob o'zgartirish" and m.from_user.id == ADMIN_ID)
    def ask_genre_for_book_edit(message):
        rows = get_genres()

        if not rows:
            bot.send_message(message.chat.id, "❌ Hozircha janr mavjud emas.")
            return

        bot.send_message(message.chat.id, "Qaysi janrdagi kitobni o'zgartirasiz?", reply_markup=genres_menu())
        bot.register_next_step_handler(message, show_books_for_edit)

    def show_books_for_edit(message):
        if message.from_user.id != ADMIN_ID:
            return

        chosen_genre_id = None

        rows = get_genres()

        for g_id, g_name in rows:
            if g_name == message.text.strip():
                chosen_genre_id = g_id
                break

        if not chosen_genre_id:
            bot.send_message(message.chat.id, "❌ Bunday janr topilmadi.")
            return

        books = get_books_by_genre(chosen_genre_id)

        if not books:
            bot.send_message(message.chat.id, "❌ Bu janrda kitoblar topilmadi.")
            return

        markup = ReplyKeyboardMarkup(resize_keyboard=True)

        for b_id, title in books:
            markup.add(KeyboardButton(title))

        markup.add(KeyboardButton("Orqaga"))

        bot.send_message(message.chat.id, "O'zgartiriladigan kitobni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, ask_which_field_to_edit, chosen_genre_id)

    def ask_which_field_to_edit(message, genre_id):
        if message.from_user.id != ADMIN_ID:
            return

        chosen_title = message.text.strip()
        chosen_book_id = None

        books = get_books_by_genre(genre_id)

        for b_id, title in books:
            if title == chosen_title:
                chosen_book_id = b_id
                break

        if not chosen_book_id:
            bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
            return

        # Soddalashtirilgan oqim: faqat title, description yoki image ni yangilash
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(KeyboardButton("Nomi"))
        markup.add(KeyboardButton("Tavsifi"))
        markup.add(KeyboardButton("Rasm URL"))
        markup.add(KeyboardButton("Orqaga"))

        bot.send_message(message.chat.id, "Qaysi maydonni o'zgartirasiz?", reply_markup=markup)
        bot.register_next_step_handler(message, process_field_choice, chosen_book_id)

    def process_field_choice(message, book_id):
        if message.from_user.id != ADMIN_ID:
            return

        choice = message.text.strip()

        if choice == "Nomi":
            bot.send_message(message.chat.id, "Yangi nomni kiriting:")
            bot.register_next_step_handler(message, save_new_title, book_id)
            return

        if choice == "Tavsifi":
            bot.send_message(message.chat.id, "Yangi tavsifni kiriting:")
            bot.register_next_step_handler(message, save_new_description, book_id)
            return

        if choice == "Rasm URL":
            bot.send_message(message.chat.id, "Yangi rasm URL ni kiriting (yoki bo'sh qoldiring):")
            bot.register_next_step_handler(message, save_new_image, book_id)
            return

        bot.send_message(message.chat.id, "Bekor qilindi.", reply_markup=admin_book_menu())

    def save_new_title(message, book_id):
        if message.from_user.id != ADMIN_ID:
            return

        new_title = message.text.strip()
        update_book(book_id, title=new_title)

        bot.send_message(
            message.chat.id,
            "✅ Kitob nomi yangilandi!",
            reply_markup=admin_book_menu()
        )

    def save_new_description(message, book_id):
        if message.from_user.id != ADMIN_ID:
            return

        new_desc = message.text.strip()
        update_book(book_id, description=new_desc)

        bot.send_message(
            message.chat.id,
            "✅ Kitob tavsifi yangilandi!",
            reply_markup=admin_book_menu()
        )

    def save_new_image(message, book_id):
        if message.from_user.id != ADMIN_ID:
            return

        new_image = message.text.strip() if message.text.strip() else None
        update_book(book_id, image_url=new_image)

        bot.send_message(
            message.chat.id,
            "✅ Kitob rasmi yangilandi!",
            reply_markup=admin_book_menu()
        )
