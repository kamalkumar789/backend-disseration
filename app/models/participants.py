
from app import db

class Participants(db.Model):
    
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String)
    postcode = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)

    user = db.relationship("Users", back_populates="participants")
    medical_info = db.relationship("MedicalInfo", back_populates="participant", uselist=False)
    trial_preferences = db.relationship("TrialPreferences", back_populates="participant", uselist=False)
    trial_participants = db.relationship("TrialParticipants", back_populates="participant")
