from app import db


class Country(db.Model):
    __tablename__ = 'countries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    counties = db.relationship('County', backref='country', lazy=True)
    clinical_trials = db.relationship('ClinicalTrials', backref='country', lazy=True)

    def __repr__(self):
        return f"<Country {self.name}>"