from flask import Blueprint, render_template, request, redirect, url_for
from ..services.product_service import ProductService

product_bp = Blueprint('products', __name__, url_prefix='/products')


def _product_form_data(form):
    return {
        'name': form['name'],
        'destination_risk_level': form['destination_risk_level'],
        'min_age': int(form['min_age']),
        'max_age': int(form['max_age']),
        'covers_pre_existing_conditions': 'covers_pre_existing_conditions' in form,
        'sports_coverage': 'sports_coverage' in form,
        'emergency_limit': int(form['emergency_limit']),
        'daily_price': float(form['daily_price']),
        'description': form['description'],
    }


@product_bp.route('/')
def list_products():
    return render_template('products/list.html', products=ProductService.get_all())


@product_bp.route('/create', methods=['GET', 'POST'])
def create_product():
    if request.method == 'POST':
        ProductService.create(_product_form_data(request.form))
        return redirect(url_for('products.list_products'))
    return render_template('products/form.html', product=None)


@product_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    product = ProductService.get_by_id(product_id)
    if request.method == 'POST':
        ProductService.update(product, _product_form_data(request.form))
        return redirect(url_for('products.list_products'))
    return render_template('products/form.html', product=product)


@product_bp.route('/<int:product_id>/delete', methods=['POST'])
def delete_product(product_id):
    ProductService.delete(ProductService.get_by_id(product_id))
    return redirect(url_for('products.list_products'))
