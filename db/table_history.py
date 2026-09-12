import json

from db.db_manager import DbManager
from db.postgres_queries import UsersHistoryTable as queries


class UserHistory(DbManager):
         
    async def user_history_tb_create(self) -> None:
        """Make user_history table"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.CREATE_USERS_HISTORY_TABLE)            
            
    async def insert_new_user_uh(self, user_id: int) -> None:
        """Make new user in user_settings"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.INSERT_NEW_USER_HISTORY_TABLE, user_id)
            
    #? Methods to work with history in users_history
    async def get_users_history(self, user_id: int) -> list[dict]:
        """Get current user history"""
        async with self._pool.acquire() as conn:
            result = await conn.fetchval(queries.GET_USERS_HISTORY_TABLE, user_id)
        return json.loads(result)
    
    async def update_user_history(self, user_id: int, conversation: list[dict]) -> None:
        """Update current user history and limits entries to 10 JSONB values"""
        history = list(await self.get_users_history(user_id))
        
        history.extend(conversation)
        if len(history) > 10:
            history = history[-10:]
            
        history = json.dumps(history, ensure_ascii=False)
            
        async with self._pool.acquire() as conn:
            await conn.execute(queries.UPDATE_USERS_HISTORY, history, user_id)
            
    async def clear_history(self, user_id: int) -> None:
        """Clear current user history requests"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.CLEAR_USERS_HISTORY, user_id)
