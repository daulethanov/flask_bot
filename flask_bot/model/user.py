from datetime import datetime
from flask_security import RoleMixin, UserMixin, SQLAlchemySessionUserDatastore
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

roles_users = db.Table(
    'roles_users',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('role.id'))
)

users_messages = db.Table(
    'users_messages',
    db.Column('id', db.Integer, primary_key=True, autoincrement=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('user_message_id', db.Integer, db.ForeignKey('usermessage.id'))
)


class Role(db.Model, RoleMixin):
    __tablename__ = 'role'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    description = db.Column(db.String(200))

    def __repr__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    token = db.Column(db.BigInteger(), unique=True)
    active = db.Column(db.Boolean(), default=1)
    created_at = db.Column(db.DateTime, default=datetime.now())
    ticket = db.relationship('Ticket', backref='users')
    messages = db.relationship('UserMessage', secondary='users_messages', backref=db.backref('users', lazy='dynamic'))
    roles = db.relationship('Role', secondary='roles_users', backref=db.backref('users', lazy='dynamic'))

    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

    def __repr__(self):
        return self.username

    def password_hash(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def create_users(self, user):
        db.session.add(user)
        db.session.commit()


user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
