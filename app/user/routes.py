from flask import render_template, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.user import bp
from app.models import UsageRecord
import json
from datetime import datetime, timedelta

@bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's total usage
    total_usage = db.session.query(
        db.func.sum(UsageRecord.data_used)
    ).filter(UsageRecord.user_id == current_user.id).scalar() or 0
    
    # Get usage over time
    usage_data = db.session.query(
        UsageRecord.timestamp,
        db.func.sum(UsageRecord.data_used).label('total_data')
    ).filter(UsageRecord.user_id == current_user.id).group_by(
        db.func.date(UsageRecord.timestamp)
    ).order_by(UsageRecord.timestamp).all()
    
    dates = [str(record.timestamp.date()) for record in usage_data]
    values = [float(record.total_data) for record in usage_data]
    
    # Get recent connections
    recent_connections = UsageRecord.query.filter_by(
        user_id=current_user.id
    ).order_by(UsageRecord.timestamp.desc()).limit(5).all()
    
    return render_template('user/dashboard.html',
                         title='My Dashboard',
                         total_usage=total_usage,
                         dates=json.dumps(dates),
                         values=json.dumps(values),
                         recent_connections=recent_connections)

@bp.route('/vpn')
@login_required
def vpn():
    return render_template('user/vpn.html', title='VPN Settings')

@bp.route('/api/usage_history')
@login_required
def usage_history():
    # Get usage history for the last 30 days
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    usage_data = db.session.query(
        UsageRecord.timestamp,
        UsageRecord.data_used,
        UsageRecord.connection_time
    ).filter(
        UsageRecord.user_id == current_user.id,
        UsageRecord.timestamp >= thirty_days_ago
    ).order_by(UsageRecord.timestamp.desc()).all()
    
    return jsonify([{
        'timestamp': record.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
        'data_used': float(record.data_used),
        'connection_time': record.connection_time
    } for record in usage_data])
