"""
Flask app for the carpentry/renovation business site.

Routes:
    GET  /          -> renders the single-page site
    POST /contact    -> validates and saves a contact form submission

Submissions are appended to data/submissions.csv for now. See the
README for how to swap this out for real email delivery later.
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


def validate_contact_form(form):
    """Check the submitted form data and return a list of error messages.

    An empty list means the form is valid.
    """
    errors = []

    name = form.get("name", "").strip()
    email = form.get("email", "").strip()
    message = form.get("message", "").strip()

    if not name:
        errors.append("Please enter your name.")

    if not email:
        errors.append("Please enter your email.")
    elif not EMAIL_PATTERN.match(email):
        errors.append("That email address doesn't look right.")

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

    message = Message(
        subject="New contact form submission — GKIDesigns website",
        recipients=[CONTACT_RECIPIENT_EMAIL],
        body="\n".join(body_lines),
    )
    mail.send(message)


@app.route("/")
def home():
    return render_template("index.html", content=CONTENT)


@app.route("/contact", methods=["POST"])
def contact():
    errors = validate_contact_form(request.form)

    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("home") + "#contact")

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
