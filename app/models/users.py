from app._init_ import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    consent = db.Column(db.Boolean, nullable=False)
    user_type = db.Column(db.String(50), nullable=False)

    profile = db.relationship('ParticipantsProfile', backref='user', uselist=False)
    medical_infos = db.relationship('MedicalInfo', backref='user', lazy=True)
    trial_preference = db.relationship('TrialPreferences', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
