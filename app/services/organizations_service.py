from app import db
from app.models.organizations import Organizations
from app.services.researchers_service import ResearchersService
from sqlalchemy.exc import SQLAlchemyError
from collections import defaultdict

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
            contact_phone=data.get('contactPersonPhone'),
            year_of_establishment=data.get('yearOfEstablishment')
        )
        db.session.add(org)
        db.session.flush()

        return org

    
    @staticmethod
    def getOrganizationDashDetails(organizationId: int):
        organization = Organizations.query.filter_by(id=organizationId).first()
        if not organization:
            return None  # or raise error

        # Calculate active and completed clinical trials
        active_clinical_trials = [trial for trial in organization.clinical_trials if trial.status == 'active']
        completed_clinical_trials = [trial for trial in organization.clinical_trials if trial.status == 'completed']

        # Calculate total participants across all clinical trials
        total_participants = sum(len(trial.trial_participants) for trial in organization.clinical_trials)

        # ---- Monthly Participants Growth ----
        # Assuming trial_participant has a 'joined_date' (datetime) field
        monthly_participants = defaultdict(int)

        for trial in organization.clinical_trials:
            for participant in trial.trial_participants:
                print(participant.created_at)
                if participant.created_at:  # make sure date exists
                    month_key = participant.created_at.strftime("%b")  # e.g. Jan, Feb
                    monthly_participants[month_key] += 1

        # Sort by month order (Jan → Dec)
        month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                    "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        participant_growth = [
            {"month": m, "participants": monthly_participants.get(m, 0)}
            for m in month_order
        ]

        # --- Researchers ---
        researchers = ResearchersService.getAllResearchers(organization_id=organizationId)
        topResearchers = []

        for researcher in researchers:
            # Get all trials linked to researcher
            trials = [tr.clinical_trial for tr in researcher.trial_researchers]

            active_trials_count = sum(1 for trial in trials if trial.status == 'active')
            completed_trials_count = sum(1 for trial in trials if trial.status == 'completed')

            topResearchers.append({
                'id': researcher.id,
                'full_name': researcher.full_name,
                'email': researcher.email,
                'totalTrials': len(trials),
                'activeTrials': active_trials_count,
                'completedTrials': completed_trials_count,
            })

        topResearchers = sorted(topResearchers, key=lambda x: x['completedTrials'], reverse=True)[:3]

        return {
            'organization': {
                'id': organization.id,
                'organization_name': organization.organization_name,
                'email': organization.official_email
            },
            'total_participants': total_participants,
            'active_clinical_trials': len(active_clinical_trials),
            'completed_clinical_trials': len(completed_clinical_trials),
            'participant_growth': participant_growth,   
            'topResearchers': topResearchers,
            'total_researchers': len(researchers)
        }

    
    @staticmethod
    def getOrganizationDetails(organizationId: int):
        """
        Fetch organization details along with total participants and researchers.
        """
        organization = Organizations.query.filter_by(id=organizationId).first()
        if not organization:
            return None 


        user = organization.user

        return {
            'id': organization.id,
            'organization_name': organization.organization_name,
            'official_email': organization.official_email,
            'registered_address': organization.registered_address,
            'year_of_establishment': organization.year_of_establishment,
            'contact_person_name': organization.contact_full_name,
            'contact_person_designation': organization.contact_designation,
            'contact_person_phone': organization.contact_phone,
            'status': user.status,
            'username': user.username
        }
        

    @staticmethod
    def getTrialsByOrganizationId(organizationId: int):
        """
        Fetch all clinical trials associated with a given organization ID
        and format the response according to TypeScript interfaces.
        """
        organization = Organizations.query.filter_by(id=organizationId).first()
        if not organization:
            return []  # or raise an exception

        trials_data = []
        for trial in organization.clinical_trials:
            # Enrolled Researchers
            enrolled_researchers = []
            for tr in trial.trial_researchers:
                researcher = tr.researcher  # assuming TrialResearchers has researcher relationship
                enrolled_researchers.append({
                    "id": researcher.id,
                    "full_name": researcher.full_name,
                    "email": researcher.email,
                    "phone": researcher.phone,
                    "joinedDate": tr.created_at.strftime("%Y-%m-%d") if tr.created_at else None,
                    "research_focus": researcher.research_focus,
                    "address": researcher.address
                })

            # Enrolled Participants
            enrolled_participants = []
            for participant in trial.trial_participants:
                enrolled_participants.append({
                    "id": participant.id,
                    "phone": participant.participant.phone,
                    "joinedDate": participant.created_at.strftime("%Y-%m-%d") if participant.created_at else None,
                    "status": participant.participant.user.status,
                    "date_of_birth": participant.participant.date_of_birth.strftime("%Y-%m-%d") if participant.participant.date_of_birth else None,
                    "full_name": participant.participant.full_name
                })

            trials_data.append({
                "id": trial.id,
                "title": trial.title,
                "overview": trial.overview,
                "whoCanParticipate": trial.participation_criteria,
                "visit_details": trial.visit_details,
                "risks": getattr(trial.trial_consent_information, 'risks', None),
                "benefits": getattr(trial.trial_consent_information, 'benefits', None),
                "privacy": getattr(trial.trial_consent_information, 'privacy', None),
                "compensation": getattr(trial.trial_consent_information, 'compensation', None),
                "rights": getattr(trial.trial_consent_information, 'rights', None),
                "safetyContacts": getattr(trial.trial_consent_information, 'safety_contacts', None),
                "ethics": getattr(trial.trial_consent_information, 'ethics', None),
                "consent_understanding": getattr(trial.trial_consent_information, 'consent_understanding', None),
                "total_duration": trial.total_duration,
                "total_compensation": getattr(trial.trial_consent_information, 'total_compensation', None),
                "total_visits": trial.total_visits,
                "status": trial.status,
                "startDate": trial.created_at.strftime("%Y-%m-%d") if trial.created_at else None,
                "endDate": trial.updated_at.strftime("%Y-%m-%d") if trial.status == 'completed' and trial.updated_at else None,
                "enrolledResearchers": enrolled_researchers,
                "enrolledParticipants": enrolled_participants,
                "location": {
                    "id": trial.location.id if trial.location else None,
                    "county_name": trial.location.county.name if trial.location and trial.location.county else None,
                    "country_name": trial.location.country.name if trial.location and trial.location.country else None,
                    "city_name": trial.location.city.name if trial.location and trial.location.city else None
                },
                "createdByResearcher": getattr(trial.created_by_researcher, 'full_name', None)
            })

        return trials_data

    @staticmethod
    def update_organization_details(user_id, organization_id, data):
        """
        Update organization details.
        `data` should be a dict like:
        {
            "section": "organization" | "user",
            "field": "organization_name",
            "value": "New Org Name"
        }
        """
        try:
            organization = Organizations.query.filter_by(
                id=organization_id, user_id=user_id
            ).first()

            if not organization:
                raise ValueError("Organization not found")

            section = data.get("section")
            field = data.get("field")
            value = data.get("value")

            if section == "organization":
                if not hasattr(organization, field):
                    raise ValueError(f"Invalid field '{field}' for organization")
                setattr(organization, field, value)

            elif section == "user":
                user = organization.user
                if not hasattr(user, field):
                    raise ValueError(f"Invalid field '{field}' for user")
                if field == "password":  # use hashing
                    user.set_password(value)
                else:
                    setattr(user, field, value)

            else:
                raise ValueError(f"Invalid section '{section}'")

            db.session.commit()
            return {"message": f"{section}.{field} updated successfully", "value": value}

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to update organization details: {e}")
            raise