from app import db
from datetime import datetime

class ClinicalTrialLocation(db.Model):
    __tablename__ = 'clinical_trial_locations'

    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255), nullable=True)

    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=True)
    city_id = db.Column(db.Integer, db.ForeignKey('cities.id'), nullable=True)

    country = db.relationship('Country')
    county = db.relationship('County')
    city = db.relationship('City')

    # Relationship back to ClinicalTrials
    clinical_trials = db.relationship(
        "ClinicalTrials",
        back_populates="location",
        cascade="all, delete-orphan"
    )

    created_at = db.Column(db.DateTime, default=datetime.now, nullable=False)  # No parentheses!
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)