from flask import Blueprint, request, jsonify, session
from app.services.meetings_service import MeetingsService

meetings_bp = Blueprint('meetings_bp', __name__)

@meetings_bp.route('/meetings', methods=['POST'])
def schedule_meeting():
    researcher_id = session.get('profile_id')
    if not researcher_id:
        return jsonify({'error': 'Researcher ID (profile_id) missing from session'}), 400

    data = request.get_json()
    meeting, error = MeetingsService.create_meeting(researcher_id, data)

    if error:
        return jsonify({'error': error}), 400

    return jsonify({
        'message': 'Meeting scheduled successfully',
        'meeting': {
            'id': meeting.id,
            'description': meeting.description,
            'meeting_date': meeting.meeting_date.isoformat(),
            'meeting_location': meeting.meeting_location,
            'meeting_type': meeting.meeting_type,
            'status': meeting.status,
            'trial_id': meeting.trial_id,
            'participant_id': meeting.participant_id,
            'researcher_id': meeting.researcher_id
        }
    }), 201


@meetings_bp.route('/researcher/meetings', methods=['GET'])
def get_researcher_meetings():
    researcher_id = session.get('profile_id')
    if not researcher_id:
        return jsonify({"error": "Researcher ID missing from session"}), 400

    meetings, error = MeetingsService.get_meetings_by_researcher(researcher_id)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"message": "Successfully fetched all meetings", "data": meetings}), 200


@meetings_bp.route("/<int:meeting_id>/status", methods=["PUT"])
def update_status(meeting_id):
    data = request.get_json()
    status = data.get("status")

    result, error = MeetingsService.update_meeting_status(meeting_id, status)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(result), 200


@meetings_bp.route('/participant/meetings', methods=['GET'])
def get_participant_meetings():
    participant_id = session.get('profile_id')
    if not participant_id:
        return jsonify({"error": "Participant ID missing from session"}), 400

    meetings, error = MeetingsService.get_trials_with_meetings_by_participant(participant_id)
    if error:
        return jsonify({"error": error}), 500

    return jsonify({"message": "Successfully fetched all meetings", "data": meetings}), 200