from db.table_usersettings import UserSettings
from db.table_history import UserHistory



class DataBase(UserSettings, UserHistory):
    """Consist methods of UserSettings class and of UserHistory class"""
    def __init__(self):
        super().__init__()
        
    async def create_new_user(self, user_id: int):
        await self.insert_new_user_us(user_id)
        await self.insert_new_user_uh(user_id)