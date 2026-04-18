from ..extensions import db
from ..models.insurance_product import InsuranceProduct


class ProductService:
    @staticmethod
    def get_all():
        return InsuranceProduct.query.order_by(InsuranceProduct.id.desc()).all()

    @staticmethod
    def get_by_id(product_id: int):
        return InsuranceProduct.query.get_or_404(product_id)

    @staticmethod
    def create(data: dict):
        product = InsuranceProduct(**data)
        db.session.add(product)
        db.session.commit()
        return product

    @staticmethod
    def update(product: InsuranceProduct, data: dict):
        for key, value in data.items():
            setattr(product, key, value)
        db.session.commit()
        return product

    @staticmethod
    def delete(product: InsuranceProduct):
        db.session.delete(product)
        db.session.commit()
