from app import db
from werkzeug.security import generate_password_hash
from app.models.users import Users

class AuthService:
    @staticmethod
    def create_user(user_type, data, status):

        userData = data['userDetails']
        user = Users(
            username=userData['username'],
            consent=userData['consent'],
            user_type=user_type,
            status=status
        )
        user.set_password(userData['password'])
        db.session.add(user)
        db.session.flush() 
        return user