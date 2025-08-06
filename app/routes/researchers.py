from flask import Blueprint, request, jsonify, session
from app.models.organizations import Organizations
from app.models.users import Users
from app.services.organizations_service import OrganizationsService
from app.services.researchers_service import ResearchersService


researchers_bp = Blueprint('researchers_bp', __name__)

@researchers_bp.route('/researchers', methods=['GET'])
def getAllNotApprovedResearchersByOrganization():
    try:
        organization_id = session.get('profile_id')

        if not organization_id:
            return jsonify({'error': 'organization_id is required as a query parameter'}), 400

        researchers = ResearchersService.getAllNotApprovedUsers(organization_id)

        if not researchers:
            return jsonify({'message': 'No unapproved researchers found'}), 200

        result = [{
            'id': r.id,
            'full_name': r.full_name,
            'email': r.email,
            'status': r.user.status,
            'joined_at': r.user.created_at
        } for r in researchers]

        return jsonify({'researchers': result}), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
