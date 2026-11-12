
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_

from app.models import URL


dashboard_bp = Blueprint("dashboard", __name__)


@dashboard_bp.route("/")
@login_required
def home():

    search_query = request.args.get("q", "").strip()

    # All URLs belonging to the logged-in user
    user_urls = current_user.urls

    # Dashboard statistics
    total_urls = len(user_urls)

    total_clicks = sum(
        len(url.clicks) for url in user_urls
    )

    # Base query
    urls_query = URL.query.filter_by(
        user_id=current_user.id
    )

    # Search functionality
    if search_query:

        search_term = f"%{search_query}%"

        urls_query = urls_query.filter(
            or_(
                URL.original_url.ilike(search_term),
                URL.short_code.ilike(search_term)
            )
        )

    # Pagination settings
    page = request.args.get("page", 1, type=int)

    pagination = urls_query.order_by(
        URL.created_at.desc()
    ).paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    urls = pagination.items

    return render_template(
        "dashboard.html",
        user=current_user,
        urls=urls,
        total_urls=total_urls,
        total_clicks=total_clicks,
        search_query=search_query,
        pagination=pagination
    )
