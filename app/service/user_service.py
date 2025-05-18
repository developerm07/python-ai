from ..model.user import User

class UserService:
    def get_user(self):
        user= User(user_id=1,name="ABC")
        return user

    def get_all_users(self):
        users= [
            User(user_id=1,name="ABC"),
            User(user_id=2,name="DEF"),
            User(user_id=3,name="GHI")
        ]
        return users