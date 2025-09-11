from app import db
from datetime import datetime

class ClinicalTrials(db.Model):
    __tablename__ = 'clinical_trials'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    created_by_researcher_id = db.Column(
        'createdByResearcher_id', db.Integer, db.ForeignKey('researchers.id'), nullable=False
    )    
    overview = db.Column(db.Text, nullable=False)
    participation_criteria = db.Column(db.Text, nullable=False)
    visit_details = db.Column(db.String, nullable=False)
    total_duration = db.Column(db.String)
    total_visits = db.Column(db.Integer, nullable=True, default=0)

    clinical_trial_location_id = db.Column(
        db.Integer, db.ForeignKey('clinical_trial_locations.id'), nullable=True
    )

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # No parentheses!
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
    status = db.Column(db.String)

    # Relationships
    organization = db.relationship("Organizations", back_populates="clinical_trials")
    created_by_researcher = db.relationship("Researchers", back_populates="clinical_trials_created")
    trial_consent_information = db.relationship("TrialConsentInformation", back_populates="clinical_trial", uselist=False)
    trial_participants = db.relationship("TrialParticipants", back_populates="clinical_trial")
    trial_researchers = db.relationship("TrialResearchers", back_populates="clinical_trial")
    meetings = db.relationship("Meetings", back_populates="trial")

    # Relationship to location
    location = db.relationship("ClinicalTrialLocation", back_populates="clinical_trials")