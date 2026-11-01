"""Email notifications — best-effort, never block a submission.

If MAIL_SERVER isn't configured, these functions quietly no-op so the site
works perfectly in development and the data is still saved to the database.
"""
import logging
from flask import current_app
from flask_mail import Message
from extensions import mail

log = logging.getLogger("pelivet.emails")


def _enabled() -> bool:
    return bool(current_app.config.get("MAIL_SERVER") and current_app.config.get("MAIL_USERNAME"))


def _send(subject: str, recipients: list[str], body: str) -> None:
    if not _enabled():
        log.info("Email disabled — would have sent %r to %s", subject, recipients)
        return
    try:
        mail.send(Message(subject=subject, recipients=recipients, body=body))
    except Exception as exc:  # pragma: no cover - never let email break a request
        log.warning("Email send failed: %s", exc)


def notify_new_booking(booking) -> None:
    to = current_app.config["MAIL_NOTIFY_TO"]
    body = (
        f"New appointment request\n\n"
        f"Name:    {booking.name}\n"
        f"Phone:   {booking.phone}\n"
        f"Email:   {booking.email or '-'}\n"
        f"Pet:     {booking.pet_name or '-'} ({booking.pet_type})\n"
        f"Reason:  {booking.reason}\n"
        f"Date:    {booking.preferred_date or 'No preference'}\n"
        f"Message: {booking.message or '-'}\n"
    )
    _send(f"New booking — {booking.name}", [to], body)


def notify_new_contact(msg) -> None:
    to = current_app.config["MAIL_NOTIFY_TO"]
    body = (
        f"New contact message\n\n"
        f"Name:    {msg.name}\n"
        f"Email:   {msg.email}\n"
        f"Subject: {msg.subject or '-'}\n\n"
        f"{msg.message}\n"
    )
    _send(f"Contact form — {msg.subject or msg.name}", [to], body)
