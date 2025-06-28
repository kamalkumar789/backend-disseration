from app._init_ import db


class MedicalInfo(db.Model):
    __tablename__ = 'medical_info'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiving_treatment = db.Column(db.Boolean, nullable=False)
    mental_health_conditions = db.Column(db.Text)
    current_medications = db.Column(db.Text)
    physical_conditions = db.Column(db.Text)
    participated_before = db.Column(db.Boolean, nullable=False)