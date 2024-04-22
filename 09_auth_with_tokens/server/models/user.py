from . import SerializerMixin, validates, re, db
from sqlalchemy.ext.hybrid import hybrid_property
from app_config import flask_bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    _password_hash = db.Column(db.String, nullable=False)

    serialize_rules = ("-_password_hash",)

    @hybrid_property
    def password_hash(self):
        raise AttributeError("Passwords cannot be inspected after being setup!")

    @password_hash.setter
    def password_hash(self, new_password):
        #! validate the password
        if len(new_password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        elif not re.search(r"\d", new_password):
            raise ValueError("Password must contain at least one digit")
        elif not re.search(r"[A-Z]", new_password):
            raise ValueError("Password must contain at least one uppercase letter")
        #! hash the password
        hashed_password = flask_bcrypt.generate_password_hash(new_password).decode('utf-8')
        #! set the hashed password onto the user
        self._password_hash = hashed_password

    def authenticate(self, password_to_check):
        return flask_bcrypt.check_password_hash(self._password_hash, password_to_check)

    @validates("username")
    def validate_username(self, key, username):
        if not re.match(r"^[a-zA-Z0-9_]*$", username):
            raise ValueError("Username must be alphanumeric with underscores only")
        return username

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(r"^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$", email):
            raise ValueError("Invalid email address")
        return email
