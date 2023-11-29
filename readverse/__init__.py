from werkzeug.exceptions import HTTPException
from os import environ
from flask import Flask, render_template
from dotenv import load_dotenv
from sqlalchemy import select

from readverse.models import AllUser

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get(
        "DATABASE_URI", "sqlite:///project.db"
    )
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SECRET_KEY"] = environ.get("SECRET_KEY")

    from readverse.plugins import admin, migrate, login_manager
    from readverse.models import db, User

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.execute(
            select(AllUser).filter(User.username == user_id)
        ).scalar_one_or_none()

    admin.init_app(app)
    db.init_app(app)
    migrate.init_app(app)
    login_manager.init_app(app)

    from readverse.routes.auth import bp as auth_bp
    from readverse.routes.index import bp as index_bp
    from readverse.routes.profile import bp as profile_bp
    from readverse.routes.story import bp as story_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(index_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(story_bp)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e: HTTPException):
        response = e.get_response()
        status_code = response.status_code
        message = e.description or response.status
        return render_template(
            "error.html",
            status_code=status_code,
            message=message,
        )

    @app.errorhandler(Exception)
    def handle_exception(e: HTTPException):
        return render_template(
            "error.html",
            status_code=500,
            message="Something terrible happened",
        )

    return app
