from getpass import getpass
from app import app
from readverse.models import db, Admin
from werkzeug.security import generate_password_hash

username = input("Username: ")
password = getpass("Password: ")
phone_number = input("Phone Number: ")
email = input("Email: ")


with app.app_context():
    user = Admin(
        username=username,
        password=generate_password_hash(password),
        email=email,
        phone_number=phone_number,
    )

    db.session.add(user)
    db.session.commit()

print("OK.")
