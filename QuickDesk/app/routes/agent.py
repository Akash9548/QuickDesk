from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import Ticket, User
from .. import db
agent_bp = Blueprint('agent', __name__)

@agent_bp.route('/agent')
@login_required
def agent_dashboard():
    if current_user.role != 'agent':
        return redirect('/dashboard')

    tickets = Ticket.query.all()
    return render_template('agent_dashboard.html', tickets=tickets)

@agent_bp.route('/assign/<int:ticket_id>')
@login_required
def assign_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if current_user.role == 'agent' and ticket:
        ticket.agent_id = current_user.id
        ticket.status = 'In Progress'
        db.session.commit()
    return redirect(url_for('agent.agent_dashboard'))

@agent_bp.route('/update_status/<int:ticket_id>', methods=['POST'])
@login_required
def dashboard_update_status(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if ticket and current_user.role == 'agent' and ticket.agent_id == current_user.id:
        new_status = request.form['status']
        ticket.status = new_status
        db.session.commit()
    return redirect(url_for('agent.agent_dashboard'))

from flask import render_template, abort

@agent_bp.route('/ticket/<int:ticket_id>')
@login_required
def ticket_detail(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)

    # Restrict access: only the ticket creator, assigned agent, or admin can view
    if current_user.id != ticket.user_id and current_user.id != ticket.agent_id and current_user.role != 'admin':
        return abort(403)

    return render_template('ticket_detail.html', ticket=ticket)

@agent_bp.route('/ticket/<int:ticket_id>/update_status', methods=['POST'])
@login_required
def update_status(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    if current_user.id != ticket.agent_id:
        return "Unauthorized", 403

    new_status = request.form.get('status')
    if new_status in ['In Progress', 'Resolved', 'Closed']:
        ticket.status = new_status
        db.session.commit()
    return redirect(url_for('agent.ticket_detail', ticket_id=ticket.id))
