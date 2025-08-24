from app import db
from datetime import datetime

class Appointments(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.Text, nullable=True)
    meeting_date = db.Column(db.DateTime, nullable=False)

    # Foreign keys
    trial_id = db.Column(db.Integer, db.ForeignKey('clinical_trials.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    researcher_id = db.Column(db.Integer, db.ForeignKey('researchers.id'), nullable=False)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    trial = db.relationship("ClinicalTrials", back_populates="appointments")
    participant = db.relationship("Participants", back_populates="appointments")
    researcher = db.relationship("Researchers", back_populates="appointments")
