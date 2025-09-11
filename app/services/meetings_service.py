from app import db
from app.models.meetings import Meetings
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from sqlalchemy.orm import joinedload

class MeetingsService:

    @staticmethod
    def create_meeting(researcher_id, data):
        try:
            
            print(data['meeting_type'])
            # Restrict meeting_type
            if data['meeting_type'] not in ['online', 'in-person']:
                return None, "meeting_type must be either 'online' or 'in_person'"

            # Status default
            status = data.get('status', 'scheduled')
            if status not in ['scheduled', 'completed', 'cancelled']:
                return None, "status must be one of: scheduled, completed, cancelled"

            # Create meeting
            meeting = Meetings(
                description=data['description'],
                meeting_date=data['meeting_date'],
                meeting_location=data['meeting_location'],
                meeting_type=data['meeting_type'],
                status=status,
                trial_id=data['trial_id'],
                participant_id=data['participant_id'],
                researcher_id=researcher_id
            )

            db.session.add(meeting)
            db.session.commit()
            return meeting, None

        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Database error: {str(e)}"
        except Exception as e:
            return None, str(e)

    @staticmethod
    def get_meetings_by_researcher(researcher_id: int):
        try:
            meetings_query = (
                db.session.query(Meetings)
                .options(
                    joinedload(Meetings.participant),  # Load participant details
                    joinedload(Meetings.trial),        # Load trial details
                )
                .filter(Meetings.researcher_id == researcher_id)
                .order_by(Meetings.meeting_date.asc())
                .all()
            )

            result = []
            for m in meetings_query:
                # Split date and time for frontend
        
                result.append({
                    "id": m.id,
                    "participant": {
                        "id": m.participant.id,
                        "name": m.participant.full_name,
                        "email": m.participant.email,
                        "phone": m.participant.phone,
                    },
                    "trial": {
                        "id": m.trial.id,
                        "title": m.trial.title,
                    },
                    "meeting_date": m.meeting_date,
                    "meeting_type": m.meeting_type,
                    "meeting_location": m.meeting_location,
                    "status": m.status,
                    "description": m.description,
                    "created_at": m.created_at.isoformat(),
                })

            return result, None
        except Exception as e:
            db.session.rollback()
            return None, str(e)

    @staticmethod
    def get_trials_with_meetings_by_participant(participant_id: int):
        try:
            # Query all meetings of this participant (with trial + researcher info)
            meetings_query = (
                db.session.query(Meetings)
                .options(
                    joinedload(Meetings.trial),       
                    joinedload(Meetings.researcher),  
                )
                .filter(Meetings.participant_id == participant_id)
                .order_by(Meetings.meeting_date.asc())
                .all()
            )

            # Group meetings under trials
            trials_dict = {}
            for m in meetings_query:
                if m.trial.id not in trials_dict:
                    trials_dict[m.trial.id] = {
                        "trial": {
                            "id": m.trial.id,
                            "title": m.trial.title,
                        },
                        "meetings": []
                    }

                trials_dict[m.trial.id]["meetings"].append({
                    "id": m.id,
                    "meeting_date": m.meeting_date,
                    "meeting_type": m.meeting_type,
                    "meeting_location": m.meeting_location,
                    "status": m.status,
                    "description": m.description,
                    "created_at": m.created_at.isoformat(),
                    "researcher": {
                        "id": m.researcher.id,
                        "name": m.researcher.full_name,
                        "email": m.researcher.email,
                    } if m.researcher else None
                })

            return list(trials_dict.values()), None

        except Exception as e:
            db.session.rollback()
            return None, str(e)
    
    
    
    @staticmethod
    def update_meeting_status(meeting_id: int, new_status: str):
        try:

            meeting = db.session.query(Meetings).filter_by(id=meeting_id).first()
            if not meeting:
                return None, f"Meeting with id {meeting_id} not found"

            # Update status
            meeting.status = new_status
            meeting.updated_at = datetime.now()  # assuming you have updated_at column
            db.session.commit()

            return {
                "id": meeting.id,
                "status": meeting.status,
                "updated_at": meeting.updated_at.isoformat()
            }, None

        except SQLAlchemyError as e:
            db.session.rollback()
            return None, f"Database error: {str(e)}"
        except Exception as e:
            db.session.rollback()
            return None, str(e)

