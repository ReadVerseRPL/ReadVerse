from os import environ
from flask import Flask
from dotenv import load_dotenv
from sqlalchemy import select

from readverse.models import AllUser

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
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

    return app
