from app._init_ import db

class Researchers(db.Model):
    __tablename__ = "researchers"

    id = db.Column(db.Integer, primary_key=True, index=True)

    full_name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)

    department = db.Column(db.String, nullable=True)
    role = db.Column(db.String, nullable=True)
    research_focus = db.Column(db.String, nullable=True)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), unique=True, nullable=False)
    organization_id = db.Column(db.Integer, db.ForeignKey("organizations.id"), nullable=False)

    account = db.relationship('Accounts', back_populates='researchers')
    organization = db.relationship("Organizations", back_populates="researchers")