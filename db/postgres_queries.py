class UserSettingTable:
    """This class stores queries to the user_settings database."""
    
    CREATE_USER_SETTINGS_TABLE = """
            CREATE TABLE "user_settings"
            (
            	user_id BIGINT PRIMARY KEY,
            	ai_model VARCHAR(58) DEFAULT 'deepseek-ai/DeepSeek-R1',
            	ai_visual_model VARCHAR(40) DEFAULT 'Qwen/Qwen2-VL-7B-Instruct'
            );
            """
            
    INSERT_NEW_USER = """
            INSERT INTO user_settings (user_id)
            VALUES ($1);"""
            
    IS_USER_EXISTS = """
            SELECT user_id
            FROM user_settings
            WHERE user_id = $1"""
        
    DELETE_USER = """ 
            DELETE FROM user_settings
            WHERE user_id = $1; 
            """
            
    GET_USERS_MODEL = """ 
            SELECT ai_model 
            FROM user_settings
            WHERE user_id = $1; 
            """
            
    GET_USERS_VISUAL_MODEL = """ 
            SELECT ai_visual_model 
            FROM user_settings
            WHERE user_id = $1; 
            """
            
    GET_ALL_USERS = """
            SELECT user_id
            FROM user_settings"""
            
    RESET_USEER_SETTINGS = """
            UPDATE user_settings
            SET
                ai_model = DEFAULT,
                ai_visual_model = DEFAULT
            WHERE user_id = $1;"""
            
    UPDATE_AI_MODEL = """
            UPDATE user_settings
            SET ai_model = $1
            WHERE user_id = $2
            """
    UPDATE_AI_VISUAL_MODEL = """
            UPDATE user_settings
            SET ai_visual_model = $1
            WHERE user_id = $2;
            """
            
    
class UsersHistoryTable:
    """This class stores queries to the users_history database."""
    
    CREATE_USERS_HISTORY_TABLE = """
            CREATE TABLE users_history
            (
            	user_id BIGINT PRIMARY KEY REFERENCES user_settings (user_id) ON UPDATE CASCADE ON DELETE CASCADE,
                conversation JSONB NOT NULL DEFAULT '[]'
            );
            """
            
    INSERT_NEW_USER_HISTORY_TABLE = """
            INSERT INTO users_history (user_id)
            VALUES ($1);"""
            
    GET_USERS_HISTORY_TABLE= """
            SELECT conversation
            FROM users_history
            WHERE user_id = $1;
            """
            
    UPDATE_USERS_HISTORY = """
            UPDATE users_history
            SET conversation = $1
            WHERE user_id = $2"""
            
    CLEAR_USERS_HISTORY = """
            UPDATE users_history 
            SET conversation = DEFAULT
            WHERE user_id = $1
            """