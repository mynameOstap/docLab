from flask import Flask
from config import Config
from .extensions import db


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)

    from .models.customer import Customer
    from .models.consultant import Consultant
    from .models.insurance_product import InsuranceProduct
    from .models.quote_request import QuoteRequest

    from .controllers.main_controller import main_bp
    from .controllers.product_controller import product_bp
    from .controllers.quote_controller import quote_bp
    from .controllers.customer_controller import customer_bp
    from .controllers.consultant_controller import consultant_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(product_bp)
    app.register_blueprint(quote_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(consultant_bp)

    with app.app_context():
        db.create_all()
        seed_data()

    return app


def seed_data():
    from .models.consultant import Consultant
    from .models.insurance_product import InsuranceProduct
    from .models.customer import Customer
    from .models.quote_request import QuoteRequest

    if Consultant.query.count() == 0:
        db.session.add_all([
            Consultant(full_name='Олена Коваль', email='olena@allianz-demo.local', specialization='Travel Risk Insurance'),
            Consultant(full_name='Ігор Мельник', email='ihor@allianz-demo.local', specialization='Premium Medical Travel')
        ])

    if InsuranceProduct.query.count() == 0:
        db.session.add_all([
            InsuranceProduct(
                name='Allianz Travel Basic',
                destination_risk_level='Medium',
                min_age=18,
                max_age=60,
                covers_pre_existing_conditions=False,
                sports_coverage=False,
                emergency_limit=30000,
                daily_price=8.5,
                description='Базова страховка для стандартних туристичних подорожей.'
            ),
            InsuranceProduct(
                name='Allianz Travel Health Protect',
                destination_risk_level='High',
                min_age=18,
                max_age=70,
                covers_pre_existing_conditions=True,
                sports_coverage=False,
                emergency_limit=80000,
                daily_price=16.0,
                description='Розширене медичне покриття для країн з високим ризиком для здоров’я.'
            ),
            InsuranceProduct(
                name='Allianz Extreme Travel Plus',
                destination_risk_level='High',
                min_age=18,
                max_age=65,
                covers_pre_existing_conditions=True,
                sports_coverage=True,
                emergency_limit=120000,
                daily_price=25.0,
                description='Преміум-страхування для високоризикових напрямків та активного відпочинку.'
            )
        ])

    if Customer.query.count() == 0:
        db.session.add_all([
            Customer(full_name='Марія Іванчук', age=34, health_status='stable', country_of_travel='Thailand', has_chronic_disease=False),
            Customer(full_name='Петро Бондар', age=61, health_status='requires_monitoring', country_of_travel='India', has_chronic_disease=True),
        ])

    db.session.commit()

    if QuoteRequest.query.count() == 0:
        customer = Customer.query.first()
        consultant = Consultant.query.first()
        product = InsuranceProduct.query.filter_by(name='Allianz Travel Health Protect').first()
        if customer and consultant and product:
            quote = QuoteRequest(
                customer_id=customer.id,
                consultant_id=consultant.id,
                insurance_product_id=product.id,
                destination_country=customer.country_of_travel,
                trip_days=10,
                health_risk_factor=1.2,
                destination_risk_factor=1.5,
                age_risk_factor=1.1,
                total_price=round(10 * product.daily_price * 1.2 * 1.5 * 1.1, 2),
                payment_status='Paid',
                notes='Тестова заявка після консультації.'
            )
            db.session.add(quote)
            db.session.commit()
