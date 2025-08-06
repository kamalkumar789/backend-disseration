
from app import db

class TrialParticipants(db.Model):
    __tablename__ = 'trial_participants'
    id = db.Column(db.Integer, primary_key=True)
    clinical_trial_id = db.Column(db.Integer, db.ForeignKey('clinical_trials.id'), nullable=False)
    participant_id = db.Column(db.Integer, db.ForeignKey('participants.id'), nullable=False)
    created_at = db.Column(db.Date)
    status = db.Column(db.String)

    clinical_trial = db.relationship("ClinicalTrials", back_populates="trial_participants")
    participant = db.relationship("Participants", back_populates="trial_participants")
