# database.py
import sqlite3
from uuid import uuid4
from config import DB_NAME

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS genres (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT,
            description TEXT,
            image_url TEXT,
            genre_id TEXT,
            FOREIGN KEY (genre_id) REFERENCES genres(id)
        )
    """)
    conn.commit()

def add_genre(name):
    gid = str(uuid4())
    cursor.execute("INSERT INTO genres (id, name) VALUES (?, ?)", (gid, name))
    conn.commit()
    return gid

def get_all_genres():
    cursor.execute("SELECT id, name FROM genres ORDER BY name")
    return cursor.fetchall()

def get_genre_id_by_name(name):
    cursor.execute("SELECT id FROM genres WHERE name = ?", (name,))
    row = cursor.fetchone()
    return row[0] if row else None

def delete_genre_by_id(genre_id):
    # delete books in genre first (cascade-like behaviour)
    cursor.execute("DELETE FROM books WHERE genre_id = ?", (genre_id,))
    cursor.execute("DELETE FROM genres WHERE id = ?", (genre_id,))
    conn.commit()

def update_genre_name(genre_id, new_name):
    cursor.execute("UPDATE genres SET name = ? WHERE id = ?", (new_name, genre_id))
    conn.commit()

def add_book(title, author, description, image_url, genre_id):
    bid = str(uuid4())
    cursor.execute("""
        INSERT INTO books (id, title, author, description, image_url, genre_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (bid, title, author, description, image_url, genre_id))
    conn.commit()
    return bid

def get_books_by_genre(genre_id):
    cursor.execute("SELECT id, title, author FROM books WHERE genre_id = ? ORDER BY title", (genre_id,))
    return cursor.fetchall()

def get_book_by_id(book_id):
    cursor.execute("SELECT id, title, author, description, image_url, genre_id FROM books WHERE id = ?", (book_id,))
    return cursor.fetchone()

def get_book_by_title_and_genre(title, genre_id):
    cursor.execute("SELECT id, title FROM books WHERE title = ? AND genre_id = ?", (title, genre_id))
    return cursor.fetchone()

def delete_book_by_id(book_id):
    cursor.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()

def update_book(book_id, title=None, author=None, description=None, image_url=None, genre_id=None):
    fields = []
    params = []
    if title is not None:
        fields.append("title = ?")
        params.append(title)
    if author is not None:
        fields.append("author = ?")
        params.append(author)
    if description is not None:
        fields.append("description = ?")
        params.append(description)
    if image_url is not None:
        fields.append("image_url = ?")
        params.append(image_url)
    if genre_id is not None:
        fields.append("genre_id = ?")
        params.append(genre_id)
    if not fields:
        return
    params.append(book_id)
    sql = "UPDATE books SET " + ", ".join(fields) + " WHERE id = ?"
    cursor.execute(sql, tuple(params))
    conn.commit()
