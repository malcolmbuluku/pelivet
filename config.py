"""Application configuration for PELIVET Veterinary Clinic.

Values are read from environment variables (see .env.example) so the same
code runs locally, in CI, and on the DigitalOcean droplet without edits.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def _bool(name: str, default: str = "false") -> bool:
    return os.environ.get(name, default).strip().lower() in {"1", "true", "yes", "on"}


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-change-me-in-production")

    # --- Database (SQLite by default; override with DATABASE_URL for Postgres etc.) ---
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{BASE_DIR / 'instance' / 'pelivet.db'}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Clinic details (surfaced across the site; edit in .env, no code changes) ---
    CLINIC_NAME = os.environ.get("CLINIC_NAME", "PELIVET Veterinary Clinic")
    CLINIC_PHONE = os.environ.get("CLINIC_PHONE", "+254 700 000 000")
    CLINIC_EMERGENCY = os.environ.get("CLINIC_EMERGENCY", "+254 711 111 111")
    CLINIC_EMAIL = os.environ.get("CLINIC_EMAIL", "hello@pelivet.co.ke")
    CLINIC_ADDRESS = os.environ.get("CLINIC_ADDRESS", "[Your street address], Nairobi")
    CLINIC_MAPS_QUERY = os.environ.get("CLINIC_MAPS_QUERY", "Nairobi, Kenya")

    # --- Admin (session login for the bookings dashboard) ---
    ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "pelivet-admin")

    # --- Email (optional: only sends if MAIL_SERVER is configured) ---
    MAIL_SERVER = os.environ.get("MAIL_SERVER")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", 587))
    MAIL_USE_TLS = _bool("MAIL_USE_TLS", "true")
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", MAIL_USERNAME)
    MAIL_NOTIFY_TO = os.environ.get("MAIL_NOTIFY_TO", CLINIC_EMAIL)

    @property
    def mail_enabled(self) -> bool:
        return bool(self.MAIL_SERVER and self.MAIL_USERNAME)
