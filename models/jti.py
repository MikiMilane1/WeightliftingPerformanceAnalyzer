from db import db


class ExpiredJTIModel(db.Model):
    __tablename__ = "jtis"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(200), nullable=False, unique=True)