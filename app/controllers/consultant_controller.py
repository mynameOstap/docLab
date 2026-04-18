from flask import Blueprint, render_template, request, redirect, url_for
from ..services.consultant_service import ConsultantService

consultant_bp = Blueprint('consultants', __name__, url_prefix='/consultants')


def _consultant_form_data(form):
    return {
        'full_name': form['full_name'],
        'email': form['email'],
        'specialization': form['specialization'],
    }


@consultant_bp.route('/')
def list_consultants():
    return render_template('consultants/list.html', consultants=ConsultantService.get_all())


@consultant_bp.route('/create', methods=['GET', 'POST'])
def create_consultant():
    if request.method == 'POST':
        ConsultantService.create(_consultant_form_data(request.form))
        return redirect(url_for('consultants.list_consultants'))
    return render_template('consultants/form.html', consultant=None)


@consultant_bp.route('/<int:consultant_id>/edit', methods=['GET', 'POST'])
def edit_consultant(consultant_id):
    consultant = ConsultantService.get_by_id(consultant_id)
    if request.method == 'POST':
        ConsultantService.update(consultant, _consultant_form_data(request.form))
        return redirect(url_for('consultants.list_consultants'))
    return render_template('consultants/form.html', consultant=consultant)


@consultant_bp.route('/<int:consultant_id>/delete', methods=['POST'])
def delete_consultant(consultant_id):
    ConsultantService.delete(ConsultantService.get_by_id(consultant_id))
    return redirect(url_for('consultants.list_consultants'))
