from app._init_ import db
from app.models.medical_info import MedicalInfo
from app.models.participants_profile import ParticipantsProfile
from app.models.trial_preferences import TrialPreferences

class ParticipantsService:
    @staticmethod
    def create_participant_profile(account, data):
        profile = ParticipantsProfile(
            account_id=account.id,
            full_name=data['fullName'],
            postcode=data.get('postCode'),
            email=data['email'],
            phone=data.get('phone')
        )
        db.session.add(profile)

    @staticmethod
    def create_medical_info(account, data):
        med_info = MedicalInfo(
            account_id=account.id,
            receiving_treatment=data.get['currentlyReceivingTreatment'],
            mental_health_conditions=data.get('mentalHealthConditions'),
            current_medications=data.get('currentMedications'),
            physical_conditions=data.get('physicalHealthConditions'),
            participated_before=data.get('previousTrialParticipation', False)
        )
        db.session.add(med_info)

    @staticmethod
    def create_trial_preferences(account, data):
        trial_pref = TrialPreferences(
            account_id=account.id,
            preferred_location=data.get('preferredLocation'),
            availability=data.get('availability'),
            contact_by_researchers=data.get('contactByResearchers', False),
            trial_length_preference=data.get('trialPreference'),
            willing_interviews=data['willingToUndergo'].get('interviews', False),
            willing_surveys=data['willingToUndergo'].get('surveys', False),
            willing_medication=data['willingToUndergo'].get('medication', False),
            willing_mri=data['willingToUndergo'].get('mri', False)
        )
        db.session.add(trial_pref)
