from .base import BaseModel
from ..extensions import db


class QuoteRequest(BaseModel):
    __tablename__ = 'quote_requests'

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    consultant_id = db.Column(db.Integer, db.ForeignKey('consultants.id'), nullable=True)
    insurance_product_id = db.Column(db.Integer, db.ForeignKey('insurance_products.id'), nullable=False)

    destination_country = db.Column(db.String(80), nullable=False)
    trip_days = db.Column(db.Integer, nullable=False)
    health_risk_factor = db.Column(db.Float, nullable=False)
    destination_risk_factor = db.Column(db.Float, nullable=False)
    age_risk_factor = db.Column(db.Float, nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    payment_status = db.Column(db.String(30), nullable=False, default='Pending')
    notes = db.Column(db.Text, nullable=True)

    customer = db.relationship('Customer', back_populates='quote_requests')
    consultant = db.relationship('Consultant', back_populates='quote_requests')
    insurance_product = db.relationship('InsuranceProduct', back_populates='quote_requests')
