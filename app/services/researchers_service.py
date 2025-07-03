from app import db
from werkzeug.security import generate_password_hash
from app.models.researchers import Researchers
from typing import List, Optional
from sqlalchemy.orm import joinedload

from app.models.users import Users
class ResearchersService:
    @staticmethod
    def create_researcher(user, data):
        researcher = Researchers(
            user_id=user.id,
            full_name=data['fullName'],
            address=data.get('address'),
            email=data['email'],
            phone=data.get('phone'),
            research_focus=data.get('researchFocus'),
            organization_id=data.get('organizationId')
        )
        db.session.add(researcher)
        db.session.flush()

        return researcher

    @staticmethod
    def getResearcherByUserId(userId) -> Optional[Researchers]:

        researcher = Researchers.query.filter_by(user_id=userId).first()
        return researcher
    
    @staticmethod
    def updateStatus(researcher_id: int, status: str) -> Optional[Researchers]:
        researcher = Researchers.query.filter_by(id=researcher_id).first()
        if researcher:
            researcher.user.status = status
            db.session.commit()
        return researcher
    
    @staticmethod
    def getAllNotApprovedUsers(organization_id: int) -> List['Researchers']:
        researchers = Researchers.query\
            .join(Researchers.user)\
            .filter(
                Researchers.organization_id == organization_id,
                Users.status == "not-verified"
            ).options(joinedload(Researchers.user)).all()

        return researchers
