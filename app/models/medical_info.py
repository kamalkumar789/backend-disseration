from app._init_ import db

class MedicalInfo(db.Model):
    __tablename__ = 'medical_infos'

    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), nullable=False)
    receiving_treatment = db.Column(db.Boolean, nullable=False)
    mental_health_conditions = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    physical_conditions = db.Column(db.Text)
    participated_before = db.Column(db.Boolean, nullable=False)

    account = db.relationship('Accounts', back_populates='medical_infos')