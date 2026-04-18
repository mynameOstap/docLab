from flask import Blueprint, render_template, request, redirect, url_for
from ..services.customer_service import CustomerService

customer_bp = Blueprint('customers', __name__, url_prefix='/customers')


def _customer_form_data(form):
    return {
        'full_name': form['full_name'],
        'age': int(form['age']),
        'health_status': form['health_status'],
        'country_of_travel': form['country_of_travel'],
        'has_chronic_disease': 'has_chronic_disease' in form,
    }


@customer_bp.route('/')
def list_customers():
    return render_template('customers/list.html', customers=CustomerService.get_all())


@customer_bp.route('/create', methods=['GET', 'POST'])
def create_customer():
    if request.method == 'POST':
        CustomerService.create(_customer_form_data(request.form))
        return redirect(url_for('customers.list_customers'))
    return render_template('customers/form.html', customer=None)


@customer_bp.route('/<int:customer_id>/edit', methods=['GET', 'POST'])
def edit_customer(customer_id):
    customer = CustomerService.get_by_id(customer_id)
    if request.method == 'POST':
        CustomerService.update(customer, _customer_form_data(request.form))
        return redirect(url_for('customers.list_customers'))
    return render_template('customers/form.html', customer=customer)


@customer_bp.route('/<int:customer_id>/delete', methods=['POST'])
def delete_customer(customer_id):
    CustomerService.delete(CustomerService.get_by_id(customer_id))
    return redirect(url_for('customers.list_customers'))
