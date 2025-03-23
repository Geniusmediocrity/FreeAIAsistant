import sqlite3
from datetime import datetime


def save_db_history(username: str, role: str, content: str, limit=5):
    """Функция для сохранения сообщения с ограничением"""
    with sqlite3.connect(database="db/DataBase.db") as db:
        # Проверяем количество записей для данного пользователя и роли
        cursor = db.cursor()
        query = """ SELECT COUNT(*) FROM chat_history 
        WHERE username = ? AND role = ? """
        cursor.execute(query, (username, role))
        count = cursor.fetchone()[0]
        
        # Если записей больше лимита, удаляем самые старые
        if count >= limit:
            query = """ DELETE FROM chat_history 
            WHERE username = ? AND role = ? AND timestamp IN (
            SELECT timestamp FROM chat_history WHERE username = ? AND role = ? ORDER BY timestamp LIMIT ?
            ) """
            db.execute(query, (username, role, username, role, count - limit + 1))
            db.commit()
            
        # Добавляем новую запись
        query = """ INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)"""
        cursor.execute(query, (username, role, content))
        db.commit()        
        
        
def load_db_history(username: str):
    """Функция для загрузки истории"""
    with sqlite3.connect(database="db/DataBase.db") as db:
        cursor = db.cursor()
        query = """ SELECT role, content FROM chat_history 
        WHERE username = ? 
        ORDER BY timestamp 
        DESC LIMIT ? """
        cursor.execute(query, (username, 5))
        db.commit()
    return [{"role": row[0], "content": row[1]} for row in cursor.fetchall()]


def clear_db_history(username: str):
    """Функция для очистки истории"""
    with sqlite3.connect(database="db/DataBase.db") as db:
        cursor = db.cursor()
        query = "DELETE FROM chat_history WHERE username = ?"
        cursor.execute(query, (username, ))
        db.commit()
        
        

# with sqlite3.connect("db/DataBase.db") as db:
#     cursor = db.cursor()
#     query = '''
# CREATE TABLE IF NOT EXISTS chat_history(
# username TEXT NOT NULL,
# role TEXT NOT NULL,
# content TEXT NOT NULL,
# timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
# )
# '''
#     cursor.execute(query)