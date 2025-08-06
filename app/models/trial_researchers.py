
from app import db

class TrialResearchers(db.Model):
    
    __tablename__ = 'trial_researchers'

    id = db.Column(db.Integer, primary_key=True)
    clinical_trial_id = db.Column(db.Integer, db.ForeignKey('clinical_trials.id'), nullable=False)
    researcher_id = db.Column(db.Integer, db.ForeignKey('researchers.id'), nullable=False)

    clinical_trial = db.relationship("ClinicalTrials", back_populates="trial_researchers")
    researcher = db.relationship("Researchers", back_populates="trial_researchers")
