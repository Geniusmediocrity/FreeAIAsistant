import os
import logging

import asyncpg
from dotenv import load_dotenv


load_dotenv("configs/.env")
DSN = os.getenv("DSN")

class DbManager:
    """Manage connect and discount with classes that work with individual tables"""
    def __init__(self):
        self.db_config = DSN
    
    async def connect(self, min_size=1, max_size=15) -> None:
        """Database connection. Make pool conection"""
        self._pool = await asyncpg.create_pool(self.db_config, min_size=min_size, max_size=max_size)
        logging.info("The DataBase connection pool was connected succesful")
        
    async def disconnect(self) -> None:
        """Close pool connection"""
        if self._pool:
            await self._pool.close()
            logging.info("The DataBase connection pool was closed succesful")