from flask import Blueprint, request, jsonify, session
from app.models.organizations import Organizations
from app.models.users import Users
from app.services.email_service import send_email
from app.services.organizations_service import OrganizationsService
from app.services.researchers_service import ResearchersService
from app import db


organization_bp = Blueprint('organization_bp', __name__)



@organization_bp.route('/organizations', methods=['GET'])  # Change to POST
def allOrganizations():

    organizations = Organizations.query.all()

    orgs_data = [{'id': org.id, 'organizationName': org.organization_name} for org in organizations]

    return jsonify({'message': 'User logged in successfully', 'organizations': orgs_data})


@organization_bp.route('/create/organization', methods=['POST'])
def createOrganization():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        organization = OrganizationsService.create_organization(user, data)
        
        db.session.commit()

        return jsonify({
            'message': 'Organization created successfully',
            'organization_id': organization.id
        }), 201

    except Exception as e:
        db.session.rollback()  # Uncomment if you use db.session
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    

@organization_bp.route('/researchers/status', methods=['PUT'])
def approveResearchers():
    try:
        user_id = session.get('user_id')
        profile_id = session.get('profile_id')
        data = request.json
        
        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404

        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        researcher = ResearchersService.updateStatus(researcher_id=data['researcher_id'], status=data['status'])
        db.session.commit()

        print('sending email to, ', researcher.email)
        send_email(researcher.email, status=data['status'])

        return jsonify({
            'message': 'Status updated successfully',
            'researcher_id': researcher.id
        }), 201

    except Exception as e:
        db.session.rollback()  # Uncomment if you use db.session
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    

@organization_bp.route('/organization/details', methods=['GET'])
def get_organization_dashboard_details():
    try:
        profile_id = session.get('profile_id')
        if not profile_id:
            return jsonify({'error': 'Session not active or missing identifiers'}), 401

        # Fetch full organization details
        dashboard_data = OrganizationsService.getOrganizationDetails(profile_id)
        if not dashboard_data:
            return jsonify({'error': 'Organization not found'}), 404

        return jsonify(dashboard_data), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    


@organization_bp.route('/organizations/dashboard/details', methods=['GET']) 
def getAllOrganizationParticipants():

    try:
        user_id = session.get('user_id')
        profile_id = session.get('profile_id')
        organization = OrganizationsService.getOrganizationDashDetails(organizationId=profile_id)
        return organization
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500



@organization_bp.route('/<int:organization_id>/trials', methods=['GET'])
def get_trials_by_organization(organization_id):
    """
    GET /api/organizations/<organization_id>/trials
    Fetch all clinical trials for a given organization
    """
    trials = OrganizationsService.getTrialsByOrganizationId(organization_id)
    return jsonify(trials), 200



@organization_bp.route('/organization/update-field', methods=['PATCH'])
def update_profile_details():
    try:
        user_id = session.get('user_id')
        organization_id = session.get('profile_id')
        data = request.json

        if not user_id or not organization_id:
            return jsonify({'error': 'user_id and organization_id are required in session'}), 400

        organization_details = OrganizationsService.update_organization_details(user_id, organization_id, data)

        if not organization_details:
            return jsonify({'message': 'No organization found'}), 404

        return jsonify(organization_details), 200

    except Exception as e:
        return jsonify({
            'error': 'An unexpected error occurred',
            'details': str(e)
        }), 500
