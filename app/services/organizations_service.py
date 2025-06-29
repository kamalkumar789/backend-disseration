from app._init_ import db
from app.models.organizations import Organizations

class OrganizationsService:
    @staticmethod
    def create_organization(account, data):
        primary_contact = data.get('primaryContact', {})
        org = Organizations(
            account_id=account.id,
            organization_name=data['organizationName'],
            legal_entity_type=data['legalEntityType'],
            registered_address=data['registeredAddress'],
            official_email=data['officialEmail'],
            contact_full_name=primary_contact.get('fullName'),
            contact_designation=primary_contact.get('designation'),
            contact_phone=primary_contact.get('phone')
        )
        db.session.add(org)