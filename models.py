"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class Trainings(db.Model):

    __tablename__ = 'trainings'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    title = db.Column(
        db.Text,
        nullable=False,
    )

    description = db.Column(
        db.Text,
        nullable=False,
    )

    date = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow(),
    )

    trainer_users_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete="cascade"),
        nullable=False
    )

    participants = db.relationship('User', secondary="trainings_users", 
                                    cascade="all,delete", backref="trainings")

    # trainer_user = db.relationship("User", backref="training", cascade="all,delete")


class Trainings_users(db.Model):

    __tablename__ = 'trainings_users' 

    users_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id', ondelete='cascade'),
        primary_key=True,
    )

    trainings_id = db.Column(
        db.Integer,
        db.ForeignKey('trainings.id', ondelete='cascade'),
        primary_key=True,
    )



class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    about = db.Column(
        db.Text,
    )

    password = db.Column(
        db.Text,
        nullable=False,
    )
    is_trainer = db.Column(
        db.Boolean,
        default=False,
    )

    user_trainings = db.relationship('Trainings', secondary="trainings_users", 
                                        cascade="all,delete", backref="users")


    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @classmethod
    def signup(cls, username, email, password, image_url, is_trainer):
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
            is_trainer=is_trainer,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


def connect_db(app):
    db.app = app
    db.init_app(app)
