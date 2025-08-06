from app import db

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