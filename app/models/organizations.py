from app import db
from datetime import datetime

class Organizations(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True, index=True)

    organization_name = db.Column(db.String, nullable=False)

    registered_address = db.Column(db.String, nullable=False)
    official_email = db.Column(db.String, nullable=False, unique=True)

    year_of_establishment = db.Column(db.Integer, nullable=True)  # <-- Add this line


    contact_full_name = db.Column(db.String, nullable=False)
    contact_designation = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)

    user = db.relationship('Users', back_populates='organization')
    researchers = db.relationship("Researchers", back_populates="organization")

    clinical_trials = db.relationship('ClinicalTrials', back_populates='organization')

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())
