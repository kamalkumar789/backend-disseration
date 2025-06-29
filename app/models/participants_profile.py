
from app._init_ import db

class ParticipantsProfile(db.Model):
    __tablename__ = 'participants_profile'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), unique=True, nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    postcode = db.Column(db.Text, nullable=True)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=True)

    account = db.relationship('Accounts', back_populates='profile')