"""Public-facing pages and form handling."""
from flask import (
    Blueprint, render_template, request, redirect, url_for, flash, abort, current_app
)
from extensions import db
from models import Service, TeamMember, Testimonial, Booking, ContactMessage, Newsletter
from forms import BookingForm, ContactForm, NewsletterForm
from content import FAQS
from emails import notify_new_booking, notify_new_contact

bp = Blueprint("public", __name__)


# --- shared queries -------------------------------------------------------
def active_services():
    return Service.query.filter_by(is_active=True).order_by(Service.sort_order).all()


def active_team():
    return TeamMember.query.filter_by(is_active=True).order_by(TeamMember.sort_order).all()


def active_testimonials():
    return (Testimonial.query.filter_by(is_active=True)
            .order_by(Testimonial.is_featured.desc(), Testimonial.sort_order).all())


# --- pages ----------------------------------------------------------------
@bp.route("/")
def home():
    return render_template(
        "index.html",
        services=active_services()[:6],
        testimonials=active_testimonials()[:3],
        team=active_team(),
        newsletter_form=NewsletterForm(),
    )


@bp.route("/services")
def services():
    return render_template("services.html", services=active_services())


@bp.route("/services/<slug>")
def service_detail(slug):
    service = Service.query.filter_by(slug=slug, is_active=True).first()
    if service is None:
        abort(404)
    others = [s for s in active_services() if s.slug != slug][:4]
    return render_template("service_detail.html", service=service, others=others)


@bp.route("/about")
def about():
    return render_template("about.html", team=active_team())


@bp.route("/team")
def team():
    return render_template("team.html", team=active_team())


@bp.route("/first-visit")
def first_visit():
    return render_template("first_visit.html", faqs=FAQS)


@bp.route("/reviews")
def reviews():
    return render_template("reviews.html", testimonials=active_testimonials())


@bp.route("/contact", methods=["GET", "POST"])
def contact():
    booking_form = BookingForm()
    contact_form = ContactForm()

    # Pre-select a service when arriving from a service page (?reason=Dental)
    if request.method == "GET":
        reason = request.args.get("reason")
        if reason:
            valid = {c[0] for c in booking_form.reason.choices}
            if reason in valid:
                booking_form.reason.data = reason

    submitted = request.form.get("form_type")

    if submitted == "booking" and booking_form.validate_on_submit():
        booking = Booking(
            name=booking_form.name.data.strip(),
            phone=booking_form.phone.data.strip(),
            email=(booking_form.email.data or "").strip(),
            pet_name=(booking_form.pet_name.data or "").strip(),
            pet_type=booking_form.pet_type.data,
            reason=booking_form.reason.data,
            preferred_date=booking_form.preferred_date.data,
            message=(booking_form.message.data or "").strip(),
        )
        db.session.add(booking)
        db.session.commit()
        notify_new_booking(booking)
        flash("Thanks — your request is in! We'll call or message you shortly to confirm.", "success")
        return redirect(url_for("public.contact", booked=1) + "#book")

    if submitted == "contact" and contact_form.validate_on_submit():
        msg = ContactMessage(
            name=contact_form.name.data.strip(),
            email=contact_form.email.data.strip(),
            subject=(contact_form.subject.data or "").strip(),
            message=contact_form.message.data.strip(),
        )
        db.session.add(msg)
        db.session.commit()
        notify_new_contact(msg)
        flash("Message sent — we'll get back to you soon. Thank you!", "success")
        return redirect(url_for("public.contact") + "#message")

    if submitted in {"booking", "contact"}:
        flash("Please check the highlighted fields and try again.", "error")

    return render_template(
        "contact.html",
        booking_form=booking_form,
        contact_form=contact_form,
        booked=request.args.get("booked"),
    )


@bp.route("/newsletter", methods=["POST"])
def newsletter():
    form = NewsletterForm()
    if form.validate_on_submit():
        email = form.email.data.strip().lower()
        if not Newsletter.query.filter_by(email=email).first():
            db.session.add(Newsletter(email=email))
            db.session.commit()
        flash("You're on the list — thanks for subscribing!", "success")
    else:
        flash("That email doesn't look right. Please try again.", "error")
    return redirect(request.referrer or url_for("public.home"))


# --- SEO helpers ----------------------------------------------------------
@bp.route("/sitemap.xml")
def sitemap():
    from flask import Response
    pages = ["home", "services", "about", "team", "first_visit", "reviews", "contact"]
    urls = [url_for(f"public.{p}", _external=True) for p in pages]
    urls += [url_for("public.service_detail", slug=s.slug, _external=True) for s in active_services()]
    body = "\n".join(
        f"<url><loc>{u}</loc><changefreq>weekly</changefreq></url>" for u in urls
    )
    xml = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
        f"{body}</urlset>"
    )
    return Response(xml, mimetype="application/xml")


@bp.route("/robots.txt")
def robots():
    from flask import Response
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin",
             f"Sitemap: {url_for('public.sitemap', _external=True)}"]
    return Response("\n".join(lines), mimetype="text/plain")
