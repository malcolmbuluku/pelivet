"""Admin area — session login + a dashboard for bookings, messages and basic analytics."""
from datetime import timedelta
from functools import wraps
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, session, current_app, abort
)
from sqlalchemy import func
from extensions import db
from models import Booking, ContactMessage, Newsletter, PageView
from forms import AdminLoginForm
from utils import utcnow

bp = Blueprint("admin", __name__, url_prefix="/admin")


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login", next=request.path))
        return view(*args, **kwargs)
    return wrapped


@bp.route("/login", methods=["GET", "POST"])
def login():
    if session.get("is_admin"):
        return redirect(url_for("admin.dashboard"))
    form = AdminLoginForm()
    if form.validate_on_submit():
        ok = (form.username.data == current_app.config["ADMIN_USERNAME"]
              and form.password.data == current_app.config["ADMIN_PASSWORD"])
        if ok:
            session["is_admin"] = True
            session.permanent = True
            nxt = request.args.get("next")
            return redirect(nxt if nxt and nxt.startswith("/admin") else url_for("admin.dashboard"))
        flash("Incorrect username or password.", "error")
    return render_template("admin_login.html", form=form)


@bp.route("/logout")
def logout():
    session.pop("is_admin", None)
    flash("Signed out.", "success")
    return redirect(url_for("admin.login"))


@bp.route("/")
@login_required
def dashboard():
    status = request.args.get("status", "all")
    q = Booking.query
    if status in Booking.STATUSES:
        q = q.filter_by(status=status)
    bookings = q.order_by(Booking.created_at.desc()).limit(200).all()
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).limit(100).all()

    # --- lightweight analytics ---
    week_ago = utcnow() - timedelta(days=7)
    stats = {
        "bookings_total": Booking.query.count(),
        "bookings_new": Booking.query.filter_by(status="new").count(),
        "messages_total": ContactMessage.query.count(),
        "messages_unread": ContactMessage.query.filter_by(is_read=False).count(),
        "subscribers": Newsletter.query.count(),
        "views_7d": PageView.query.filter(PageView.created_at >= week_ago).count(),
    }
    top_pages = (
        db.session.query(PageView.path, func.count(PageView.id).label("n"))
        .filter(PageView.created_at >= week_ago)
        .group_by(PageView.path).order_by(func.count(PageView.id).desc()).limit(8).all()
    )
    return render_template(
        "admin_dashboard.html",
        bookings=bookings, messages=messages, stats=stats,
        top_pages=top_pages, status=status,
    )


@bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
@login_required
def set_booking_status(booking_id):
    booking = db.session.get(Booking, booking_id) or abort(404)
    new_status = request.form.get("status")
    if new_status in Booking.STATUSES:
        booking.status = new_status
        db.session.commit()
        flash(f"Booking #{booking.id} marked {new_status}.", "success")
    return redirect(url_for("admin.dashboard", status=request.args.get("status", "all")))


@bp.route("/messages/<int:message_id>/read", methods=["POST"])
@login_required
def mark_message_read(message_id):
    msg = db.session.get(ContactMessage, message_id) or abort(404)
    msg.is_read = True
    db.session.commit()
    return redirect(url_for("admin.dashboard") + "#messages")
