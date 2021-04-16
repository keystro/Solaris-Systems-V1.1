#!/usr/bin/python3
#!/usr/flask/python3

from flask import Flask, render_template, url_for, flash, redirect, request
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required 
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import IPAddressType
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, IPAddress
import secrets, os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a9df6d4111e5c368c27fdbdebc186e0e'
app.config['SQLALCHEMY_DATABSE_URI'] ='sqlite:///'+os.path.join(basedir, 'data-drive.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bootstrap = Bootstrap(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


#SQLalchemy db models

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__='user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable = False)
    email = db.Column(db.String(128), unique = True, nullable = False)
    is_active = db.Column(db.Boolean, unique=False, default=False , nullable = False)
    password = db.Column(db.String(128), unique= False, nullable = False)
    devices = db.relationship('Device', backref = 'owner')


    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"


class Device(db.Model):
    __tablename__='device'
    id = db.Column(db.Integer, primary_key=True)
    unique_tag = db.Column(db.String(128), unique=True, nullable=True)
    decive_IP = db.Column(IPAddressType, unique=True, nullable = True)
    api_token = db.Column(db.String(256), unique=True, nullable=True)
    telemetrys = db.relationship('Telemetry', backref='device_data')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f"Device('{self.unique_tag}', '{self.decive_IP}')"


class Telemetry(db.Model):
    __tablename__='telemetry'
    id = db.Column(db.Integer, primary_key=True)
    watts_in = db.Column(db.SmallInteger, unique=False, nullable = False)
    watts_out = db.Column(db.SmallInteger, unique=False, nullable = False)
    op_volt = db.Column(db.SmallInteger, unique=False, nullable = False)
    op_amp = db.Column(db.SmallInteger, unique=False, nullable = False)
    device_temp = db.Column(db.SmallInteger, unique=False, nullable = False)
    battery_temp = db.Column(db.SmallInteger, unique=False, nullable = False)
    fan_state = db.Column(db.String(128), unique=False, nullable = False)
    timestamp = db.Column(db.DateTime, unique=False, nullable = False)
    device_id = db.Column(db.Integer, db.ForeignKey('device.id'))

    def __repr__(self):
        return f"Telemetry('{self.watts_in}', '{self.watts_out}', '{self.op_volt}', '{self.op_amp}','{self.device_temp}', '{self.battery_temp}','{self.enegry_state}', '{self.fan_state}','{self.timestamp}')"


#forms
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class NewdeviceForm(FlaskForm):
    device_IP = StringField('IoT Device IP', validators=[DataRequired(), IPAddress(message='eg. 192.168...')])
    submit = SubmitField('Integrate')



#app routes


@app.route('/login')
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check your login details', 'danger')
    return render_template('login.html')

@app.route('/register')
def register():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password= form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User account has been created successfully','success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/account')
def account():
    return render_template('account.html')

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

#appilcation inputs


#runnig server command

if __name__ == '__main__':
    app.run(debug=True, host='192.168.1.104', port = 8090)