from app import db
from app.models.organizations import Organizations
from werkzeug.security import generate_password_hash
from app.models.researchers import Researchers
from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.exc import SQLAlchemyError


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
            organization_id=data.get('organizationId'),
            date_of_birth=data['dateOfBirth']
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
            ).options(joinedload(Researchers.user)).all()

        return researchers
    
    @staticmethod
    def getAllResearchers(organization_id: int) -> List['Researchers']:
        researchers = Researchers.query.filter_by(organization_id=organization_id).all();
        return researchers


    @staticmethod
    def get_researcher_by_id(researcher_id):
        """
        Returns detailed information about a researcher by their ID,
        including user and organization data.
        """
        try:
            researcher = (
                db.session.query(Researchers)
                .join(Users, Researchers.user_id == Users.id)
                .join(Organizations, Researchers.organization_id == Organizations.id)
                .filter(Researchers.id == researcher_id)
                .first()
            )

            if not researcher:
                return None
            
            active_studies = sum(1 for trial in researcher.clinical_trials_created if trial.status != "completed")


            # Construct JSON-like response
            result = {
                'id': researcher.id,
                'full_name': researcher.full_name,
                'email': researcher.email,
                'phone': researcher.phone,
                'research_focus': researcher.research_focus,
                'date_of_birth': researcher.date_of_birth,
                'user': {
                    'id': researcher.user.id,
                    'username': researcher.user.username,
                    'status': researcher.user.status,
                    'user_type': researcher.user.user_type,
                    'created_at': researcher.user.created_at.strftime('%Y-%m-%d %H:%M:%S') if researcher.user.created_at else None
                },
                'organization': {
                    'id': researcher.organization.id,
                    'organization_name': researcher.organization.organization_name,
                    'year_of_establishment': researcher.organization.year_of_establishment,
                    'registered_address': researcher.organization.registered_address,
                    'official_email': researcher.organization.official_email
                },
                "active_studies": active_studies
            }

            return result

        except Exception as e:
            print("Error fetching researcher:", e)
            return None
    @staticmethod
    def update_researcher_field(researcher_id, data):
        """
        Update a single field for a researcher.
        - user_id: ID of the authenticated user
        - field: field name to update
        - value: new value
        """

        field = data.get("field")
        value = data.get("value")
        
        try:
            researcher = Researchers.query.filter_by(id=researcher_id).first()
            if not researcher:
                raise ValueError("Researcher not found")

            # Check if field exists in Researchers or Users
            if hasattr(researcher, field):
                setattr(researcher, field, value)
            elif hasattr(researcher.user, field):
                if field == "password":  # hash password
                    researcher.user.set_password(value)
                else:
                    setattr(researcher.user, field, value)
            else:
                raise ValueError(f"Field '{field}' not found in researcher or user")

            db.session.commit()
            return {"message": f"{field} updated successfully", "value": value}

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to update researcher field: {e}")
            raise
    