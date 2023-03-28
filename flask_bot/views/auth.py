from flask import Blueprint, render_template, redirect, url_for, jsonify, session, request
from flask_jwt_extended import create_access_token
from marshmallow import ValidationError
from ..model.user import User
from ..sh.user import UserSchema

auth = Blueprint('auth', __name__, url_prefix='/auth')

user_schema = UserSchema()


@auth.route('/register', methods=['POST'])
def register():
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    create_user = User(
        username=user_data['username'],
        password=user_data['password'],
        email=user_data['email'],
        token=user_data['token']
    )
    create_user.password_hash(password=user_data['password'])
    create_user.create_users(create_user)
    result = UserSchema().dump(create_user)
    return jsonify(result)


@auth.route('/sign-in', methods=['POST'])
def login():
    try:
        user_data = UserSchema().load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    user = User.query.filter_by(email=user_data['email']).first()
    if user and user.check_password(user_data['password']):
        access_token = create_access_token(identity=user.id)
        return user_schema.dump(user)
    else:
        return jsonify({'login': False})


from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from flask_login import login_user, LoginManager, login_required
from wtforms.validators import DataRequired, Email
login_manager = LoginManager()


class LoginForm(FlaskForm):
    email = StringField(validators=[DataRequired(), Email()])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField()


@auth.route('/login', methods=['GET', 'POST'])
def login_users():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data, password=form.password.data).first()
        if user is not None:
            login_user(user)
            return redirect(url_for('admin.index'))

    return render_template('auth/login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@auth.route('/secret')
@login_required
def secret():
    return "This is a secret page!"