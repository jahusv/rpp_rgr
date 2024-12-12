from __init__ import db
from flask_login import UserMixin

class Subscription(db.Model, UserMixin):
    subscription_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    cost = db.Column(db.Float, nullable=False)
    frequency = db.Column(db.Integer, nullable=False)
    start_date = db.Column(db.Date, nullable=False)