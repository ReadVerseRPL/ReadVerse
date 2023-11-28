from flask import Blueprint, redirect, render_template, url_for
from sqlalchemy import select

from readverse.models import db, RegularUser

bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/")
def profile():
    # TODO: Show current user's profile
    return render_template("pages/profile/index.html")


@bp.get("/edit")
def edit_profile():
    # TODO: Show edit profile form
    return render_template("pages/profile/edit.html")


@bp.post("/edit")
def edit_profile_post():
    # TODO: Process post request
    return redirect(url_for("profile.profile"))
