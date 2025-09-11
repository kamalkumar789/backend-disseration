from datetime import datetime
from app import db

class Researchers(db.Model):
    __tablename__ = "researchers"

    id = db.Column(db.Integer, primary_key=True, index=True)

    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    research_focus = db.Column(db.String, nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)  # <-- added DOB field

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())

    user = db.relationship('Users', back_populates='researchers')
    organization = db.relationship("Organizations", back_populates="researchers")

    clinical_trials_created = db.relationship("ClinicalTrials", back_populates="created_by_researcher")
    trial_researchers = db.relationship("TrialResearchers", back_populates="researcher")
    meetings = db.relationship("Meetings", back_populates="researcher")
