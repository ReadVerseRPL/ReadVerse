from flask import Blueprint, redirect, render_template, url_for, abort
from sqlalchemy import select
from readverse.plugins import current_user
from readverse.models import db, RegularUser
from readverse.utils import validate
from readverse.dto import UpdateProfileDTO


bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/")
def profile():
    # TODO: Show current user's profile
    return render_template("pages/profile/index.html")


@bp.get("/edit")
def edit_profile():
    # TODO: Show edit profile form
    print(current_user.description)
    return render_template("pages/profile/edit.html",
        user = current_user
    )


@bp.post("/edit")
@validate
def edit_profile_post(form: UpdateProfileDTO):
    user: RegularUser = db.session.execute(
        select(RegularUser).where(RegularUser.username == current_user.get_id())
    ).scalar_one_or_none()


    print(current_user.get_id())
    if not user:
        abort(404)

    user.about = form.about
    user.email = form.email
    user.description = form.description
    user.phone_number = form.phone
    user.website = form.website

    print(user)
    # db.session.add(user)
    db.session.commit()
    return redirect(url_for("profile.edit_profile"))
