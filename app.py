"""
Flask app for the carpentry/renovation business site.

Routes:
    GET  /          -> renders the single-page site
    POST /contact    -> validates and saves a contact form submission

Every submission is appended to data/submissions.csv. If mail settings
are filled in (see .env.example and the README), the business owner is
also emailed a copy of each submission.
"""

import csv
import os
import re
from datetime import datetime

from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mail import Mail, Message

from content import CONTENT

load_dotenv()  # reads a local .env file, if present, into os.environ

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-before-deploying")

# --- Email delivery config (see .env.example) ---
# These are read from environment variables so no real credentials ever
# live in the code. If MAIL_USERNAME/CONTACT_RECIPIENT_EMAIL aren't set,
# the contact form just skips sending an email and keeps saving to CSV.
app.config["MAIL_SERVER"] = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
app.config["MAIL_PORT"] = int(os.environ.get("MAIL_PORT", 587))
app.config["MAIL_USE_TLS"] = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
app.config["MAIL_USERNAME"] = os.environ.get("MAIL_USERNAME")
app.config["MAIL_PASSWORD"] = os.environ.get("MAIL_PASSWORD")
app.config["MAIL_DEFAULT_SENDER"] = os.environ.get("MAIL_DEFAULT_SENDER")
CONTACT_RECIPIENT_EMAIL = os.environ.get("CONTACT_RECIPIENT_EMAIL")

mail = Mail(app)

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
SUBMISSIONS_FILE = os.path.join(DATA_DIR, "submissions.csv")

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# Phone numbers may only use digits, spaces, "+", "-" and brackets, e.g.
# "078 395 0283" or "+27 (78) 395-0283". The number of actual digits is
# checked separately in validate_contact_form().
PHONE_PATTERN = re.compile(r"^[0-9+()\s-]+$")
PHONE_MIN_DIGITS = 9
PHONE_MAX_DIGITS = 15


def validate_contact_form(form):
    """Check the submitted form data and return a list of error messages.

    An empty list means the form is valid.
    """
    errors = []

    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    phone = form.get("phone", "").strip()
    message = form.get("message", "").strip()

    if not name:
        errors.append("Please enter your name.")

    if not email:
        errors.append("Please enter your email.")
    elif not EMAIL_PATTERN.match(email):
        errors.append("That email address doesn't look right.")

    # Phone is optional, so only check it if something was typed in.
    if phone:
        digit_count = len(re.sub(r"\D", "", phone))  # count just the digits
        if (not PHONE_PATTERN.match(phone)
                or not PHONE_MIN_DIGITS <= digit_count <= PHONE_MAX_DIGITS):
            errors.append("That phone number doesn't look right.")

    if not message:
        errors.append("Tell us a little about your project.")

    return errors


def save_submission(form):
    """Append a validated submission to the CSV file, creating it with
    a header row the first time it's used.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    file_exists = os.path.isfile(SUBMISSIONS_FILE)

    with open(SUBMISSIONS_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "name", "email", "phone", "project_type", "message"])
        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            form.get("name", "").strip(),
            form.get("email", "").strip(),
            form.get("phone", "").strip(),
            form.get("project_type", "").strip(),
            form.get("message", "").strip(),
        ])


def send_contact_email(form):
    """Email the business owner about a new contact form submission.

    Only called when mail credentials are configured (see contact() below),
    so this assumes app.config["MAIL_USERNAME"] and CONTACT_RECIPIENT_EMAIL
    are both set.
    """
    body_lines = [
        f"Name: {form.get('name', '').strip()}",
        f"Email: {form.get('email', '').strip()}",
        f"Phone: {form.get('phone', '').strip()}",
        f"Project type: {form.get('project_type', '').strip()}",
        "",
        form.get("message", "").strip(),
    ]

    # Styled version of the same email, matching the website's look.
    # Email apps show this one; body_lines above is the plain-text fallback.
    html = render_template(
        "email/contact_notification.html",
        business_name=CONTENT["business_name"],
        name=form.get("name", "").strip(),
        email=form.get("email", "").strip(),
        message=form.get("message", "").strip(),
        details=[
            ("Name", form.get("name", "").strip()),
            ("Email", form.get("email", "").strip()),
            ("Phone", form.get("phone", "").strip()),
            ("Project type", form.get("project_type", "").strip()),
        ],
    )

    message = Message(
        subject="New contact form submission — GKIDesigns website",
        recipients=[CONTACT_RECIPIENT_EMAIL],
        reply_to=form.get("email", "").strip(),   # Reply goes to the customer
        body="\n".join(body_lines),
        html=html,
    )
    mail.send(message)


@app.route("/")
def home():
    # form_data is empty here; contact() passes the visitor's answers back
    # in when the form has errors, so the fields stay filled in.
    return render_template("index.html", content=CONTENT, form_data={})


@app.route("/contact", methods=["POST"])
def contact():
    errors = validate_contact_form(request.form)

    if errors:
        for error in errors:
            flash(error, "error")
        # Show the page again with the visitor's answers still filled in,
        # so they only need to fix the field that was wrong instead of
        # retyping everything. (The form's action ends in "#contact", so
        # the browser scrolls straight back down to the form.)
        return render_template("index.html", content=CONTENT, form_data=request.form)

    save_submission(request.form)

    if app.config["MAIL_USERNAME"] and CONTACT_RECIPIENT_EMAIL:
        try:
            send_contact_email(request.form)
        except Exception as e:
            # Don't let an email/SMTP problem break the visitor's experience —
            # the submission is already safely saved to the CSV above.
            print(f"Failed to send contact form email: {e}")

    flash("Thanks! Your message has been sent — we'll be in touch soon.", "success")
    return redirect(url_for("home") + "#contact")


if __name__ == "__main__":
    app.run(debug=True)
