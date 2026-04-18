from .base import BaseModel
from ..extensions import db


class Consultant(BaseModel):
    __tablename__ = 'consultants'

    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    specialization = db.Column(db.String(120), nullable=False)

    quote_requests = db.relationship('QuoteRequest', back_populates='consultant')
