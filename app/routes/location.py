from flask import Blueprint, request, jsonify, session
from app.models.city import City
from app.models.country import Country
from app.models.county import County
from app.services.clinical_trial_service import ClinicalTrialService
from app.services.researchers_service import ResearchersService
from app import db

location_bp = Blueprint('location_bp', __name__)



@location_bp.route('/location/countries', methods=['GET'])
def get_all_countries():
    try:
        user_id = session.get('user_id')
        researcher_id = session.get('profile_id')

        countries = Country.query.all()
        result = [{'id': country.id, 'name': country.name} for country in countries]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500


@location_bp.route('/location/counties', methods=['GET'])
def get_all_counties():
    try:
        country_id = request.args.get('country_id', type=int)
        if not country_id:
            return jsonify({'error': 'Missing or invalid country_id'}), 400

        counties = County.query.filter_by(country_id=country_id).all()
        result = [{'id': county.id, 'name': county.name, 'country_id': country_id} for county in counties]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500



@location_bp.route('/location/cities', methods=['GET'])
def get_all_cities():
    try:
        county_id = request.args.get('county_id', type=int)
        if not county_id:
            return jsonify({'error': 'Missing or invalid county_id'}), 400

        cities = City.query.filter_by(county_id=county_id).all()
        result = [{'id': city.id, 'name': city.name, 'county_id': county_id} for city in cities]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500
