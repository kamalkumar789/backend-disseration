from flask import Blueprint, request, jsonify, session
from app.models.organizations import Organizations
from app.models.users import Users
from app.services.organizations_service import OrganizationsService
from app.services.researchers_service import ResearchersService
from app.services.participants_service import ParticipantsService

participants_bp = Blueprint('participants_bp', __name__)

@participants_bp.route('/participant/details', methods=['GET'])
def get_participant_details():
    try:
        user_id = session.get('user_id')
        participant_id = session.get('profile_id')

        if not user_id or not participant_id:
            return jsonify({'error': 'user_id and participant_id are required in session'}), 400

        participant_details = ParticipantsService.get_full_participant_details(user_id, participant_id)

        if not participant_details:
            return jsonify({'message': 'No participant found'}), 404

        return jsonify(participant_details), 200

    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500


@participants_bp.route('/participants/update-field', methods=['PATCH'])
def update_profile_details():
    try:
        user_id = session.get('user_id')
        participant_id = session.get('profile_id')
        data = request.json

        if not user_id or not participant_id:
            return jsonify({'error': 'user_id and participant_id are required in session'}), 400

        participant_details = ParticipantsService.update_profile_details(user_id, participant_id, data)

        if not participant_details:
            return jsonify({'message': 'No participant found'}), 404

        return jsonify(participant_details), 200

    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500
