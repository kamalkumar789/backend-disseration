from app._init_ import db


class TrialPreferences(db.Model):
    __tablename__ = 'trial_preferences'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    preferred_location = db.Column(db.String(100), nullable=False)
    availability = db.Column(db.Text)
    contact_by_researchers = db.Column(db.Boolean, nullable=False)
    trial_length_preference = db.Column(db.String(50))
    willing_interviews = db.Column(db.Boolean, nullable=False)
    willing_surveys = db.Column(db.Boolean, nullable=False)
    willing_medication = db.Column(db.Boolean, nullable=False)
    willing_mri = db.Column(db.Boolean, nullable=False)
