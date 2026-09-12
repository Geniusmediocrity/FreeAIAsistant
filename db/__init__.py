from db.table_usersettings import UserSettings
from db.table_history import UserHistory



class DataBase(UserSettings, UserHistory):
    """Consist methods of UserSettings class and of UserHistory class"""
    def __init__(self):
        super().__init__()
        
    async def create_db(self):
        """Create db if not exists"""
        await self.user_setting_tb_create()
        await self.user_history_tb_create()
        
    async def create_new_user(self, user_id: int):
        """Create new user in user_settings and in users_history tables"""
        await self.insert_new_user_us(user_id)
        await self.insert_new_user_uh(user_id)