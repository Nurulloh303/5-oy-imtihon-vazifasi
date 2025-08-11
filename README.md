# 📚 Telegram Kutubxona Boti

Bu Telegram bot foydalanuvchilarga janrlar bo‘yicha kitoblarni ko‘rish, qidirish va adminlarga yangi janr hamda kitoblarni qo‘shish, o‘chirish, o‘zgartirish imkonini beradi.  
Bot SQLite ma’lumotlar bazasidan foydalanadi va barcha boshqaruvlar tugmalar orqali amalga oshiriladi.

## ✨ Funksiyalar

### 👤 Foydalanuvchilar uchun:
- 📖 **Janrlar ro‘yxatini ko‘rish** — mavjud barcha janrlarni chiqaradi.
- 📚 **Tanlangan janrdagi kitoblarni ko‘rish** — janr tugmasini bosganda shu janrga tegishli kitoblar chiqadi.
- 🔍 **Kitob nomi bo‘yicha qidirish** — istalgan kitobni tez topish imkoniyati.

### 🛡 Adminlar uchun:
- 📂 **Janrlar bo‘limi**
  - ➕ Janr qo‘shish
  - ✏ Janr nomini o‘zgartirish
  - 🗑 Janrni o‘chirish
- 📂 **Kitoblar bo‘limi**
  - ➕ Kitob qo‘shish (oldin janr bo‘lishi shart)
  - ✏ Kitob ma’lumotlarini o‘zgartirish
  - 🗑 Kitobni o‘chirish

⚠️ **Admin bo‘lish** uchun `config.py` ichida `ADMIN_ID` ga o‘z Telegram ID’ingizni kiriting.

---

## 🛠 Texnologiyalar
- Python 3
- [PyTelegramBotAPI](https://pypi.org/project/pyTelegramBotAPI/)
- SQLite (ma’lumotlar bazasi)
- Telebot Inline va Reply Keyboard tugmalari

---

Ism: [Nurulloh]
Telegram: [@nurulloh_303]
GitHub: [Nurulloh303]
Bot telegram linki: [@janrlar_bot]
