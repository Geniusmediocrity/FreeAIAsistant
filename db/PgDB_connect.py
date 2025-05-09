import psycopg2


class DataBaseConnect():
    
    def __init__(self):
        self.__connection = psycopg2.connect(
            port=5432,
            host="127.0.0.1",
            dbname="test_db",
            user="FreeAIAsist",
            password="6734",
            )
        self.__cursor = self.__connection.cursor()
