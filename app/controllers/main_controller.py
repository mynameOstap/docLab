from flask import Blueprint, render_template
from ..models.insurance_product import InsuranceProduct
from ..models.quote_request import QuoteRequest
from ..models.customer import Customer
from ..models.consultant import Consultant

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    stats = {
        'products': InsuranceProduct.query.count(),
        'quotes': QuoteRequest.query.count(),
        'customers': Customer.query.count(),
        'consultants': Consultant.query.count(),
    }
    featured_products = InsuranceProduct.query.order_by(InsuranceProduct.daily_price.desc()).limit(3).all()
    return render_template('index.html', stats=stats, featured_products=featured_products)
