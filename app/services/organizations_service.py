from typing import List
from app import db
from app.models.organizations import Organizations
from app.models.researchers import Researchers
from app.models.users import Users

class OrganizationsService:
    @staticmethod
    def create_organization(user, data):
       
        org = Organizations(
            user_id=user.id,
            organization_name=data['organizationName'],
            registered_address=data['registeredAddress'],
            official_email=data['officialEmail'],
            contact_full_name=data.get('contactPersonName'),
            contact_designation=data.get('contactPersonDesignation'),
            contact_phone=data.get('contactPersonPhone')
        )
        db.session.add(org)
        db.session.flush()

        return org
    
    
    