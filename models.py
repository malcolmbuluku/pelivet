"""Database models for PELIVET.

Content models (Service, TeamMember, Testimonial) are seeded from content.py
and drive the public pages. Submission models (Booking, ContactMessage,
Newsletter) capture what visitors send. PageView powers the lightweight
analytics panel in the admin dashboard.
"""
from extensions import db
from utils import utcnow


class Service(db.Model):
    __tablename__ = "services"
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(80), unique=True, nullable=False, index=True)
    title = db.Column(db.String(120), nullable=False)
    icon = db.Column(db.String(40), nullable=False)          # key into the icon set
    summary = db.Column(db.String(300), nullable=False)       # card blurb
    description = db.Column(db.Text, nullable=False)           # detail-page body
    includes = db.Column(db.Text, default="")                 # newline-separated bullets
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)

    @property
    def include_list(self):
        return [line.strip() for line in (self.includes or "").splitlines() if line.strip()]


class TeamMember(db.Model):
    __tablename__ = "team_members"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(120), nullable=False)
    bio = db.Column(db.String(400), nullable=False)
    initials = db.Column(db.String(4), nullable=False)
    color = db.Column(db.String(40), default="#12304F")       # avatar gradient base
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Testimonial(db.Model):
    __tablename__ = "testimonials"
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(120), nullable=False)
    pet = db.Column(db.String(120), nullable=False)
    quote = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    initials = db.Column(db.String(4), nullable=False)
    color = db.Column(db.String(40), default="#159AA8")
    is_featured = db.Column(db.Boolean, default=False)
    sort_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)


class Booking(db.Model):
    __tablename__ = "bookings"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(160), default="")
    pet_name = db.Column(db.String(120), default="")
    pet_type = db.Column(db.String(40), default="Dog")
    reason = db.Column(db.String(80), default="Wellness / check-up")
    preferred_date = db.Column(db.Date, nullable=True)
    message = db.Column(db.Text, default="")
    status = db.Column(db.String(20), default="new")          # new | confirmed | done
    created_at = db.Column(db.DateTime, default=utcnow, index=True)

    STATUSES = ("new", "confirmed", "done")


class ContactMessage(db.Model):
    __tablename__ = "contact_messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(160), nullable=False)
    subject = db.Column(db.String(160), default="")
    message = db.Column(db.Text, nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=utcnow, index=True)


class Newsletter(db.Model):
    __tablename__ = "newsletter"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(160), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=utcnow)


class PageView(db.Model):
    __tablename__ = "page_views"
    id = db.Column(db.Integer, primary_key=True)
    path = db.Column(db.String(200), index=True)
    referrer = db.Column(db.String(300), default="")
    user_agent = db.Column(db.String(300), default="")
    ip = db.Column(db.String(60), default="")
    created_at = db.Column(db.DateTime, default=utcnow, index=True)
