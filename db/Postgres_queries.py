class UserQueries:
    GET_DB_USERS = """ 
            SELECT user_id 
            FROM users_model; 
            """

    DELETE_DB_USERS = """ 
            DELETE FROM users_model 
            WHERE user_id = %s; 
            """
    
    CLEAR_USERS = """
            DELETE * FROM users_model 
            WHERE user_id = %s
            """

    CREATE_TABLE_USERS_MODEL = """
            CREATE TABLE IF NOT EXISTS users_model
            (
                user_id BIGINT PRIMARY KEY,
                stars_donations INTEGER DEFAULT 0 CONSTRAINT positive_price CHECK(stars_donations >= 0),
                model VARCHAR(65) NOT NULL,
                visual_model TEXT NOT NULL
            );
            """
    
    
class ModelsQueries:
    START_DB_MODEL = """ 
            INSERT INTO users_model(user_id, model, visualmodel) 
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id) DO UPDATE SET
            model = %s,
            visualmodel = %s
            """
        
    GET_DB_MODEL = """ 
            SELECT model 
            FROM users_model 
            WHERE user_id = %s
            """
    
    UPDATE_DB_MODEL = """ 
            UPDATE users_model 
            SET model = %s 
            WHERE user_id = %s 
            """
            
    GET_DB_VISUALMODEL = """ 
            SELECT visualmodel 
            FROM users_model 
            WHERE user_id = %s
            """
            
    UPDATE_DB_VISUALMODEL = """ 
            UPDATE users_model 
            SET visualmodel = %s WHERE 
            user_id = %s 
            """
            
class HistoryQueries:
    
    SAVE_DB_HISTORY = """ 
            INSERT INTO chat_history (user_id, role, content) 
            VALUES (%s, %s, %s)
            """
            
    LOAD_DB_HISTORY = """
            SELECT role, content FROM chat_history 
            WHERE user_id = %s
            ORDER BY timestamp DESC 
            LIMIT %s; 
            """
            
    CLEAR_DB_HISTORY = """
            DELETE FROM chat_history 
            WHERE user_id = %s; 
            """
            
    CREATE_TABLE_CHAT_HISTORY = '''
            CREATE TABLE IF NOT EXISTS chat_history(
                user_id BIGINT UNSIGNED PRIMARY KEY,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                timestamp DATETIME
            )
            '''
            
    
            
    