from flask import Blueprint, render_template, request, redirect, url_for
from ..services.quote_service import QuoteService, QuoteCalculationService
from ..services.customer_service import CustomerService
from ..services.consultant_service import ConsultantService
from ..services.product_service import ProductService

quote_bp = Blueprint('quotes', __name__, url_prefix='/quotes')


def _build_quote_data(form):
    customer = CustomerService.get_by_id(int(form['customer_id']))
    product = ProductService.get_by_id(int(form['insurance_product_id']))
    trip_days = int(form['trip_days'])

    calculations = QuoteCalculationService.calculate_total(
        product=product,
        age=customer.age,
        health_status=customer.health_status,
        has_chronic_disease=customer.has_chronic_disease,
        destination_country=form['destination_country'],
        trip_days=trip_days,
    )

    consultant_id = form.get('consultant_id')
    return {
        'customer_id': customer.id,
        'consultant_id': int(consultant_id) if consultant_id else None,
        'insurance_product_id': product.id,
        'destination_country': form['destination_country'],
        'trip_days': trip_days,
        'health_risk_factor': calculations['health_risk_factor'],
        'destination_risk_factor': calculations['destination_risk_factor'],
        'age_risk_factor': calculations['age_risk_factor'],
        'total_price': calculations['total_price'],
        'payment_status': form['payment_status'],
        'notes': form.get('notes', ''),
    }


@quote_bp.route('/')
def list_quotes():
    return render_template('quotes/list.html', quotes=QuoteService.get_all())


@quote_bp.route('/create', methods=['GET', 'POST'])
def create_quote():
    customers = CustomerService.get_all()
    consultants = ConsultantService.get_all()
    products = ProductService.get_all()
    if request.method == 'POST':
        QuoteService.create(_build_quote_data(request.form))
        return redirect(url_for('quotes.list_quotes'))
    return render_template('quotes/form.html', quote=None, customers=customers, consultants=consultants, products=products)


@quote_bp.route('/<int:quote_id>/edit', methods=['GET', 'POST'])
def edit_quote(quote_id):
    quote = QuoteService.get_by_id(quote_id)
    customers = CustomerService.get_all()
    consultants = ConsultantService.get_all()
    products = ProductService.get_all()
    if request.method == 'POST':
        QuoteService.update(quote, _build_quote_data(request.form))
        return redirect(url_for('quotes.list_quotes'))
    return render_template('quotes/form.html', quote=quote, customers=customers, consultants=consultants, products=products)


@quote_bp.route('/<int:quote_id>/delete', methods=['POST'])
def delete_quote(quote_id):
    QuoteService.delete(QuoteService.get_by_id(quote_id))
    return redirect(url_for('quotes.list_quotes'))
