from flask import Blueprint, request, jsonify, session

from app.services.auth_service import AuthService
from app.services.organizations_service import OrganizationsService
from app.services.participants_service import ParticipantsService
from app.services.researchers_service import ResearchersService
from app.models.participants import Participants
from app.models.researchers import Researchers
from app.models.organizations import Organizations
from app.models.users import Users

from app import db


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'userType' not in data or 'data' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    user_type = data['userType']
    user_data = data['data']

    try:
        status = "active"
        
        if(user_type == "researcher"):
            status = "not-verified"

        user = AuthService.create_user(user_type, user_data, status)

        email = ""
        
        profileId = None

        if user_type == 'participant':
            email = user_data["profile"].get("officialEmail")
            participant = ParticipantsService.create_participant_profile(user, user_data)
            profileId = participant.id
            ParticipantsService.create_medical_info(profileId, user_data)
            ParticipantsService.create_trial_preferences(profileId, user_data)

        elif user_type == 'researcher':
            # email = user_data["profile"].get("officialEmail")
            researcher = ResearchersService.create_researcher(user, user_data)
            profileId = researcher.id


        elif user_type == 'organization':
            email = user_data.get("officialEmail")
            organization = OrganizationsService.create_organization(user, user_data)
            profileId = organization.id
            
        db.session.commit()

        session['user_id'] = user.id
        session['profile_id'] = profileId


        if user_type == 'researcher':
            return jsonify({
                "message": "Registration successful, but your account requires verification. You will receive an email once it’s verified.",
            }), 201

        return jsonify({
            "message": "Registration successful",
            "userId": user.id,
            "username": user.username,
            "userType": user.user_type,
            "email": email,
            "profileId": profileId

        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    userType = data.get('userType')

    if not username or not password:
        return jsonify({'error': 'Username and password required'}), 400

    user = Users.query.filter_by(username=username, user_type=userType).first()

    if not user:
        return jsonify({'error': 'This user is not registered'}), 401

    if not user.verify_password(password):
        return jsonify({'error': 'Invalid password'}), 401
    
    if user.status == "not-verified":
        return jsonify({'error': 'This account is not verified. You will be send email once its verified'}), 401
    
    if user.status == "reject":
        return jsonify({'error': 'This account was rejected'}), 401


    profile_id = None
    email = None

    if user.user_type == 'participant':
        participant_profile = Participants.query.filter_by(user_id=user.id).first()
        profile_id = participant_profile.id if participant_profile else None
        email = participant_profile.email if participant_profile else None

    elif user.user_type == 'researcher':
        researcher = Researchers.query.filter_by(user_id=user.id).first()
        profile_id = researcher.id if researcher else None
        email = researcher.email if researcher else None

    elif user.user_type == 'organization':
        organization = Organizations.query.filter_by(user_id=user.id).first()
        profile_id = organization.id if organization else None
        email = organization.official_email if organization else None

    

    session['user_id'] = user.id
    session['profile_id'] = profile_id
    
    return jsonify({
        "message": "login successful",
        "userId": user.id,
        "username": user.username,
        "userType": user.user_type,
        "email": email,
        "profileId": profile_id,
        "status": user.status
    }), 200

@auth_bp.route('/whoami', methods=['POST'])
def whoami():
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'Session not active'}), 401

    session['user_id'] = user_id

    return jsonify({'message': 'User logged in successfully', 'user_id': user_id})


@auth_bp.route('/logout', methods=['GET'])
def logout():
    session.clear() 
    return jsonify({'message': 'Logged out successfully'}), 200