from flask_admin import Admin
from flask_migrate import Migrate
from flask_login import LoginManager, current_user as original_current_user

from readverse.models import User, db, RegularUser, Admin as AdminUser

admin = Admin(name="ReadVerse", template_mode="bootstrap4")
migrate = Migrate(db=db)
login_manager = LoginManager()
current_user: AdminUser | RegularUser = original_current_user  # type: ignore
