from app import db
from datetime import datetime

class ClinicalTrials(db.Model):
    __tablename__ = 'clinical_trials'

    id = db.Column(db.Integer, primary_key=True)
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=False)
    title = db.Column(db.Text, nullable=False)
    createdByResearcher_id = db.Column(db.Integer, db.ForeignKey('researchers.id'), nullable=False)
    overview = db.Column(db.Text, nullable=False)
    participation_criteria = db.Column(db.Text, nullable=False)
    visit_details = db.Column(db.String, nullable=False)

    # Location info (New Fields)
    address = db.Column(db.String(255), nullable=True)  # Optional street address
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=True)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=True)

    # Optional FK to a separate location table (if needed)
    clinical_trial_location_id = db.Column(
        db.Integer, db.ForeignKey('clinical_trial_locations.id'), nullable=True
    )

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())
    status = db.Column(db.String)

    # Relationships
    organization = db.relationship("Organizations", back_populates="clinical_trials")
    created_by_researcher = db.relationship("Researchers", back_populates="clinical_trials_created")
    trial_consent_information = db.relationship("TrialConsentInformation", back_populates="clinical_trial", uselist=False)
    trial_participants = db.relationship("TrialParticipants", back_populates="clinical_trial")
    trial_researchers = db.relationship("TrialResearchers", back_populates="clinical_trial")

    city = db.relationship("City")
    county = db.relationship("County")
    country = db.relationship("Country")
