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

from flask import Flask, render_template, request, redirect, url_for, flash

from content import CONTENT

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key-change-this-before-deploying")

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
    flash("Thanks! Your message has been sent — we'll be in touch soon.", "success")
    return redirect(url_for("home") + "#contact")


if __name__ == "__main__":
    app.run(debug=True)
