from .base import BaseModel
from ..extensions import db


class InsuranceProduct(BaseModel):
    __tablename__ = 'insurance_products'

    name = db.Column(db.String(150), nullable=False)
    destination_risk_level = db.Column(db.String(20), nullable=False)
    min_age = db.Column(db.Integer, nullable=False)
    max_age = db.Column(db.Integer, nullable=False)
    covers_pre_existing_conditions = db.Column(db.Boolean, default=False, nullable=False)
    sports_coverage = db.Column(db.Boolean, default=False, nullable=False)
    emergency_limit = db.Column(db.Integer, nullable=False)
    daily_price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)

    quote_requests = db.relationship('QuoteRequest', back_populates='insurance_product')
