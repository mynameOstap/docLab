from ..extensions import db
from ..models.customer import Customer


class CustomerService:
    @staticmethod
    def get_all():
        return Customer.query.order_by(Customer.id.desc()).all()

    @staticmethod
    def get_by_id(customer_id: int):
        return Customer.query.get_or_404(customer_id)

    @staticmethod
    def create(data: dict):
        customer = Customer(**data)
        db.session.add(customer)
        db.session.commit()
        return customer

    @staticmethod
    def update(customer: Customer, data: dict):
        for key, value in data.items():
            setattr(customer, key, value)
        db.session.commit()
        return customer

    @staticmethod
    def delete(customer: Customer):
        db.session.delete(customer)
        db.session.commit()
