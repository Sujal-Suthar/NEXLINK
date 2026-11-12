
import secrets
import string
from urllib.parse import urlparse
from flask import render_template
from datetime import datetime, timedelta, timezone

from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user

from app.extensions import db
from app.models import URL, Click

urls_bp = Blueprint("urls", __name__)


def generate_short_code(length=7):
    characters = string.ascii_letters + string.digits

    while True:
        short_code = "".join(
            secrets.choice(characters)
            for _ in range(length)
        )

        existing_url = URL.query.filter_by(
            short_code=short_code
        ).first()

        if not existing_url:
            return short_code


def is_valid_url(value):
    try:
        parsed = urlparse(value)

        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and parsed.hostname not in ("localhost", "127.0.0.1")
        )

    except ValueError:
        return False


@urls_bp.route("/")
def home():
    return redirect(url_for("auth.login"))

@urls_bp.route("/create", methods=["POST"])
@login_required
def create_short_url():

    original_url = request.form.get(
        "original_url", ""
    ).strip()

    if not is_valid_url(original_url):
        flash("Please enter a valid HTTP or HTTPS URL.", "danger")
        return redirect(url_for("dashboard.home"))

    short_code = generate_short_code()

    new_url = URL(
        original_url=original_url,
        short_code=short_code,
        user_id=current_user.id
    )

    try:
        db.session.add(new_url)
        db.session.commit()

        flash("Short URL created successfully!", "success")

    except Exception:
        db.session.rollback()
        flash("Something went wrong. Please try again.", "danger")

    return redirect(url_for("dashboard.home"))


@urls_bp.route("/<short_code>")
def redirect_url(short_code):

    url_record = URL.query.filter_by(
        short_code=short_code
    ).first_or_404()

    click = Click(url_id=url_record.id)

    db.session.add(click)
    db.session.commit()

    return redirect(url_record.original_url)



@urls_bp.route("/delete/<int:url_id>", methods=["POST"])
@login_required
def delete_url(url_id):

    url_record = URL.query.filter_by(
        id=url_id,
        user_id=current_user.id
    ).first_or_404()

    db.session.delete(url_record)
    db.session.commit()

    flash("URL deleted successfully!", "success")

    return redirect(url_for("dashboard.home"))





@urls_bp.route("/analytics/<int:url_id>")
@login_required
def url_analytics(url_id):

    url_record = URL.query.filter_by(
        id=url_id,
        user_id=current_user.id
    ).first_or_404()

    # India timezone
    
    india_timezone = timezone(
        timedelta(hours=5, minutes=30),
        name="IST"
    )

    # Convert UTC timestamps into India local time
    click_history = []

    for click in url_record.clicks:

        click_time = click.clicked_at

        # SQLite may return a naive datetime.
        # Our application stores these timestamps in UTC.
        if click_time.tzinfo is None:
            click_time = click_time.replace(
                tzinfo=timezone.utc
            )

        local_time = click_time.astimezone(india_timezone)

        # Display-friendly local timestamp
        click.display_time = local_time.strftime(
            "%d %b %Y, %I:%M %p"
        )

        click.local_date = local_time.date()

        click_history.append(click)

    # Latest clicks first
    click_history.sort(
        key=lambda click: click.clicked_at,
        reverse=True
    )

    total_clicks = len(click_history)

    # Last 7 days in India timezone
    today = datetime.now(india_timezone).date()

    dates = [
        today - timedelta(days=i)
        for i in range(6, -1, -1)
    ]

    daily_counts = {day: 0 for day in dates}

    for click in click_history:

        if click.local_date in daily_counts:
            daily_counts[click.local_date] += 1

    chart_labels = [
        day.strftime("%d %b")
        for day in dates
    ]

    chart_data = [
        daily_counts[day]
        for day in dates
    ]

    return render_template(
        "analytics.html",
        url=url_record,
        total_clicks=total_clicks,
        click_history=click_history,
        chart_labels=chart_labels,
        chart_data=chart_data
    )
