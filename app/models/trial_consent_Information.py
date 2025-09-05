
from app import db
from datetime import datetime


class TrialConsentInformation(db.Model):
    __tablename__ = 'trial_consent_information'
    id = db.Column(db.Integer, primary_key=True)
    clinical_trial_id = db.Column(db.Integer, db.ForeignKey('clinical_trials.id'), nullable=False)
    risks = db.Column(db.Text)
    benefits = db.Column(db.Text)
    privacy = db.Column(db.Text)
    compensation = db.Column(db.String)
    rights = db.Column(db.Text)
    safety_contacts = db.Column(db.Text)
    ethics = db.Column(db.Text)
    consent_understanding = db.Column(db.Text)
    total_compensation = db.Column(db.Integer)
    clinical_trial = db.relationship("ClinicalTrials", back_populates="trial_consent_information")
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())
