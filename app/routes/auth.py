from flask import Blueprint, request, jsonify, session

from app.models.accounts import Accounts
from app.models.participants_profile import ParticipantsProfile
from app.models.medical_info import MedicalInfo
from app.models.trial_preferences import TrialPreferences

from app._init_ import db
from app.services.auth_service import AuthService
from app.services.organizations_service import OrganizationsService
from app.services.participants_service import ParticipantsService
from app.services.researchers_service import ResearchersService


auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'userType' not in data or 'data' not in data:
        return jsonify({"error": "Invalid request payload"}), 400

    user_type = data['userType']
    user_data = data['data']

    try:
        account = AuthService.create_account({
            'username': user_data['username'],
            'consent': user_data['consent'],
            'userType': user_type,
            'password': user_data['password']
        })

        if user_type == 'participant':
            ParticipantsService.create_participant_profile(account, user_data)
            ParticipantsService.create_medical_info(account, user_data)
            ParticipantsService.create_trial_preferences(account, user_data)

        elif user_type == 'researcher':
            ResearchersService.create_researcher(account, user_data)

        elif user_type == 'organization':
            OrganizationsService.create_organization(account, user_data)

        db.session.commit()

        session['account_id'] = account.id

        return jsonify({
            "message": "Registration successful",
            "accountId": account.id,
            "username": account.username,
            "userType": account.user_type
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({'error': 'email and password required'}), 400

    acc = Accounts.query.filter_by(email=email).first()
    if not acc:
        return jsonify({'error': 'This user is not registered'}), 400

    if not Accounts.verify_password(password):
        return jsonify({'error': 'Invalid password'}), 401

    session['account_id'] = Accounts.id

    return jsonify({'message': 'User logged in successfully'})


@auth_bp.route('/whoami', methods=['POST'])
def whoami():
    account_id = session.get('account_id')

    if not account_id:
        return jsonify({'error': 'Session not active'}), 400

    session['account_id'] = account_id

    return jsonify({'message': 'User logged in successfully', 'account_id': account_id})


@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.clear() 
    return jsonify({'message': 'Logged out successfully'}), 200