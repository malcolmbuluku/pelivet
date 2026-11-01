"""Seed / refresh content tables from content.py.

Run standalone:        python seed.py
Or via the Flask CLI:  flask seed

Safe to re-run: it upserts content by a natural key and never touches
visitor submissions (bookings, messages, newsletter, page views).
"""
from app import create_app
from extensions import db
from models import Service, TeamMember, Testimonial
from content import SERVICES, TEAM, TESTIMONIALS


def seed_content():
    # Services (keyed by slug)
    for i, s in enumerate(SERVICES):
        row = Service.query.filter_by(slug=s["slug"]).first() or Service(slug=s["slug"])
        row.title, row.icon, row.summary = s["title"], s["icon"], s["summary"]
        row.description, row.includes = s["description"], s["includes"]
        row.sort_order, row.is_active = i, True
        db.session.add(row)

    # Team (keyed by name)
    for i, m in enumerate(TEAM):
        row = TeamMember.query.filter_by(name=m["name"]).first() or TeamMember(name=m["name"])
        row.role, row.bio, row.initials = m["role"], m["bio"], m["initials"]
        row.color, row.sort_order, row.is_active = m["color"], i, True
        db.session.add(row)

    # Testimonials (keyed by author + pet)
    for i, t in enumerate(TESTIMONIALS):
        row = Testimonial.query.filter_by(author=t["author"], pet=t["pet"]).first() \
            or Testimonial(author=t["author"], pet=t["pet"])
        row.quote, row.rating, row.initials = t["quote"], t["rating"], t["initials"]
        row.color, row.is_featured, row.sort_order, row.is_active = t["color"], t["featured"], i, True
        db.session.add(row)

    db.session.commit()


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        seed_content()
        print(f"Seeded {len(SERVICES)} services, {len(TEAM)} team members, "
              f"{len(TESTIMONIALS)} testimonials.")
