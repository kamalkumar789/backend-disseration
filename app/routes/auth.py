from flask import Blueprint, request, jsonify, session

from app.models.users import Users
from app.models.participants_profile import ParticipantsProfile
from app.models.medical_info import MedicalInfo
from app.models.trial_preferences import TrialPreferences

from app._init_ import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    # Basic user info
    username = data.get('username')
    password = data.get('password')
    consent = data.get('consent', False)
    user_type = data.get('userType', None)

    profile_data = data.get('profile', {})
    email = profile_data.get('email')

    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400

    if ParticipantsProfile.query.filter_by(email=email).first():
        return jsonify({'error': 'email already exists'}), 400

    user = Users(username=username, consent=consent, user_type=user_type)
    user.set_password(password)

    profile = ParticipantsProfile(
        full_name=profile_data.get('fullName'),
        postcode=profile_data.get('postcode'),
        email=profile_data.get('email'),
        phone=profile_data.get('phone'),
        user=user
    )

    medical_data = data.get('medicalInfo', {})
    medical_info = MedicalInfo(
        receiving_treatment=medical_data.get('receivingTreatment', False),
        mental_health_conditions=medical_data.get('mentalHealthConditions'),
        current_medications=medical_data.get('currentMedications'),
        physical_conditions=medical_data.get('physicalConditions'),
        participated_before=medical_data.get('participatedBefore', False),
        user=user
    )

    trial_data = data.get('trialPreferences', {})
    trial_preferences = TrialPreferences(
        preferred_location=trial_data.get('preferredLocation'),
        availability=trial_data.get('availability'),
        contact_by_researchers=trial_data.get('contactByResearchers', False),
        trial_length_preference=trial_data.get('trialLengthPreference'),
        willing_interviews=trial_data.get('willingInterviews', False),
        willing_surveys=trial_data.get('willingSurveys', False),
        willing_medication=trial_data.get('willingMedication', False),
        willing_mri=trial_data.get('willingMRI', False),
        user=user
    )

    db.session.add(user)
    db.session.add(profile)
    db.session.add(medical_info)
    db.session.add(trial_preferences)
    db.session.commit()

    session['user_id'] = user.id

    return jsonify({'message': 'User registered successfully'})


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = Users.query.filter_by(email=email).first()
    if not user:
        return jsonify({'error': 'This user is not registered'}), 400

    if not user.check_password(password):
        return jsonify({'error': 'Invalid password'}), 401

    session['user_id'] = user.id

    return jsonify({'message': 'User logged in successfully'})


@auth_bp.route('/whoami', methods=['POST'])
def whoami():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Session not active'}), 400

    session['user_id'] = user_id

    return jsonify({'message': 'User logged in successfully', 'user_id': user_id})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear() 
    return jsonify({'message': 'Logged out successfully'}), 200