from app import db


class County(db.Model):
    __tablename__ = 'counties'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'), nullable=False)
    cities = db.relationship('City', backref='county', lazy=True)

    def __repr__(self):
        return f"<County {self.name}>"