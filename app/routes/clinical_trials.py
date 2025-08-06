from flask import Blueprint, request, jsonify, session
from app.services.clinical_trial_service import ClinicalTrialService
from app.services.researchers_service import ResearchersService
from app import db

clinicaltrials_bp = Blueprint('clinicaltrials_bp', __name__)



@clinicaltrials_bp.route('/create/clinical-trials', methods=['POST',])
def createClinicalTrials():
    try:
        user_id = session.get('user_id')
        researcher_id = session.get('profile_id')
        data = request.json

        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        researcher = ResearchersService.getResearcherByUserId(userId=user_id)

        print(researcher.id)
        print(researcher.organization_id)

        clinicaltrial = ClinicalTrialService.createClinicalTrial(data=data, organization_id=researcher.organization_id, researcher_id=researcher_id)
        consentTrial = ClinicalTrialService.createClinicalTrialsConsent(data=data, clinical_trial_id=clinicaltrial.id)

        db.session.commit()

        return jsonify({
            'message': 'Clinical trial created successfully',
            'clinicaltrial_id': clinicaltrial.id
        }), 201

    except Exception as e:
        return jsonify({'error': 'An error occurred while creating clinical trial', 'details': str(e)}), 500



@clinicaltrials_bp.route('/clinical-trials', methods=['GET'])
def get_all_clinical_trials():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        clinical_trials = ClinicalTrialService.getAllClinicalTrials()
        return jsonify({
            'message': 'All clinical trials fetched successfully',
            'data': clinical_trials
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error fetching clinical trials',
            'details': str(e)  # 🔒 Consider hiding in prod
        }), 500
    

@clinicaltrials_bp.route('/organizations/<int:organization_id>/clinical-trials', methods=['GET'])
def get_clinical_trials_by_organization(organization_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        clinical_trials = ClinicalTrialService.getAllClinicalTrialsByOrganizationId(organization_id)
        return jsonify({
            'message': f'Clinical trials for organization {organization_id} fetched successfully',
            'data': clinical_trials
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error fetching organization clinical trials',
            'details': str(e)
        }), 500
    

@clinicaltrials_bp.route('/clinical-trials/<int:trial_id>', methods=['GET'])
def get_clinical_trial_by_id(trial_id):
    try:
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Session not active'}), 401

        trial = ClinicalTrialService.getClinicalTrialsById(trial_id)
        return jsonify({
            'message': f'Clinical trial {trial_id} fetched successfully',
            'data': trial
        }), 200

    except Exception as e:
        return jsonify({
            'error': 'Error fetching clinical trial',
            'details': str(e)
        }), 500