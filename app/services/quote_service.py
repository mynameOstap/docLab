from ..extensions import db
from ..models.quote_request import QuoteRequest
from ..models.insurance_product import InsuranceProduct


class QuoteCalculationService:
    HIGH_RISK_COUNTRIES = {'India', 'Thailand', 'Brazil', 'Kenya', 'Indonesia', 'Mexico'}

    @staticmethod
    def calculate_age_factor(age: int) -> float:
        if age < 18:
            return 1.3
        if age <= 40:
            return 1.0
        if age <= 60:
            return 1.2
        return 1.5

    @staticmethod
    def calculate_health_factor(health_status: str, has_chronic_disease: bool) -> float:
        factor = 1.0
        if health_status == 'requires_monitoring':
            factor += 0.2
        if health_status == 'high_risk':
            factor += 0.4
        if has_chronic_disease:
            factor += 0.2
        return factor

    @staticmethod
    def calculate_destination_factor(country: str) -> float:
        return 1.5 if country in QuoteCalculationService.HIGH_RISK_COUNTRIES else 1.0

    @staticmethod
    def calculate_total(product: InsuranceProduct, age: int, health_status: str, has_chronic_disease: bool, destination_country: str, trip_days: int) -> dict:
        age_factor = QuoteCalculationService.calculate_age_factor(age)
        health_factor = QuoteCalculationService.calculate_health_factor(health_status, has_chronic_disease)
        destination_factor = QuoteCalculationService.calculate_destination_factor(destination_country)
        total = round(product.daily_price * trip_days * age_factor * health_factor * destination_factor, 2)
        return {
            'age_risk_factor': age_factor,
            'health_risk_factor': health_factor,
            'destination_risk_factor': destination_factor,
            'total_price': total,
        }


class QuoteService:
    @staticmethod
    def get_all():
        return QuoteRequest.query.order_by(QuoteRequest.id.desc()).all()

    @staticmethod
    def get_by_id(quote_id: int):
        return QuoteRequest.query.get_or_404(quote_id)

    @staticmethod
    def create(data: dict):
        quote = QuoteRequest(**data)
        db.session.add(quote)
        db.session.commit()
        return quote

    @staticmethod
    def update(quote: QuoteRequest, data: dict):
        for key, value in data.items():
            setattr(quote, key, value)
        db.session.commit()
        return quote

    @staticmethod
    def delete(quote: QuoteRequest):
        db.session.delete(quote)
        db.session.commit()
