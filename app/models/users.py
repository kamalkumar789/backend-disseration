from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model):
    
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    consent = db.Column(db.Boolean, default=False)
    user_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.now(), nullable=False, onupdate=datetime.now())
    status = db.Column(db.String)

    participants = db.relationship("Participants", back_populates="user", uselist=False)
    organization = db.relationship("Organizations", back_populates="user", uselist=False)
    researchers = db.relationship("Researchers", back_populates="user", uselist=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)