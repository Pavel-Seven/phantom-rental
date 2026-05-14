import sqlite3

def init_db():
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    # Создаем таблицу для видео
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    # Создаем таблицу для заявок (лидов)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact TEXT NOT NULL,
            date TEXT,
            comments TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    # Добавим тестовые данные, если таблица пустая
    cursor.execute('SELECT COUNT(*) FROM videos')
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO videos (title, url) VALUES (?, ?)', ("Phantom Flex 4K Gold", "video1.mp4"))
        cursor.execute('INSERT INTO videos (title, url) VALUES (?, ?)', ("Highspeed Motion", "video2.mp4"))
    
    conn.commit()
    conn.close()

def get_videos():
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT title, url FROM videos')
    rows = cursor.fetchall()
    conn.close()
    return [{"title": row[0], "url": row[1]} for row in rows]

def add_video(title, url):
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO videos (title, url) VALUES (?, ?)', (title, url))
    conn.commit()
    conn.close()

def add_order(name, contact, date, comments):
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO orders (name, contact, date, comments) VALUES (?, ?, ?, ?)', (name, contact, date, comments))
    conn.commit()
    conn.close()

def get_orders():
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, contact, date, comments, created_at FROM orders ORDER BY created_at DESC')
    rows = cursor.fetchall()
    conn.close()
    return [{"id": r[0], "name": r[1], "contact": r[2], "date": r[3], "comments": r[4], "created_at": r[5]} for r in rows]
