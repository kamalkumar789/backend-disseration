
from datetime import datetime
from app import db
from datetime import datetime

class Participants(db.Model):
    
    __tablename__ = 'participants'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    full_name = db.Column(db.String)
    postcode = db.Column(db.String)
    email = db.Column(db.String)
    phone = db.Column(db.String)
    date_of_birth = db.Column(db.Date, nullable=True) 

    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())

    user = db.relationship("Users", back_populates="participants")
    medical_info = db.relationship("MedicalInfo", back_populates="participant", uselist=False)
    trial_preferences = db.relationship("TrialPreferences", back_populates="participant", uselist=False)
    trial_participants = db.relationship("TrialParticipants", back_populates="participant")
    meetings = db.relationship("Meetings", back_populates="participant")

