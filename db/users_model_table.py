from .PgDB_connect import database_connection


class UsersModelTable(database_connection):
    """ Методы для работы с юзерами"""
    
    def __init__(self):
        # TODO self._create_users_model()
        super().__init__()
    
    #! --- Методы для работы с юзерами
    def get_db_users(self):
        with self._connection:
            query = """ SELECT user_id FROM users_model; """
            result = self._cursor.execute(query).fetchall()
            self._connection.commit()
            return result
        
    def delete_db_user(self, user_id):
        with self._connection:
            query = """ DELETE FROM users_model WHERE user_id = %s; """
            self._cursor.execute(query, (user_id,))
            self.clear_db_history(user_id=user_id)
            self._connection.commit()
            
            
    #! --- Методы для работы с моделями
    def start_db_model(self, user_id: str):
        """Начало работы с моделями(регистрация в бд нового юзера)"""
        with self._connection:
            model = "deepseek-ai/DeepSeek-R1"
            visualmodel = "meta-llama/Llama-3.2-90B-Vision-Instruct"
            self._cursor = self._connection.cursor()
            query = """ INSERT INTO users_model(user_id, model, visualmodel) 
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
                model = %s,
                visualmodel = %s
    """
            self._cursor.execute(query, (user_id, model, visualmodel, model, visualmodel))
            self._connection.commit()
            
    def get_db_model(self, user_id: str) -> list:
        """Получение модели пользователя"""
        with self._connection:
            query = """ SELECT model FROM users_model WHERE user_id = %s"""
            self._cursor.execute(query, (user_id, ))
            self._connection.commit()
        return tuple(self._cursor)[0][0]
                
    def update_db_model(self, user_id: str, model: str):
        """Обновление модели пользователя"""
        with self._connection:
            query = """ 
            UPDATE users_model 
            SET model = %s 
            WHERE user_id = %s """
            self._cursor.execute(query, (model, user_id))
            self._connection.commit()
        
    def get_db_visualmodel(self, user_id: str):
        """Получение визуальной модели пользователя"""
        with self._connection:
            self._cursor = self._connection.cursor()
            query = """ 
            SELECT visualmodel 
            FROM users_model 
            WHERE user_id = %s"""
            self._cursor.execute(query, (user_id, ))
            self._connection.commit()
        return tuple(self._cursor)[0][0]

    def update_db_visualmodel(self, user_id: str, visualmodel: str):
        """Обновление визуальной модели пользователя"""
        with self._connection:
            query = """ 
            UPDATE users_model 
            SET visualmodel = %s WHERE 
            user_id = %s """
            self._cursor.execute(query, (visualmodel, user_id))
            self._connection.commit()
            
            
    def _clear_users(self, user_id: str):
        """Удадение пользователя"""
        with self.connection:
            query = """ DELETE * FROM users_model 
                WHERE user_id = %s"""
            self._cursor.execute(query, (user_id, ))
            self.connection.commit()
            
    
    def _create_users_model(self):
        """Создание БД"""
        with self._connection:
            query = """
            CREATE TABLE IF NOT EXISTS users_model
            (
	            user_id BIGINT PRIMARY KEY,
	            stars_donations INTEGER DEFAULT 0 CONSTRAINT positive_price CHECK(stars_donations >= 0),
            	model VARCHAR(65) NOT NULL,
	            visual_model TEXT NOT NULL
            );
            """
            self._cursor.execute(query)