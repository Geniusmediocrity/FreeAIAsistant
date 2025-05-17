from db.db_manager import DbManager
from db.postgres_queries import UserSettingTable as queries


class UserSettings(DbManager):
        
    async def user_setting_tb_create(self) -> None:
        """Create user_settings table"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.CREATE_USER_SETTINGS_TABLE)
            
    #? Methods to work with users in user_settings
    async def insert_new_user_us(self, user_id: int) -> None:
        """Make new user in user_settings"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.INSERT_NEW_USER, user_id)
            
    async def is_user_exists(self, user_id: int) -> bool:
        """check user id in DB"""
        async with self._pool.acquire() as conn:
            return bool(await conn.fetchval(queries.IS_USER_EXISTS, user_id))
        
    async def del_user_us(self, user_id: int) -> None:
        """Delete current user from user_setting and from users_history"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.DELETE_USER, user_id)
            
    async def get_all_users(self) -> list:
        """Get ALL users from DB"""
        async with self._pool.acquire() as conn:
            users = await conn.fetch(queries.GET_ALL_USERS)
            return [user['user_id'] for user in users]
            
    #? Methods to get users ai models
    async def get_users_model(self, user_id: int) -> str:
        """Get current user ai_model"""
        async with self._pool.acquire() as conn:
            return await conn.fetchval(queries.GET_USERS_MODEL, user_id)
        
    async def get_users_visual_model(self, user_id: int) -> str:
        """Get current user ai_visual_model"""
        async with self._pool.acquire() as conn:
            return await conn.fetchval(queries.GET_USERS_VISUAL_MODEL, user_id)
                    
            
    #? Methods to change users ai models
    async def reset_user_settings(self, user_id: int) -> None:
        """Reset user_settings (ai_model, ai_visual_model) on DEFAULT value"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.RESET_USEER_SETTINGS, user_id)
        
    async def update_users_ai_model(self, user_id: int, new_ai_model: str) -> None:
        """Update current user ai_model on new_ai_model"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.UPDATE_AI_MODEL, new_ai_model, user_id)
            
    async def update_users_ai_visual_model(self, user_id: int, new_ai_visual_model: str) -> None:
        """Update current user ai_model on new_ai_model"""
        async with self._pool.acquire() as conn:
            await conn.execute(queries.UPDATE_AI_VISUAL_MODEL, new_ai_visual_model, user_id)