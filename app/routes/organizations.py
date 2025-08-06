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
def get_organization_details():
    try:
        user_id = session.get('user_id')
        profile_id = session.get('profile_id')

        if not user_id or not profile_id:
            return jsonify({'error': 'Session not active or missing identifiers'}), 401
        
        # Fetch user details from users table
        user = Users.query.filter_by(id=user_id).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Fetch organization details using profile_id
        organization = OrganizationsService.getOrganizationDetails(organizationId=profile_id)
        if not organization:
            return jsonify({'error': 'Organization not found'}), 404
        
        # Prepare combined response data
        response_data = {
            'userId': user.id,
            'profileId': profile_id,
            'username': user.username,
            'consent': user.consent,  # assuming this field exists in Users
            
            'organizationName': organization.organization_name,
            'yearOfEstablishment': organization.year_of_establishment,  # assuming this field exists
            'registeredAddress': organization.registered_address,
            'officialEmail': organization.official_email,
            'contactPersonName': organization.contact_full_name,
            'contactPersonDesignation': organization.contact_designation,
            'contactPersonPhone': organization.contact_phone,
            
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500



@organization_bp.route('/organizations/dashboard/details', methods=['GET'])  # Change to POST
def getAllOrganizationParticipants():

    try:
        user_id = session.get('user_id')
        profile_id = session.get('profile_id')
        organization = OrganizationsService.getOrganizationDashDetails(organizationId=profile_id)
        return organization
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500


