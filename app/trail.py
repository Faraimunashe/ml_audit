from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import AuditLog

trail_bp = Blueprint('trail', __name__)

@trail_bp.route('/audits', methods=['GET'])
@login_required
def trail():
    search_query = request.args.get('search', '').strip()
    
    query = AuditLog.query.order_by(AuditLog.timestamp.desc())

    if search_query:
        query = query.filter(
            (AuditLog.model_name.ilike(f'%{search_query}%')) |
            (AuditLog.action.ilike(f'%{search_query}%'))
        )
    
    audits_data = query.all()
    
    return render_template('trail.html', audit_logs=audits_data, search_query=search_query)
