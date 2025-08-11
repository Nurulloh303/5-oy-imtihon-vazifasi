from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from database.database import get_genres

def main_menu(is_admin=False):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("Janrlar"))

    if is_admin:
        markup.add(KeyboardButton("Admin Buyruqlari"))

    return markup


def admin_main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("Janrlar"))
    markup.add(KeyboardButton("Kitoblar"))
    markup.add(KeyboardButton("Orqaga"))

    return markup


def admin_genre_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("Janr qo'shish"))
    markup.add(KeyboardButton("Janr o'chirish"))
    markup.add(KeyboardButton("Janr o'zgartirish"))
    markup.add(KeyboardButton("Orqaga"))

    return markup


def admin_book_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add(KeyboardButton("Kitob qo'shish"))
    markup.add(KeyboardButton("Kitob o'chirish"))
    markup.add(KeyboardButton("Kitob o'zgartirish"))
    markup.add(KeyboardButton("Orqaga"))

    return markup


def genres_menu():
    rows = get_genres()
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for _id, name in rows:
        markup.add(KeyboardButton(name))

    markup.add(KeyboardButton("Orqaga"))

    return markup


def books_menu_for_genre(genre_id):
    from database import get_books_by_genre

    rows = get_books_by_genre(genre_id)
    markup = ReplyKeyboardMarkup(resize_keyboard=True)

    for book_id, title in rows:
        display = title
        markup.add(KeyboardButton(display))

    markup.add(KeyboardButton("Orqaga"))
    return markup
