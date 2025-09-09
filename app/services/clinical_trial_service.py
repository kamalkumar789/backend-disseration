
from datetime import datetime
from app.models.clinical_trial_location import ClinicalTrialLocation
from app.models.clinical_trials import ClinicalTrials
from app.models.meetings import Meetings
from app.models.researchers import Researchers
from app.models.trial_consent_Information import TrialConsentInformation
from app.models.trial_researchers import TrialResearchers
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import asc, func
from sqlalchemy import and_


from app import db
from app.models.trial_participants import TrialParticipants


class ClinicalTrialService:

    @staticmethod
    def createClinicalTrial(data, organization_id, researcher_id, location_id):
        clinicaltrial = ClinicalTrials(
            title=data['title'],
            organization_id=organization_id,
            created_by_researcher_id=researcher_id,
            overview=data['overview'],
            participation_criteria=data['participation_criteria'],
            visit_details=data['visit_details'],
            total_duration=data['total_duration'],
            clinical_trial_location_id=location_id,
            total_visits=data['total_visits'],
            status="active"
        )

        db.session.add(clinicaltrial)
        db.session.flush()  

        return clinicaltrial
    
    @staticmethod
    def createClinicalTrialLocation(data):

        location = ClinicalTrialLocation(
            address=data.get('address'),
            country_id=data.get('country_id'),
            county_id=data.get('county_id'),
            city_id=data.get('city_id')
        )
        db.session.add(location)
        db.session.flush()  

        return location

    @staticmethod
    def createClinicalTrialsConsent(data, clinical_trial_id):
        consentInformation = TrialConsentInformation(
            clinical_trial_id=clinical_trial_id,
            risks=data['risks'],
            benefits=data['benefits'],
            privacy=data['privacy'],
            compensation=data['compensation'],
            rights=data['rights'],
            safety_contacts=data['safety_contacts'],
            ethics=data['ethics'],
            consent_understanding=data['consent_understanding'],
            total_compensation=data['total_compensation']

        )

        db.session.add(consentInformation)

        return consentInformation
    
    @staticmethod
    def getAllClinicalTrialsByOrganizationId(organization_id):
        clinical_trials = ClinicalTrials.query.filter_by(organization_id=organization_id).all()

        result = []

        for trial in clinical_trials:
            # Get researchers from junction table
            researchers = [
                {
                    "id": tr.researcher.id,
                    "full_name": tr.researcher.full_name,
                    "email": tr.researcher.email
                }
                for tr in trial.trial_researchers
            ]

            # Get consent info
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "overview": trial.overview,
                "participation_criteria": trial.participation_criteria,
                "visit_details": trial.visit_details,
                "total_duration": trial.total_duration,
                "total_visits": trial.total_visits,
                "status": trial.status,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at,
                
                "researchers": researchers,
                "consent": {
                    "id": consent.id,
                    "risks": consent.risks,
                    "benefits": consent.benefits,
                    "privacy": consent.privacy,
                    "compensation": consent.compensation,
                    "rights": consent.rights,
                    "safety_contacts": consent.safety_contacts,
                    "ethics": consent.ethics,
                    "consent_understanding": consent.consent_understanding,
                    "total_compensation": consent.total_compensation

                } if consent else None,
                "location": {
                    "id": location.id if location is not None else None,
                    "country_name": location.country.name if location is not None else "",
                    "county_name": location.county.name if location is not None else "",
                    "city_name": location.city.name if location is not None else ""
                }
            }

            result.append(trial_data)

        return result
    
    @staticmethod
    def getAllClinicalTrials(participant_id):
        subquery = db.session.query(TrialParticipants.clinical_trial_id).filter_by(
            participant_id=participant_id
        )

        # Main query: all clinical trials NOT in that subquery
        clinical_trials = ClinicalTrials.query.filter(
            ~ClinicalTrials.id.in_(subquery)
        ).all()

        result = []

        for trial in clinical_trials:
            researchers = [
                {
                    "id": tr.researcher.id,
                    "full_name": tr.researcher.full_name,
                    "email": tr.researcher.email
                }
                for tr in trial.trial_researchers
            ]

            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "overview": trial.overview,
                "participation_criteria": trial.participation_criteria,
                "visit_details": trial.visit_details,
                "total_duration": trial.total_duration,
                "total_visits": trial.total_visits,
                "status": trial.status,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at,
                "researchers": researchers,
                "consent": {
                    "id": consent.id,
                    "risks": consent.risks,
                    "benefits": consent.benefits,
                    "privacy": consent.privacy,
                    "compensation": consent.compensation,
                    "rights": consent.rights,
                    "safety_contacts": consent.safety_contacts,
                    "ethics": consent.ethics,
                    "consent_understanding": consent.consent_understanding,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location is not None else None,
                    "country_name": location.country.name if location is not None else "",
                    "county_name": location.county.name if location is not None else "",
                    "city_name": location.city.name if location is not None else ""
                }
            }

            result.append(trial_data)

        return result
    

    @staticmethod
    def getClinicalTrialsById(clinical_id, participant_id):
        trial = ClinicalTrials.query.get(clinical_id)  # direct PK lookup

        if not trial:
            return None  # or raise Exception / return {}

        researchers = [
            {
                "id": tr.researcher.id,
                "full_name": tr.researcher.full_name,
                "email": tr.researcher.email
            }
            for tr in trial.trial_researchers
        ]

        consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
        location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
        is_registered = TrialParticipants.query.filter_by(
                participant_id=participant_id, clinical_trial_id=clinical_id
            ).first() is not None
        
        trial_data = {
            "id": trial.id,
            "title": trial.title,
            "overview": trial.overview,
            "participation_criteria": trial.participation_criteria,
            "visit_details": trial.visit_details,
            "total_duration": trial.total_duration,
            "total_visits": trial.total_visits,
            "status": trial.status,
            "created_by": trial.created_by_researcher.full_name if trial.created_by_researcher else None,
            "created_at": trial.created_at,
            "researchers": researchers,
            "isRegisteredAlready": is_registered,
            "consent": {
                "id": consent.id,
                "risks": consent.risks,
                "benefits": consent.benefits,
                "privacy": consent.privacy,
                "compensation": consent.compensation,
                "rights": consent.rights,
                "safety_contacts": consent.safety_contacts,
                "ethics": consent.ethics,
                "consent_understanding": consent.consent_understanding,
                "total_compensation": consent.total_compensation
            } if consent else None,
            "location": {
                "id": location.id if location else None,
                "country_name": location.country.name if location and location.country else "",
                "county_name": location.county.name if location and location.county else "",
                "city_name": location.city.name if location and location.city else ""
            } if location else None,
        }

        return trial_data


    def getClinicalTrialsByParticipantId(participant_id):
        clinical_trials = (
            db.session.query(ClinicalTrials)
            .join(TrialParticipants, TrialParticipants.clinical_trial_id == ClinicalTrials.id)
            .filter(TrialParticipants.participant_id == participant_id)
            .all()
        )

        result = []

        for trial in clinical_trials:

            # Consent and location info
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

            # Meetings for this participant and trial
            meetings_query = Meetings.query.filter_by(
                trial_id=trial.id,
                participant_id=participant_id
            )

            # Next upcoming meeting
            new_next_meeting = meetings_query.filter(Meetings.meeting_date >= datetime.now(), Meetings.status != "completed") \
                                            .order_by(asc(Meetings.meeting_date)) \
                                            .first()

            # Total completed meetings
            total_completed_meetings = meetings_query.filter(Meetings.status == "completed").count()

            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "total_duration": trial.total_duration,
                "status": trial.status,
                "total_visits": trial.total_visits,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at.strftime("%d %b %Y"),
                "consent": {
                    "id": consent.id,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location else None,
                    "country_name": location.country.name if location else "",
                    "county_name": location.county.name if location else "",
                    "city_name": location.city.name if location else ""
                },
                "new_next_meeting": {
                    "id": new_next_meeting.id,
                    "meeting_date": new_next_meeting.meeting_date, 
                    "meeting_location": new_next_meeting.meeting_location,
                    "meeting_type": new_next_meeting.meeting_type,
                    "status": new_next_meeting.status
                } if new_next_meeting else None,
                "total_completed_meetings": total_completed_meetings
            }

            result.append(trial_data)

        return result

    
    @staticmethod
    def getClinicalTrialsByResearcherId(researcher_id):
        clinical_trials = (
            db.session.query(ClinicalTrials)
            .join(TrialResearchers, TrialResearchers.clinical_trial_id == ClinicalTrials.id)
            .filter(TrialResearchers.researcher_id == researcher_id)
            .all()
        )

        result = []

        for trial in clinical_trials:
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
            meetings_query = Meetings.query.filter_by(
                trial_id=trial.id,
            )

            # Total completed meetings
            total_completed_meetings = meetings_query.filter(Meetings.status == "completed").count()
            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "total_duration": trial.total_duration,
                "status": trial.status,
                "total_visits": trial.total_visits,
                "created_at": trial.created_at,
                "consent": {
                    "id": consent.id,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location else None,
                    "country_name": location.country.name if location and location.country else "",
                    "county_name": location.county.name if location and location.county else "",
                    "city_name": location.city.name if location and location.city else ""
                } if location else None,
                "total_participants": len(trial.trial_participants) if trial.trial_participants else 0,
                "completed_visits": total_completed_meetings
            }

            result.append(trial_data)

        return result


    @staticmethod
    def register_participant(data, participant_id):
        try:
            trial_id = data.get('trial_id')
            if not trial_id:
                raise ValueError("trial_id is required")

            # Check if trial exists
            trial = ClinicalTrials.query.get(trial_id)
            if not trial:
                raise ValueError(f"Clinical trial with id {trial_id} does not exist")

            # Check if already registered (optional)
            existing = TrialParticipants.query.filter_by(
                clinical_trial_id=trial_id, 
                participant_id=participant_id
            ).first()
            if existing:
                raise ValueError("Participant is already registered for this trial")

            # Register participant
            trial_participant = TrialParticipants(
                clinical_trial_id=trial_id,
                participant_id=participant_id
            )
            db.session.add(trial_participant)
            db.session.commit()

            return trial_participant

        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            # You could raise or return an error dict depending on your API style
            return {"error": str(e)}
    
    @staticmethod
    def register_trial_researcher(trial_id, researcher_id):
        try:
            # Check if trial exists
            trial = ClinicalTrials.query.get(trial_id)
            if not trial:
                raise ValueError(f"Clinical trial with id {trial_id} does not exist")

            # Check if researcher exists
            researcher = Researchers.query.get(researcher_id)
            if not researcher:
                raise ValueError(f"Researcher with id {researcher_id} does not exist")

            # Check if already registered
            existing = TrialResearchers.query.filter_by(
                clinical_trial_id=trial_id, 
                researcher_id=researcher_id
            ).first()
            if existing:
                raise ValueError("Researcher is already registered for this trial")

            # Register researcher
            trial_researcher = TrialResearchers(
                clinical_trial_id=trial_id,
                researcher_id=researcher_id
            )
            db.session.add(trial_researcher)
            db.session.commit()

            return trial_researcher

        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            return {"error": str(e)}
        

    @staticmethod
    def getAllDetailsByClinicalTrailId(trial_id):
        trial = ClinicalTrials.query.get(trial_id)

        if not trial:
            return None  # or raise Exception

        # Researchers
        researchers = [
            {
                "id": tr.researcher.id,
                "full_name": tr.researcher.full_name,
                "email": tr.researcher.email,
                "phone": tr.researcher.phone,
                "research_focus": tr.researcher.research_focus,
                "date_of_birth": tr.researcher.date_of_birth
            }
            for tr in trial.trial_researchers
            if tr.researcher is not None
        ]

        # Participants
        participants = []
        for tp in trial.trial_participants:
            if tp.participant is None:
                continue

            participant_meetings = Meetings.query.filter_by(
                trial_id=trial.id,
                participant_id=tp.participant.id
            )

            # Next upcoming meeting
            next_meeting = participant_meetings.filter(Meetings.meeting_date >= datetime.now(), Meetings.status != "completed") \
                                            .order_by(asc(Meetings.meeting_date)) \
                                            .first()

            # Last completed meeting
            last_meeting = participant_meetings.filter(Meetings.status == "completed") \
                                            .order_by(Meetings.meeting_date.desc()) \
                                            .first()

            participants.append({
                "id": tp.participant.id,
                "full_name": tp.participant.full_name,
                "email": tp.participant.email,
                "status": tp.participant.user.status,
                "joined_at": tp.participant.created_at,
                "next_visit": next_meeting.meeting_date if next_meeting else None,
                "last_visit": last_meeting.meeting_date if last_meeting else None,
                "phone": tp.participant.phone
            })

        # Consent
        consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()

        # Location
        location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

        # Total completed meetings
        total_completed_meetings = Meetings.query.filter_by(trial_id=trial.id, status="completed").count()

        trial_data = {
            "id": trial.id,
            "title": trial.title,
            "overview": trial.overview,
            "participation_criteria": trial.participation_criteria,
            "visit_details": trial.visit_details,
            "total_duration": trial.total_duration,
            "total_visits": trial.total_visits,
            "status": trial.status,
            "created_by": trial.created_by_researcher.full_name if trial.created_by_researcher else None,
            "created_at": trial.created_at,
            "researchers": researchers,
            "participants": participants,
            "consent": {
                "id": consent.id,
                "risks": consent.risks,
                "benefits": consent.benefits,
                "privacy": consent.privacy,
                "compensation": consent.compensation,
                "rights": consent.rights,
                "safety_contacts": consent.safety_contacts,
                "ethics": consent.ethics,
                "consent_understanding": consent.consent_understanding,
                "total_compensation": consent.total_compensation,
            } if consent else None,
            "location": {
                "id": location.id if location else None,
                "country_name": location.country.name if location and location.country else "",
                "county_name": location.county.name if location and location.county else "",
                "city_name": location.city.name if location and location.city else "",
            } if location else None,
            "completed_visits": total_completed_meetings
        }

        return trial_data



from datetime import datetime
from app.models.clinical_trial_location import ClinicalTrialLocation
from app.models.clinical_trials import ClinicalTrials
from app.models.meetings import Meetings
from app.models.researchers import Researchers
from app.models.trial_consent_Information import TrialConsentInformation
from app.models.trial_researchers import TrialResearchers
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import asc, func

from app import db
from app.models.trial_participants import TrialParticipants


class ClinicalTrialService:

    @staticmethod
    def createClinicalTrial(data, organization_id, researcher_id, location_id):
        clinicaltrial = ClinicalTrials(
            title=data['title'],
            organization_id=organization_id,
            created_by_researcher_id=researcher_id,
            overview=data['overview'],
            participation_criteria=data['participation_criteria'],
            visit_details=data['visit_details'],
            total_duration=data['total_duration'],
            clinical_trial_location_id=location_id,
            total_visits=data['total_visits'],
            status="active"
        )

        db.session.add(clinicaltrial)
        db.session.flush()  

        return clinicaltrial
    
    @staticmethod
    def createClinicalTrialLocation(data):

        location = ClinicalTrialLocation(
            address=data.get('address'),
            country_id=data.get('country_id'),
            county_id=data.get('county_id'),
            city_id=data.get('city_id')
        )
        db.session.add(location)
        db.session.flush()  

        return location

    @staticmethod
    def createClinicalTrialsConsent(data, clinical_trial_id):
        consentInformation = TrialConsentInformation(
            clinical_trial_id=clinical_trial_id,
            risks=data['risks'],
            benefits=data['benefits'],
            privacy=data['privacy'],
            compensation=data['compensation'],
            rights=data['rights'],
            safety_contacts=data['safety_contacts'],
            ethics=data['ethics'],
            consent_understanding=data['consent_understanding'],
            total_compensation=data['total_compensation']

        )

        db.session.add(consentInformation)

        return consentInformation
    
    @staticmethod
    def getAllClinicalTrialsByOrganizationId(organization_id):
        clinical_trials = ClinicalTrials.query.filter(
            and_(
                ClinicalTrials.organization_id == organization_id,
                ClinicalTrials.status != 'deleted'
            )
        ).all()
        result = []

        for trial in clinical_trials:
            # Get researchers from junction table
            researchers = [
                {
                    "id": tr.researcher.id,
                    "full_name": tr.researcher.full_name,
                    "email": tr.researcher.email
                }
                for tr in trial.trial_researchers
            ]

            # Get consent info
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "overview": trial.overview,
                "participation_criteria": trial.participation_criteria,
                "visit_details": trial.visit_details,
                "total_duration": trial.total_duration,
                "total_visits": trial.total_visits,
                "status": trial.status,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at,
                
                "researchers": researchers,
                "consent": {
                    "id": consent.id,
                    "risks": consent.risks,
                    "benefits": consent.benefits,
                    "privacy": consent.privacy,
                    "compensation": consent.compensation,
                    "rights": consent.rights,
                    "safety_contacts": consent.safety_contacts,
                    "ethics": consent.ethics,
                    "consent_understanding": consent.consent_understanding,
                    "total_compensation": consent.total_compensation

                } if consent else None,
                "location": {
                    "id": location.id if location is not None else None,
                    "country_name": location.country.name if location is not None else "",
                    "county_name": location.county.name if location is not None else "",
                    "city_name": location.city.name if location is not None else ""
                }
            }

            result.append(trial_data)

        return result
    
    @staticmethod
    def getAllClinicalTrials(participant_id):
        subquery = db.session.query(TrialParticipants.clinical_trial_id).filter_by(
            participant_id=participant_id
        )

        # Main query: all clinical trials NOT in that subquery
        clinical_trials = ClinicalTrials.query.filter(
            and_(
                ~ClinicalTrials.id.in_(subquery),
                ClinicalTrials.status != 'deleted'
            )
        ).all()

        result = []

        for trial in clinical_trials:
            researchers = [
                {
                    "id": tr.researcher.id,
                    "full_name": tr.researcher.full_name,
                    "email": tr.researcher.email
                }
                for tr in trial.trial_researchers
            ]

            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "overview": trial.overview,
                "participation_criteria": trial.participation_criteria,
                "visit_details": trial.visit_details,
                "total_duration": trial.total_duration,
                "total_visits": trial.total_visits,
                "status": trial.status,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at,
                "researchers": researchers,
                "consent": {
                    "id": consent.id,
                    "risks": consent.risks,
                    "benefits": consent.benefits,
                    "privacy": consent.privacy,
                    "compensation": consent.compensation,
                    "rights": consent.rights,
                    "safety_contacts": consent.safety_contacts,
                    "ethics": consent.ethics,
                    "consent_understanding": consent.consent_understanding,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location is not None else None,
                    "country_name": location.country.name if location is not None else "",
                    "county_name": location.county.name if location is not None else "",
                    "city_name": location.city.name if location is not None else ""
                }
            }

            result.append(trial_data)

        return result
    

    @staticmethod
    def getClinicalTrialsById(clinical_id, participant_id):
        trial = ClinicalTrials.query.get(clinical_id)  # direct PK lookup

        if not trial:
            return None  # or raise Exception / return {}

        researchers = [
            {
                "id": tr.researcher.id,
                "full_name": tr.researcher.full_name,
                "email": tr.researcher.email
            }
            for tr in trial.trial_researchers
        ]

        consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
        location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
        is_registered = TrialParticipants.query.filter_by(
                participant_id=participant_id, clinical_trial_id=clinical_id
            ).first() is not None
        
        trial_data = {ClinicalTrials.status != "deleted"
            "id": trial.id,
            "title": trial.title,
            "overview": trial.overview,
            "participation_criteria": trial.participation_criteria,
            "visit_details": trial.visit_details,
            "total_duration": trial.total_duration,
            "total_visits": trial.total_visits,
            "status": trial.status,
            "created_by": trial.created_by_researcher.full_name if trial.created_by_researcher else None,
            "created_at": trial.created_at,
            "researchers": researchers,
            "isRegisteredAlready": is_registered,
            "consent": {
                "id": consent.id,
                "risks": consent.risks,
                "benefits": consent.benefits,
                "privacy": consent.privacy,
                "compensation": consent.compensation,
                "rights": consent.rights,
                "safety_contacts": consent.safety_contacts,
                "ethics": consent.ethics,
                "consent_understanding": consent.consent_understanding,
                "total_compensation": consent.total_compensation
            } if consent else None,
            "location": {
                "id": location.id if location else None,
                "country_name": location.country.name if location and location.country else "",
                "county_name": location.county.name if location and location.county else "",
                "city_name": location.city.name if location and location.city else ""
            } if location else None,
        }

        return trial_data


    def getClinicalTrialsByParticipantId(participant_id):
        clinical_trials = (
            db.session.query(ClinicalTrials)
            .join(TrialParticipants, TrialParticipants.clinical_trial_id == ClinicalTrials.id)
            .filter(TrialParticipants.participant_id == participant_id, ClinicalTrials.status != "deleted")
            .all()
        )

        result = []

        for trial in clinical_trials:

            # Consent and location info
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

            # Meetings for this participant and trial
            meetings_query = Meetings.query.filter_by(
                trial_id=trial.id,
                participant_id=participant_id
            )

            # Next upcoming meeting
            new_next_meeting = meetings_query.filter(Meetings.meeting_date >= datetime.now(), Meetings.status != "completed") \
                                            .order_by(asc(Meetings.meeting_date)) \
                                            .first()

            # Total completed meetings
            total_completed_meetings = meetings_query.filter(Meetings.status == "completed").count()

            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "total_duration": trial.total_duration,
                "status": trial.status,
                "total_visits": trial.total_visits,
                "created_by": trial.created_by_researcher.full_name,
                "created_at": trial.created_at.strftime("%d %b %Y"),
                "consent": {
                    "id": consent.id,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location else None,
                    "country_name": location.country.name if location else "",
                    "county_name": location.county.name if location else "",
                    "city_name": location.city.name if location else ""
                },
                "new_next_meeting": {
                    "id": new_next_meeting.id,
                    "meeting_date": new_next_meeting.meeting_date, 
                    "meeting_location": new_next_meeting.meeting_location,
                    "meeting_type": new_next_meeting.meeting_type,
                    "status": new_next_meeting.status
                } if new_next_meeting else None,
                "total_completed_meetings": total_completed_meetings
            }

            result.append(trial_data)

        return result

    
    @staticmethod
    def getClinicalTrialsByResearcherId(researcher_id):
        clinical_trials = (
            db.session.query(ClinicalTrials)
            .join(TrialResearchers, TrialResearchers.clinical_trial_id == ClinicalTrials.id)
            .filter(TrialResearchers.researcher_id == researcher_id, ClinicalTrials.status != "deleted")
            .all()
        )

        result = []

        for trial in clinical_trials:
            consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()
            location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()
            meetings_query = Meetings.query.filter_by(
                trial_id=trial.id,
            )

            # Total completed meetings
            total_completed_meetings = meetings_query.filter(Meetings.status == "completed").count()
            trial_data = {
                "id": trial.id,
                "title": trial.title,
                "total_duration": trial.total_duration,
                "status": trial.status,
                "total_visits": trial.total_visits,
                "created_at": trial.created_at,
                "consent": {
                    "id": consent.id,
                    "total_compensation": consent.total_compensation
                } if consent else None,
                "location": {
                    "id": location.id if location else None,
                    "country_name": location.country.name if location and location.country else "",
                    "county_name": location.county.name if location and location.county else "",
                    "city_name": location.city.name if location and location.city else ""
                } if location else None,
                "total_participants": len(trial.trial_participants) if trial.trial_participants else 0,
                "completed_visits": total_completed_meetings
            }

            result.append(trial_data)

        return result


    @staticmethod
    def register_participant(data, participant_id):
        try:
            trial_id = data.get('trial_id')
            if not trial_id:
                raise ValueError("trial_id is required")

            # Check if trial exists
            trial = ClinicalTrials.query.get(trial_id)
            if not trial:
                raise ValueError(f"Clinical trial with id {trial_id} does not exist")

            # Check if already registered (optional)
            existing = TrialParticipants.query.filter_by(
                clinical_trial_id=trial_id, 
                participant_id=participant_id
            ).first()
            if existing:
                raise ValueError("Participant is already registered for this trial")

            # Register participant
            trial_participant = TrialParticipants(
                clinical_trial_id=trial_id,
                participant_id=participant_id
            )
            db.session.add(trial_participant)
            db.session.commit()

            return trial_participant

        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            # You could raise or return an error dict depending on your API style
            return {"error": str(e)}
    
    @staticmethod
    def register_trial_researcher(trial_id, researcher_id):
        try:
            # Check if trial exists
            trial = ClinicalTrials.query.get(trial_id)
            if not trial:
                raise ValueError(f"Clinical trial with id {trial_id} does not exist")

            # Check if researcher exists
            researcher = Researchers.query.get(researcher_id)
            if not researcher:
                raise ValueError(f"Researcher with id {researcher_id} does not exist")

            # Check if already registered
            existing = TrialResearchers.query.filter_by(
                clinical_trial_id=trial_id, 
                researcher_id=researcher_id
            ).first()
            if existing:
                raise ValueError("Researcher is already registered for this trial")

            # Register researcher
            trial_researcher = TrialResearchers(
                clinical_trial_id=trial_id,
                researcher_id=researcher_id
            )
            db.session.add(trial_researcher)
            db.session.commit()

            return trial_researcher

        except (ValueError, SQLAlchemyError) as e:
            db.session.rollback()
            return {"error": str(e)}
        
        from datetime import datetime


    @staticmethod
    def getAllDetailsByClinicalTrailId(trial_id):
        trial = ClinicalTrials.query.get(trial_id)

        if not trial:
            return None  # or raise Exception

        # Researchers
        researchers = [
            {
                "id": tr.researcher.id,
                "full_name": tr.researcher.full_name,
                "email": tr.researcher.email,
                "phone": tr.researcher.phone,
                "research_focus": tr.researcher.research_focus,
                "date_of_birth": tr.researcher.date_of_birth
            }
            for tr in trial.trial_researchers
            if tr.researcher is not None
        ]

        # Participants
        participants = []
        for tp in trial.trial_participants:
            if tp.participant is None:
                continue

            participant_meetings = Meetings.query.filter_by(
                trial_id=trial.id,
                participant_id=tp.participant.id
            )

            # Next upcoming meeting
            next_meeting = participant_meetings.filter(Meetings.meeting_date >= datetime.now(), Meetings.status != "completed") \
                                            .order_by(asc(Meetings.meeting_date)) \
                                            .first()

            # Last completed meeting
            last_meeting = participant_meetings.filter(Meetings.status == "completed") \
                                            .order_by(Meetings.meeting_date.desc()) \
                                            .first()

            participants.append({
                "id": tp.participant.id,
                "full_name": tp.participant.full_name,
                "email": tp.participant.email,
                "status": tp.participant.user.status,
                "joined_at": tp.participant.created_at,
                "next_visit": next_meeting.meeting_date if next_meeting else None,
                "last_visit": last_meeting.meeting_date if last_meeting else None,
                "phone": tp.participant.phone
            })

        # Consent
        consent = TrialConsentInformation.query.filter_by(clinical_trial_id=trial.id).first()

        # Location
        location = ClinicalTrialLocation.query.filter_by(id=trial.clinical_trial_location_id).first()

        # Total completed meetings
        total_completed_meetings = Meetings.query.filter_by(trial_id=trial.id, status="completed").count()

        trial_data = {
            "id": trial.id,
            "title": trial.title,
            "overview": trial.overview,
            "participation_criteria": trial.participation_criteria,
            "visit_details": trial.visit_details,
            "total_duration": trial.total_duration,
            "total_visits": trial.total_visits,
            "status": trial.status,
            "created_by": trial.created_by_researcher.full_name if trial.created_by_researcher else None,
            "created_at": trial.created_at,
            "researchers": researchers,
            "participants": participants,
            "consent": {
                "id": consent.id,
                "risks": consent.risks,
                "benefits": consent.benefits,
                "privacy": consent.privacy,
                "compensation": consent.compensation,
                "rights": consent.rights,
                "safety_contacts": consent.safety_contacts,
                "ethics": consent.ethics,
                "consent_understanding": consent.consent_understanding,
                "total_compensation": consent.total_compensation,
            } if consent else None,
            "location": {
                "id": location.id if location else None,
                "country_name": location.country.name if location and location.country else "",
                "county_name": location.county.name if location and location.county else "",
                "city_name": location.city.name if location and location.city else "",
            } if location else None,
            "completed_visits": total_completed_meetings
        }

        return trial_data


    @staticmethod
    def deleteClinicalTrialById(trial_id, researcher_id):
        """
        Soft delete a clinical trial by updating its status.
        Only the researcher who created the trial can delete it.
        
        Args:
            trial_id (int): ID of the clinical trial to delete
            researcher_id (int): ID of the researcher attempting to delete

        Returns:
            dict: Success message or error details
        """
        try:
            trial = ClinicalTrials.query.get(trial_id)

            if not trial:
                return {"error": f"Clinical trial with id {trial_id} does not exist"}

            # Check ownership
            if trial.created_by_researcher_id != researcher_id:
                return {"error": "You are not authorized to delete this clinical trial"}

            # Soft delete by updating status
            trial.status = "deleted"
            trial.updated_at = datetime.now()  # if you have updated_at field
            db.session.commit()

            return {"message": f"Clinical trial with id {trial_id} has been deleted successfully"}

        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": str(e)}