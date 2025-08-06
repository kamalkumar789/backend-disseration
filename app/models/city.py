from app import db

class City(db.Model):
    __tablename__ = 'cities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    county_id = db.Column(db.Integer, db.ForeignKey('counties.id'), nullable=False)
    clinical_trials = db.relationship('ClinicalTrials', backref='city', lazy=True)

    def __repr__(self):
        return f"<City {self.name}>"