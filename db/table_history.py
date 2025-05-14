from db.db_manager import DbManager
from db.postgres_queries import UsersHistoryTable as queries


class UserHistory(DbManager):
         
    async def user_history_tb_create(self):
        """Make user_history table"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.CREATE_USERS_HISTORY_TABLE)            
            
    #? Methods to work with history in users_history
    async def get_users_history(self, user_id: int) -> list[dict]:
        """Get current user history"""
        async with self._pool.acquire() as conn:
            return await conn.fetchval(queries.GET_USERS_HISTORY_TABLE, user_id)
    
    async def update_user_history(self, user_id: int, conversation: list[dict]):
        """Update current user history and limits entries to 10 JSONB values"""
        row = await self.get_users_history(user_id)
        history = row["history"] if row and row["history"] else []
        
        history += conversation
        if len(history) > 10:
            history = history[-10:]
            
        async with self._pool.acquire() as conn:
            await conn.execute(queries.UPDATE_USERS_HISTORY, history, user_id)
            
    async def clear_history(self, user_id: int):
        """Clear current user history requests"""
        async with self.pool.acquire() as conn:
            await conn.execute(queries.CLEAR_USERS_HISTORY, user_id)
