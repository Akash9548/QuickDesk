from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from ..models import Ticket
from .. import db

user_bp = Blueprint('user', __name__)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    tickets = Ticket.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tickets=tickets)

@user_bp.route('/create-ticket', methods=['POST'])
@login_required
def create_ticket():
    subject = request.form['subject']
    description = request.form['description']
    category = request.form['category']

    attachment = None
    file = request.files.get('attachment')
    if file and file.filename != '':
        filename = secure_filename(file.filename)
        upload_folder = os.path.join('app', 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)
        attachment = filename

    new_ticket = Ticket(
        subject=subject,
        description=description,
        category=category,
        attachment=attachment,
        user_id=current_user.id
    )
    db.session.add(new_ticket)
    db.session.commit()

    return redirect(url_for('user.dashboard'))


