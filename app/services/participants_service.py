from app import db
from app.models.medical_info import MedicalInfo
from app.models.participants import Participants
from app.models.trial_preferences import TrialPreferences
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional


class ParticipantsService:
    @staticmethod
    def create_participant_profile(user, data):
        try:
            profile_data = data['profile']
            profile = Participants(
                user_id=user.id,
                full_name=profile_data['fullName'],
                postcode=profile_data.get('postcode'),
                email=profile_data['email'],
                phone=profile_data.get('phone')
            )
            db.session.add(profile)
            db.session.flush()

            return profile
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to create participant profile: {e}")
            raise

    @staticmethod
    def create_medical_info(profile_id, data):
        try:
            medical_info_data = data['medicalInfo']
            print("profile_data", medical_info_data)

            med_info = MedicalInfo(
                participant_id=profile_id,
                receiving_treatment=medical_info_data.get('currentlyReceivingTreatment'),
                mental_health_conditions=medical_info_data.get('mentalHealthConditions'),
                current_medications=medical_info_data.get('currentMedications'),
                physical_conditions=medical_info_data.get('physicalConditions'),
                participated_before=medical_info_data.get('participatedBefore', False)
            )

            db.session.add(med_info)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to create medical info: {e}")
            raise

    @staticmethod
    def create_trial_preferences(profileId, data):
        try:
            trial_preferences_data = data['trialPreferences']

            trial_pref = TrialPreferences(
                participant_id=profileId,
                preferred_location=trial_preferences_data.get('preferredLocation'),
                availability=trial_preferences_data.get('availability'),
                contact_by_researchers=trial_preferences_data.get('contactByResearchers', False),
                trial_length_preference=trial_preferences_data.get('trialLengthPreference'),
                willing_interviews=trial_preferences_data.get('willingInterviews', False),
                willing_surveys=trial_preferences_data.get('willingSurveys', False),
                willing_medication=trial_preferences_data.get('willingMedication', False),
                willing_mri=trial_preferences_data.get('willingMRI', False)
            )
            db.session.add(trial_pref)
        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to create trial preferences: {e}")
            raise


    @staticmethod
    def getParticipantDetails(userId) -> Optional[Participants]:
        try:
            profile = Participants.query.filter_by(userId=userId).first()
            return profile
        except SQLAlchemyError as e:
            print(f"[ERROR] Failed to get participant details: {e}")
            raise