"""WTForms definitions — server-side validation and CSRF protection for every form."""
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, PasswordField
from wtforms.validators import DataRequired, Email, Length, Optional

PET_TYPES = [("Dog", "Dog"), ("Cat", "Cat"), ("Rabbit", "Rabbit"), ("Bird", "Bird"), ("Other", "Other")]
REASONS = [
    ("Wellness / check-up", "Wellness / check-up"),
    ("Vaccination", "Vaccination"),
    ("Dental", "Dental"),
    ("Sick / not right", "Sick / not right"),
    ("Surgery consult", "Surgery consult"),
    ("Grooming", "Grooming"),
    ("Other", "Other"),
]


class BookingForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), Length(max=120)])
    phone = StringField("Phone", validators=[DataRequired(), Length(max=40)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=160)])
    pet_name = StringField("Pet's name", validators=[Optional(), Length(max=120)])
    pet_type = SelectField("Pet type", choices=PET_TYPES, default="Dog")
    reason = SelectField("Reason for visit", choices=REASONS, default="Wellness / check-up")
    preferred_date = DateField("Preferred date", validators=[Optional()])
    message = TextAreaField("Anything we should know?", validators=[Optional(), Length(max=2000)])


class ContactForm(FlaskForm):
    name = StringField("Your name", validators=[DataRequired(), Length(max=120)])
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=160)])
    subject = StringField("Subject", validators=[Optional(), Length(max=160)])
    message = TextAreaField("Message", validators=[DataRequired(), Length(max=2000)])


class NewsletterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=160)])


class AdminLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
