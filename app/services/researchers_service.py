from app._init_ import db
from werkzeug.security import generate_password_hash
from app.models.researchers import Researchers

class ResearchersService:
    @staticmethod
    def create_researcher(account, data):
        researcher = Researchers(
            account_id=account.id,
            full_name=data['fullName'],
            address=data.get('address'),
            email=data['email'],
            phone=data.get('phone'),
            department=data.get('department'),
            role=data.get('role'),
            research_focus=data.get('researchFocus'),
            organization_id=data.get('organizationId')
        )
        db.session.add(researcher)