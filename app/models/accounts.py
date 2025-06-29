from app._init_ import db
from werkzeug.security import generate_password_hash, check_password_hash


class Accounts(db.Model):
    __tablename__ = 'accounts'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    consent = db.Column(db.Boolean, nullable=False)
    user_type = db.Column(db.String(50), nullable=False)

    profile = db.relationship('ParticipantsProfile', back_populates='account', uselist=False)
    medical_infos = db.relationship('MedicalInfo', back_populates='account', lazy=True)
    trial_preference = db.relationship('TrialPreferences', back_populates='account', uselist=False)
    researchers = db.relationship('Researchers', back_populates='account', uselist=False)
    organizations = db.relationship('Organizations', back_populates='account', uselist=False)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)