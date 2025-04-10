from app.extensions import db

class Card(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.Text, nullable=True)
    name = db.Column(db.String(120), nullable=False)
    surname = db.Column(db.String(120), nullable=True)
    job = db.Column(db.String(120), nullable=True)
    company_name = db.Column(db.String(120), nullable=True)
    phones = db.Column(db.PickleType, nullable=True)
    email = db.Column(db.PickleType, nullable=True)
    address = db.Column(db.String(255), nullable=True)
    websites = db.Column(db.PickleType, nullable=True)
    social_medias = db.Column(db.PickleType, nullable=True)
    competencies = db.Column(db.Text, nullable=True)
    talk_info = db.Column(db.PickleType, nullable=True)

class UserCard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    card_id = db.Column(db.Integer, db.ForeignKey('card.id'), nullable=False)