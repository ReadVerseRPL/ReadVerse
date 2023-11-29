from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user
from sqlalchemy import select
from readverse.dto import LoginFormDTO, RegisterFormDTO
from readverse.models import AllUser, RegularUser, db

from readverse.utils import validate
from werkzeug.security import check_password_hash, generate_password_hash


bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.get("/login")
def login_page():
    return render_template("pages/auth/login.html")


@bp.post("/login")
@validate
def login(form: LoginFormDTO):
    username = form.username
    password = form.password

    user = db.session.execute(
        select(AllUser).filter(AllUser.username == username)
    ).scalar_one_or_none()

    if not user or not check_password_hash(user.password, password):
        flash("Invalid username or password", "error")
        return redirect(url_for("auth.login_page"))

    login_user(user)
    return redirect(url_for("index.index"))


@bp.get("/register")
def register_page():
    return render_template("pages/auth/register.html")


@bp.post("/register")
@validate
def register(form: RegisterFormDTO):
    user = RegularUser(
        username=form.username,
        password=generate_password_hash(form.password),
        email=form.email,
        phone_number=form.phone_number,
    )

    db.session.add(user)
    db.session.commit()

    flash("Registered!")
    return redirect(url_for("index.index"))


@bp.get("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index.index"))
