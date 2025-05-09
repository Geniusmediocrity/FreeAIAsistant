import psycopg2


class DataBase():
    
    def __init__(self):
        self.__connection = psycopg2.connect(
            port=5432,
            host="127.0.0.1",
            dbname="test_db",
            user="FreeAIAsist",
            password="6734",
            )
        self.__cursor = self.__connection.cursor()
        
    #! --- Работа с историей запросов ---
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
            
            
    #! --- Методы для работы с юзерами
    def get_db_users(self):
        with self.__connection:
            query = """ SELECT user_id FROM users_model; """
            result = self.__cursor.execute(query).fetchall()
            self.__connection.commit()
            return result
        
    def delete_db_user(self, user_id):
        with self.__connection:
            query = """ DELETE FROM users_model WHERE user_id = %s; """
            self.__cursor.execute(query, (user_id,))
            self.clear_db_history(user_id=user_id)
            self.__connection.commit()
                        
                        
    #! --- Методы для работы с моделями
    def start_db_model(self, user_id: str):
        with self.__connection:
            model = "deepseek-ai/DeepSeek-R1"
            visualmodel = "meta-llama/Llama-3.2-90B-Vision-Instruct"
            self.__cursor = self.__connection.cursor()
            query = """ INSERT INTO users_model(user_id, model, visualmodel) 
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                model = %s,
                visualmodel = %s
    """
            self.__cursor.execute(query, (user_id, model, visualmodel, model, visualmodel))
            self.__connection.commit()
            
    def read_db_model(self, user_id: str) -> list:
        with self.__connection:
            query = """ SELECT model FROM users_model WHERE user_id = %s"""
            self.__cursor.execute(query, (user_id, ))
            self.__connection.commit()
        return tuple(self.__cursor)[0][0]
                
    def update_db_model(self, user_id: str, model: str):
        with self.__connection:
            query = """ 
            UPDATE users_model 
            SET model = %s 
            WHERE user_id = %s """
            self.__cursor.execute(query, (model, user_id))
            self.__connection.commit()
            
    def read_db_visualmodel(self, user_id: str):
        with self.__connection:
            self.__cursor = self.__connection.cursor()
            query = """ 
            SELECT visualmodel 
            FROM users_model 
            WHERE user_id = %s"""
            self.__cursor.execute(query, (user_id, ))
            self.__connection.commit()
        return tuple(self.__cursor)[0][0]

    def update_db_visualmodel(self, user_id: str, visualmodel: str):
        with self.__connection:
            query = """ 
            UPDATE users_model 
            SET visualmodel = %s WHERE 
            user_id = %s """
            self.__cursor.execute(query, (visualmodel, user_id))
            self.__connection.commit()
            
    # ⁡⁣⁢⁡⁣⁣⁢В main.py не используются, нужны на всякий случай, и чтобы, ⁡
    # ⁡⁣⁣⁢если что почистить пользователей или пересоздать таблицы⁡
    def __clear_users(self, user_id: str):
        with self.connection:
            query = """ DELETE * FROM users_model 
                WHERE user_id = %s"""
            self.__cursor.execute(query, (user_id, ))
            self.connection.commit()
            
    def __create_chat_history(self):
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

    def __create_users_model(self):
        with self.__connection:
            query = """
            CREATE TABLE IF NOT EXISTS users_model(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                model TEXT NOT NULL,
                visual_model TEXT NOT NULL
            )
            """
            self.__cursor.execute(query)
            

