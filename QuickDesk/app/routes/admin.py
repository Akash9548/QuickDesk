from flask import Blueprint, render_template, redirect, url_for, request
from flask_login import login_required, current_user
from ..models import User, Ticket
from .. import db

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    users = User.query.all()
    tickets = Ticket.query.all()
    return render_template('admin_dashboard.html', users=users, tickets=tickets)

@admin_bp.route('/admin/change-role/<int:user_id>', methods=['POST'])
@login_required
def change_role(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    new_role = request.form.get('new_role')
    if new_role in ['user', 'agent']:
        user.role = new_role
        db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))


@admin_bp.route('/admin/delete-user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        return redirect(url_for('auth.login'))

    user = User.query.get_or_404(user_id)
    if user.role != 'admin':
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.admin_dashboard'))
