from extensions.extensions import db, login_manager
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    title = db.Column(db.String(100))
    content = db.Column(db.Text)
    author_avatar = db.Column(db.String(100))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(100), unique=True)
    avatar = db.Column(db.String(100))
    role = db.Column(db.String(100))
    visible = db.Column(db.Boolean, default=True)

    is_active = db.Column(db.Boolean, default=True)
    is_authenticated = db.Column(db.Boolean, default=False)
    is_anonymous = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))
