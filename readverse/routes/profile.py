from flask import Blueprint, flash, redirect, render_template, url_for, abort
from sqlalchemy import select
from readverse.plugins import current_user
from readverse.models import db, RegularUser
from readverse.utils import validate
from readverse.dto import UpdateProfileDTO, ChangePasswordDTO
from werkzeug.security import check_password_hash, generate_password_hash




bp = Blueprint("profile", __name__, url_prefix="/profile")


@bp.get("/")
def profile():
    # TODO: Show current user's profile
    return render_template("pages/profile/index.html")


@bp.get("/edit")
def edit_profile():
    return render_template("pages/profile/edit.html",
        user = current_user
    )


@bp.get("/password")
def change_password():
    return render_template("pages/profile/change_password.html")

@bp.post("/password")
@validate
def change_password_post(form: ChangePasswordDTO):
    user: RegularUser = db.session.execute(
        select(RegularUser).where(RegularUser.username == current_user.get_id())
    ).scalar_one_or_none()

    if not user:
        abort(404)

    if not check_password_hash(user.password, form.currentPassword):
        flash("Wrong Password!", "error")
        return redirect(url_for("profile.change_password"))
    
    if (form.newPassword != form.confirmPassword):
        flash("New Password Didn't Match", "error")
        return redirect(url_for("profile.change_password"))
    
    newPassword = generate_password_hash(form.newPassword)
    user.password = newPassword

    db.session.commit()
    
    return redirect(url_for("profile.profile"))


@bp.post("/edit")
@validate
def edit_profile_post(form: UpdateProfileDTO):
    user: RegularUser = db.session.execute(
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
