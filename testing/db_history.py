import sqlite3
from datetime import datetime

class DBHistory:
    
    def __init__(self, database: str):
        self.connection = sqlite3.connect(database="db/DataBase.db")
        self.cursor = self.connection.cursor()
        
    def save_db_history(self, username: str, role: str, content: str, limit=5):
        """Функция для сохранения сообщения с ограничением"""
        with self.connection:
            # Проверяем количество записей для данного пользователя и роли
            query = """ SELECT COUNT(*) FROM chat_history 
            WHERE username = ? AND role = ? """
            self.cursor.execute(query, (username, role))
            count = self.cursor.fetchone()[0]
            
            # Если записей больше лимита, удаляем самые старые
            if count >= limit:
                query = """ DELETE FROM chat_history 
                WHERE username = ? AND role = ? AND timestamp IN (
                SELECT timestamp FROM chat_history WHERE username = ? AND role = ? ORDER BY timestamp LIMIT ?
                ) """
                self.connection.execute(query, (username, role, username, role, count - limit + 1))
                self.connection.commit()
                
            # Добавляем новую запись
            query = """ INSERT INTO chat_history (username, role, content) VALUES (?, ?, ?)"""
            self.cursor.execute(query, (username, role, content))
            self.connection.commit()        
            
            
    def load_db_history(self, username: str):
        """Функция для загрузки истории"""
        with self.connection:
            query = """ SELECT role, content FROM chat_history 
            WHERE username = ? 
            ORDER BY timestamp 
            DESC LIMIT ? """
            self.cursor.execute(query, (username, 5))
            self.connection.commit()
        return [{"role": row[0], "content": row[1]} for row in self.cursor.fetchall()]


    def clear_db_history(self, username: str):
        """Функция для очистки истории"""
        with self.connection:
            query = "DELETE FROM chat_history WHERE username = ?"
            self.cursor.execute(query, (username, ))
            self.connection.commit()
            
            

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