from flask import Blueprint, flash, redirect, render_template, url_for, abort
from sqlalchemy import select, desc
from readverse.plugins import current_user
from readverse.models import db, RegularUser, Story
from readverse.utils import validate
from readverse.dto import UpdateProfileDTO, ChangePasswordDTO
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/")
def profile():
    stories = (
        db.session.query(Story)
        .where(Story.author_id == current_user.get_id())
        .order_by(desc(Story.created_at))
        .all()
    )
    if len(stories) == 0:
        stories = None

    return render_template(
        "pages/profile/index.html", user=current_user, stories=stories
    )


@bp.get("/<username>")
def user_profile(username: str):
    user = db.session.query(RegularUser).where(RegularUser.username == username).first()
    if not user:
        abort(404)

    stories = (
        db.session.query(Story)
        .where(Story.author_id == user.get_id())
        .order_by(desc(Story.created_at))
        .all()
    )
    if len(stories) == 0:
        stories = None

    return render_template("pages/profile/index.html", user=user, stories=stories)


@bp.get("/edit")
def edit_profile():
    return render_template("pages/profile/edit.html", user=current_user)


@bp.get("/password")
def change_password():
    return render_template("pages/profile/change_password.html")


@bp.post("/password")
@validate
def change_password_post(form: ChangePasswordDTO):
    user = db.session.execute(
        select(RegularUser).where(RegularUser.username == current_user.get_id())
    ).scalar_one_or_none()

    if not user:
        abort(404)

    if not check_password_hash(user.password, form.current_password):
        flash("Wrong Password!", "error")
        return redirect(url_for("profile.change_password"))

    if form.new_password != form.confirm_password:
        flash("New Password Didn't Match", "error")
        return redirect(url_for("profile.change_password"))

    new_password = generate_password_hash(form.new_password)
    user.password = new_password

    db.session.commit()

    return redirect(url_for("profile.profile"))


@bp.post("/edit")
@validate
def edit_profile_post(form: UpdateProfileDTO):
    user = db.session.execute(
        select(RegularUser).where(RegularUser.username == current_user.get_id())
    ).scalar_one_or_none()

    if not user:
        abort(404)

    user.about = form.about
    user.email = form.email
    user.description = form.description
    user.phone_number = form.phone
    user.website = form.website

    db.session.commit()
    return redirect(url_for("profile.edit_profile"))
