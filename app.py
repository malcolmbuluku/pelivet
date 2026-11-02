"""PELIVET Veterinary Clinic — Flask application factory."""
import logging
from datetime import timedelta
from flask import Flask, render_template, request, g

from config import Config
from utils import utcnow
from extensions import db, csrf, mail
from icons import icon


def create_app(config_class: type = Config) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)

    # instance/ holds the SQLite file and is created on first run
    import os
    os.makedirs(app.instance_path, exist_ok=True)

    logging.basicConfig(level=logging.INFO)

    # --- extensions ---
    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    app.permanent_session_lifetime = timedelta(days=7)

    # --- models & tables ---
    with app.app_context():
        from models import (  # noqa: F401  (registers models)
            Service, TeamMember, Testimonial, Booking,
            ContactMessage, Newsletter, PageView,
        )
        db.create_all()

    # --- blueprints ---
    from routes.public import bp as public_bp
    from routes.admin import bp as admin_bp
    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp)

    # --- template globals / context ---
    @app.context_processor
    def inject_globals():
        return {
            "clinic": {
                "name": app.config["CLINIC_NAME"],
                "phone": app.config["CLINIC_PHONE"],
                "phone_tel": _tel(app.config["CLINIC_PHONE"]),
                "emergency": app.config["CLINIC_EMERGENCY"],
                "emergency_tel": _tel(app.config["CLINIC_EMERGENCY"]),
                "email": app.config["CLINIC_EMAIL"],
                "address": app.config["CLINIC_ADDRESS"],
                "maps_query": app.config["CLINIC_MAPS_QUERY"],
            },
            "year": utcnow().year,
            "icon": icon,
            "nav_items": [
                ("public.services", "Services"),
                ("public.about", "About"),
                ("public.team", "Our Team"),
                ("public.first_visit", "First Visit"),
                ("public.reviews", "Reviews"),
                ("public.contact", "Contact"),
            ],
        }

    # --- simple page-view analytics (GET, non-asset, non-admin) ---
    @app.before_request
    def _track_view():
        p = request.path
        if request.method != "GET":
            return
        if p.startswith(("/static", "/admin")) or p in {"/favicon.ico", "/robots.txt", "/sitemap.xml"}:
            return
        try:
            db.session.add(PageView(
                path=p,
                referrer=(request.referrer or "")[:300],
                user_agent=(request.user_agent.string or "")[:300],
                ip=(request.headers.get("X-Forwarded-For", request.remote_addr) or "")[:60],
            ))
            db.session.commit()
        except Exception:
            db.session.rollback()

    # --- error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return render_template("errors/404.html"), 404

    @app.errorhandler(500)
    def server_error(e):
        db.session.rollback()
        return render_template("errors/500.html"), 500

    # --- CLI: flask seed ---
    @app.cli.command("seed")
    def seed_command():
        """Seed services, team and testimonials from content.py."""
        from seed import seed_content
        seed_content()
        print("Seeded content.")

    return app


def _tel(number: str) -> str:
    """Turn a display phone number into a tel: href value."""
    return "+" + "".join(ch for ch in number if ch.isdigit())


# For `flask run` and gunicorn `app:app`
app = create_app()


if __name__ == "__main__":
    app.run(debug=True, port=5000)
