from app import db
from app.models.medical_info import MedicalInfo
from app.models.participants import Participants
from app.models.trial_preferences import TrialPreferences
from app.models.trial_participants import TrialParticipants
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from sqlalchemy.orm import joinedload


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
                phone=profile_data.get('phone'),
                date_of_birth=profile_data['dateOfBirth']
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

    @staticmethod
    def get_full_participant_details(user_id: int, participant_id: int):
        try:
            participant = (
                Participants.query
                .options(
                    joinedload(Participants.medical_info),
                    joinedload(Participants.trial_preferences),
                    joinedload(Participants.user),   # load user as well
                )
                .filter_by(user_id=user_id, id=participant_id)
                .first()
            )

            if not participant:
                return None

            user = participant.user  # get linked user object
            total_trials = TrialParticipants.query.filter_by(participant_id=participant.id).count()
            # Build structured response JSON
            return {
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "password": user.password,
                    "role": user.role if hasattr(user, "role") else None,
                    "created_at": user.created_at if hasattr(user, "created_at") else None,
                },
                "profile": {
                    "id": participant.id,
                    "full_name": participant.full_name,
                    "email": participant.email,
                    "phone": participant.phone,
                    "postcode": participant.postcode,
                    "date_of_birth": participant.date_of_birth
                },
                "medical_info": {
                    "id": participant.medical_info.id,
                    "receiving_treatment": participant.medical_info.receiving_treatment if participant.medical_info else None,
                    "mental_health_conditions": participant.medical_info.mental_health_conditions if participant.medical_info else None,
                    "current_medications": participant.medical_info.current_medications if participant.medical_info else None,
                    "physical_conditions": participant.medical_info.physical_conditions if participant.medical_info else None,
                    "participated_before": participant.medical_info.participated_before if participant.medical_info else None,
                },
                "trial_preferences": {
                    "id": participant.trial_preferences.id,
                    "preferred_location": participant.trial_preferences.preferred_location if participant.trial_preferences else None,
                    "availability": participant.trial_preferences.availability if participant.trial_preferences else None,
                    "trial_length_preference": participant.trial_preferences.trial_length_preference if participant.trial_preferences else None,
                    "willing_interviews": participant.trial_preferences.willing_interviews if participant.trial_preferences else None,
                    "willing_surveys": participant.trial_preferences.willing_surveys if participant.trial_preferences else None,
                    "willing_medication": participant.trial_preferences.willing_medication if participant.trial_preferences else None,
                    "willing_mri": participant.trial_preferences.willing_mri if participant.trial_preferences else None,
                }, 
                "participation_count": total_trials,
            }
        except SQLAlchemyError as e:
            print(f"[ERROR] Failed to fetch participant details: {e}")
            raise
    

    @staticmethod
    def update_profile_details(user_id, participant_id, data):
        """
        Update participant profile details.
        `data` should be a dict like:
        {
            "section": "profile" | "user" | "medicalInfo" | "trialPreferences",
            "field": "full_name",
            "value": "New Name"
        }
        """
        try:
            participant = Participants.query.filter_by(
                id=participant_id, user_id=user_id
            ).first()

            if not participant:
                raise ValueError("Participant not found")

            section = data.get("section")
            field = data.get("field")
            value = data.get("value")

            if section == "profile":
                if not hasattr(participant, field):
                    raise ValueError(f"Invalid field '{field}' for profile")
                setattr(participant, field, value)

            elif section == "user":
                user = participant.user
                if not hasattr(user, field):
                    raise ValueError(f"Invalid field '{field}' for user")
                if field == "password":  # use hashing
                    user.set_password(value)
                else:
                    setattr(user, field, value)

            elif section == "medicalInfo":
                medical_info = participant.medical_info
                if not medical_info:
                    medical_info = MedicalInfo(participant_id=participant.id)
                    db.session.add(medical_info)
                if not hasattr(medical_info, field):
                    raise ValueError(f"Invalid field '{field}' for medical info")
                setattr(medical_info, field, value)

            elif section == "trialPreferences":
                prefs = participant.trial_preferences
                if not prefs:
                    prefs = TrialPreferences(participant_id=participant.id)
                    db.session.add(prefs)
                if not hasattr(prefs, field):
                    raise ValueError(f"Invalid field '{field}' for trial preferences")
                setattr(prefs, field, value)

            else:
                raise ValueError(f"Invalid section '{section}'")

            db.session.commit()
            return {"message": f"{section}.{field} updated successfully", "value": value}

        except SQLAlchemyError as e:
            db.session.rollback()
            print(f"[ERROR] Failed to update participant details: {e}")
            raise
