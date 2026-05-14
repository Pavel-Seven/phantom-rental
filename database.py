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
    # Превращаем список строк в список словарей для фронтенда
    return [{"title": row[0], "url": row[1]} for row in rows]

def add_video(title, url):
    conn = sqlite3.connect('phantom.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO videos (title, url) VALUES (?, ?)', (title, url))
    conn.commit()
    conn.close()
