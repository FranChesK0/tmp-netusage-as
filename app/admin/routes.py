import json
from datetime import datetime, timedelta
from functools import wraps

from flask import flash, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from app import db
from app.admin import bp
from app.admin.forms import UserForm
from app.models import UsageRecord, User


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Вам нужно быть администратором для доступа к этой странице.")
            return redirect(url_for("auth.login"))
        return f(*args, **kwargs)

    return decorated_function


@bp.route("/dashboard")
@login_required
@admin_required
def dashboard():
    total_users = User.query.count()
    total_usage = db.session.query(db.func.sum(UsageRecord.data_used)).scalar() or 0

    # Get usage data for the graph
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)

    usage_data = (
        db.session.query(
            db.func.date(UsageRecord.timestamp).label("date"),
            db.func.sum(UsageRecord.data_used).label("total_data"),
        )
        .filter(UsageRecord.timestamp >= start_date, UsageRecord.timestamp <= end_date)
        .group_by(db.func.date(UsageRecord.timestamp))
        .order_by("date")
        .all()
    )

    dates = [str(record.date) for record in usage_data]
    values = [float(record.total_data) for record in usage_data]

    return render_template(
        "admin/dashboard.html",
        title="Анализ Трафика",
        total_users=total_users,
        total_usage=total_usage,
        dates=json.dumps(dates),
        values=json.dumps(values),
    )


@bp.route("/create_user", methods=["GET", "POST"])
@login_required
@admin_required
def create_user():
    form = UserForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data,
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(f"Пользователь {user.username} успешно создан.")
        return redirect(url_for("admin.dashboard"))
    return render_template(
        "admin/create_user.html", title="Создание пользователя", form=form
    )


@bp.route("/users")
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template(
        "admin/users.html", title="Управление пользователями", users=users
    )


@bp.route("/user/<int:id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_user(id):
    user = User.query.get_or_404(id)
    form = UserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        db.session.commit()
        flash("Данные пользователя обновлены.")
        return redirect(url_for("admin.users"))
    return render_template(
        "admin/edit_user.html",
        title="Изменение данных пользователя",
        form=form,
        user=user,
    )


@bp.route("/user/<int:id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_user(id):
    user = User.query.get_or_404(id)
    if user == current_user:
        flash("Вы не можете удалить собственный аккаунт!")
        return redirect(url_for("admin.users"))
    db.session.delete(user)
    db.session.commit()
    flash("Пользователь удален.")
    return redirect(url_for("admin.users"))


@bp.route("/api/usage_stats")
@login_required
@admin_required
def usage_stats():
    # Get top users by data usage
    top_users = (
        db.session.query(
            User.username, db.func.sum(UsageRecord.data_used).label("total_data")
        )
        .join(UsageRecord)
        .group_by(User.id)
        .order_by(db.desc("total_data"))
        .limit(5)
        .all()
    )

    return jsonify(
        {
            "labels": [user.username for user in top_users],
            "values": [float(user.total_data) for user in top_users],
        }
    )
