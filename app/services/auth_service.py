from app._init_ import db
from werkzeug.security import generate_password_hash
from app.models.accounts import Accounts

class AuthService:
    @staticmethod
    def create_account(data):
        account = Accounts(
            username=data['username'],
            consent=data['consent'],
            user_type=data['userType']
        )
        account.set_password(data['password'])
        db.session.add(account)
        db.session.flush() 
        return account