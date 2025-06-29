from app._init_ import db

class Organizations(db.Model):
    __tablename__ = "organizations"

    id = db.Column(db.Integer, primary_key=True, index=True)

    organization_name = db.Column(db.String, nullable=False)
    legal_entity_type = db.Column(db.String, nullable=False)

    registered_address = db.Column(db.String, nullable=False)
    official_email = db.Column(db.String, nullable=False, unique=True)

    contact_full_name = db.Column(db.String, nullable=False)
    contact_designation = db.Column(db.String, nullable=False)
    contact_phone = db.Column(db.String, nullable=False)

    account_id = db.Column(db.Integer, db.ForeignKey('accounts.id'), unique=True, nullable=False)

    account = db.relationship('Accounts', back_populates='organizations')
    researchers = db.relationship("Researchers", back_populates="organization")