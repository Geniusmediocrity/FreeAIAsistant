import asyncpg

from configs import DB_USER, DB_PASSWORD, DB_NAME, DB_HOST, DB_PORT


#! ПЕРЕДЕЛАТЬ НА АСИНХРОН И УДАЛИТЬ psycopg2

async def database_connection():
    """Create Postgres Data Base connection"""
    _connection = await asyncpg.connect(
        port=DB_PORT,
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        )
    return _connection





# async def database_executor(connection: asyncpg.Connection, query: str, parameters: tuple = tuple()):
#     """Execute postgres queries"""
#     ...