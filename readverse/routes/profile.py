from flask import Blueprint, redirect, render_template, url_for
from sqlalchemy import select, desc

from readverse.models import db, RegularUser, Story
from readverse.plugins import current_user

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/")
def profile():
    stories = db.session.query(Story).where(Story.author_id == current_user.get_id()).order_by(desc(Story.created_at)).all()
    if len(stories) == 0: stories = None
    return render_template("pages/profile/index.html", user=current_user, stories=stories)


@bp.get("/edit")
def edit_profile():
    # TODO: Show edit profile form
    return render_template("pages/profile/edit.html")


@bp.post("/edit")
def edit_profile_post():
    # TODO: Process post request
    return redirect(url_for("profile.profile"))
