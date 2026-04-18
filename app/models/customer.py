from .base import BaseModel
from ..extensions import db


class Customer(BaseModel):
    __tablename__ = 'customers'

    full_name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    health_status = db.Column(db.String(80), nullable=False)
    country_of_travel = db.Column(db.String(80), nullable=False)
    has_chronic_disease = db.Column(db.Boolean, default=False, nullable=False)

    quote_requests = db.relationship('QuoteRequest', back_populates='customer', cascade='all, delete-orphan')
