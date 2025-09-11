from app import db
from datetime import datetime

class Meetings(db.Model):
    __tablename__ = 'meetings'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text, nullable=True)
    meeting_date = db.Column(db.DateTime, nullable=False)
    meeting_location = db.Column(db.Text, nullable=False)
    meeting_type = db.Column(db.Enum('online', 'in-person', name='meeting_type_enum'), nullable=False)
    status = db.Column(db.Enum('scheduled', 'completed', 'cancelled', name='meeting_status_enum'), default='scheduled', nullable=False)

    # Foreign keys
    trial_id = db.Column(db.Integer, db.ForeignKey('clinical_trials.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    researcher_id = db.Column(db.Integer, db.ForeignKey('researchers.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())

    # Relationships
    trial = db.relationship("ClinicalTrials", back_populates="meetings")
    participant = db.relationship("Participants", back_populates="meetings")
    researcher = db.relationship("Researchers", back_populates="meetings")
