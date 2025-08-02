from flask import Blueprint, request, redirect, url_for
from flask_login import login_required, current_user
from ..models import Comment, Ticket
from .. import db
comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/ticket/<int:ticket_id>/comment', methods=['POST'])
@login_required
def add_comment(ticket_id):
    content = request.form['content'].strip()

    if not content:
        return redirect(url_for('agent.ticket_detail', ticket_id=ticket_id))

    ticket = Ticket.query.get_or_404(ticket_id)

    # Only ticket owner or assigned agent can comment
    if current_user.id != ticket.user_id and current_user.id != ticket.agent_id:
        return "Unauthorized", 403

    new_comment = Comment(
        content=content,
        user_id=current_user.id,
        ticket_id=ticket.id
    )

    db.session.add(new_comment)
    db.session.commit()
    
    return redirect(url_for('agent.ticket_detail', ticket_id=ticket.id))
