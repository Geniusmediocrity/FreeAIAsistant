from .PgDB_connect import DataBaseConnect



class HistoryTable(DataBaseConnect):
    """Работа с историей запросов"""
    
    def __init__(self):
        # TODO self.__create_chat_history()
        super().__init__()
    
    def save_db_history(self, user_id: str, role: str, content: str, limit=5):
        """Метод для сохранения сообщения с ограничением"""
        with self.__connection:
            # Проверяем количество записей для данного пользователя и роли
            query = """ 
            SELECT COUNT(*) 
            FROM chat_history 
            WHERE user_id = %s AND role = %s; """
            self.__cursor.execute(query, (user_id, role))
            count = self.__cursor.fetchone()[0]
            
            # Если записей больше лимита, удаляем самые старые
            if count >= limit:
                query = """ DELETE FROM chat_history 
                WHERE user_id = %s AND role = %s AND timestamp IN (
                SELECT timestamp 
                FROM chat_history 
                WHERE user_id = %s AND role = %s 
                ORDER BY timestamp LIMIT %s;
                ) """
                self.__connection.execute(query, (user_id, role, user_id, role, count - limit + 1))
                self.__connection.commit()
                
            # Добавляем новую запись
            query = """ INSERT INTO chat_history (user_id, role, content) VALUES (%s, %s, %s)"""
            self.__cursor.execute(query, (user_id, role, content))
            self.__connection.commit()        
            
            
    def load_db_history(self, user_id: str):
        """Метод для загрузки истории"""
        with self.__connection:
            query = """ SELECT role, content FROM chat_history 
            WHERE user_id = %s
            ORDER BY timestamp DESC 
            LIMIT %s; """
            self.__cursor.execute(query, (user_id, 5))
            self.__connection.commit()
        return [{"role": row[0], "content": row[1]} for row in self.__cursor.fetchall()]


    def clear_db_history(self, user_id: str):
        """Метод для очистки истории"""
        with self.__connection:
            query = " DELETE FROM chat_history WHERE user_id = %s; "
            self.__cursor.execute(query, (user_id,))
            self.__connection.commit()
            
    def _create_chat_history(self):
        with self.__connection:
            query = '''
        CREATE TABLE IF NOT EXISTS chat_history(
            user_id BIGINT UNSIGNED PRIMARY KEY,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME
        )
        '''
            self.__cursor.execute(query)
            
            