import sqlite3


def start_db_model(username: str):
    with sqlite3.connect(database="db/DataBase.db") as db:
        model = "deepseek-ai/DeepSeek-R1"
        cursor = db.cursor()
        query = f""" INSERT INTO users_model(username, model) 
        VALUES (?, ?)
        ON CONFLICT (username) DO UPDATE SET
            model = ?
"""
        cursor.execute(query, (username, model, model))
        db.commit()
        
def read_db_model(username: str) -> list:
    with sqlite3.connect(database="db/DataBase.db") as db:
        cursor = db.cursor()
        query = """ SELECT * FROM users_model WHERE username = ?"""
        cursor.execute(query, (username, ))
        db.commit()
    return tuple(cursor)[0][1]
            
def update_db_model(username: str, model: str):
    with sqlite3.connect(database="db/DataBase.db") as db:
        cursor = db.cursor()
        query = f""" UPDATE users_model SET model = ? WHERE username = ? """
        cursor.execute(query, (model, username))
        db.commit()


# with sqlite3.connect("db/DataBase.db") as db:
#     cursor = db.cursor()
#     query = """
#     CREATE TABLE IF NOT EXISTS users_model(
#         username UNIQUE NOT NULL,
#         model TEXT NOT NULL,
#     )
#     """
#     cursor.execute(query)