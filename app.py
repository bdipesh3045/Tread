from flask import Flask, render_template, url_for, redirect, flash, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    UserMixin,
    login_user,
    LoginManager,
    login_required,
    logout_user,
    current_user,
)
import secrets
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

from main_insta import main_login, add_book


app = Flask(__name__)

bcrypt = Bcrypt(app)
import os

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"sqlite:///{os.path.join(os.getcwd(), 'database.db')}"
)

app.config["SECRET_KEY"] = "thisisasecretkey"
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    instapaper_account = db.relationship(
        "InstapaperAccount", backref="user", uselist=False, cascade="all, delete-orphan"
    )
    api_token = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        return f"<User {self.username}>"


class InstapaperAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    consumer_key = db.Column(db.String(120), nullable=False)
    consumer_secret = db.Column(db.String(120), nullable=False)
    iname = db.Column(db.String(100), nullable=False)  # Instapaper username
    password = db.Column(
        db.String(200), nullable=False
    )  # Store password securely (hashed ideally)
    is_verified = db.Column(db.Boolean, default=False)
    # Foreign key to link with User
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<InstapaperAccount {self.iname}>"


class InstapaperForm(FlaskForm):
    consumer_key = StringField(
        validators=[InputRequired(), Length(min=4, max=120)],
        render_kw={"placeholder": "Consumer Key"},
    )

    consumer_secret = StringField(
        validators=[InputRequired(), Length(min=4, max=120)],
        render_kw={"placeholder": "Consumer Secret"},
    )

    iname = StringField(
        validators=[InputRequired(), Length(min=4, max=100)],
        render_kw={"placeholder": "Instapaper Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=4, max=200)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Save")


@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    form = InstapaperForm()

    # Query the current user's Instapaper account details (if exists)
    instapaper_account = InstapaperAccount.query.filter_by(
        user_id=current_user.id
    ).first()

    if form.validate_on_submit():
        if instapaper_account:
            # Create new account if it doesn't exist
            form_data = main_login(
                form.consumer_key.data,
                form.consumer_secret.data,
                form.iname.data,
                form.password.data,
            )
            print(form_data)
            if form_data is False:

                flash("Failed to login to Instapaper. Please check your credentials.")
            else:

                current_user.api_token = secrets.token_hex(32)
                db.session.add(current_user)
                db.session.commit()
                print(current_user.api_token)

            # Update existing account if it exists
            instapaper_account.consumer_key = form.consumer_key.data
            instapaper_account.consumer_secret = form.consumer_secret.data
            instapaper_account.iname = form.iname.data
            instapaper_account.password = form.password.data  # Ensure this is
            instapaper_account.is_verified = form_data

        else:
            # Create new account if it doesn't exist
            form_data = main_login(
                form.consumer_key.data,
                form.consumer_secret.data,
                form.iname.data,
                form.password.data,
            )
            print(form_data)
            if form_data is False:

                flash("Failed to login to Instapaper. Please check your credentials.")

            instapaper_account = InstapaperAccount(
                consumer_key=form.consumer_key.data,
                consumer_secret=form.consumer_secret.data,
                iname=form.iname.data,
                is_verified=form_data,
                password=form.password.data,  # Ensure this is hashed
                user_id=current_user.id,
            )
            db.session.add(instapaper_account)

        db.session.commit()
        flash("Instapaper account details updated successfully!", "success")
        # return redirect(url_for("dashboard"))

    return render_template(
        "profile.html", form=form, instapaper_account=instapaper_account
    )


class RegisterForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose a different one."
            )


class LoginForm(FlaskForm):
    username = StringField(
        validators=[InputRequired(), Length(min=4, max=20)],
        render_kw={"placeholder": "Username"},
    )

    password = PasswordField(
        validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"},
    )

    submit = SubmitField("Login")


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect(url_for("dashboard"))
    return render_template("login.html", form=form)


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard():
    if request.method == "POST":
        # Get folder name
        folder_name = request.form.get("folderName")

        # Get lists of book names and URLs
        book_names = request.form.getlist("bookNames[]")
        urls = request.form.getlist("urls[]")
        # current_user = User.query.filter_by(username='current_username').first()  # Replace with actual session or login logic

        # Fetch the user's Instapaper credentials from the database
        instapaper_account = current_user.instapaper_account

        # Retrieve the secrets for Instapaper authentication
        secrets = [
            instapaper_account.consumer_key,
            instapaper_account.consumer_secret,
            instapaper_account.iname,
            instapaper_account.password,
        ]
        print(secrets)
        add_book(secrets, filename=folder_name, title=book_names, links=urls)
        print(folder_name, book_names, urls)

        return render_template("thanks.html")
    return render_template("dashboard.html")


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Creating the api that will allow people to connect it with the scrapper
@app.route("/api/<string:key>/", methods=["POST", "GET"])
def api(key):
    user = User.query.filter_by(api_token=key).first()
    if user is None:
        return {"message": "Invalid API key"}

    if request.method == "POST":
        data = dict(request.get_json())
        # return {"message": "Success"}
        # print(data)

        folder_name = data.get("folderName")
        book_names = data.get("bookNames")
        urls = data.get("urls")
        if book_names is None or urls is None:
            return {"message": "Invalid data"}
        if book_names is None:
            book_names = []
        print(folder_name, book_names, urls)
        # print(folder_name)

        instapaper_account = user.instapaper_account

        # Retrieve the secrets for Instapaper authentication
        secrets = [
            instapaper_account.consumer_key,
            instapaper_account.consumer_secret,
            instapaper_account.iname,
            instapaper_account.password,
        ]
        # print(secrets)
        try:
            add_book(secrets, filename=folder_name, title=book_names, links=urls)
        except Exception as e:
            return {"message": "Failed to add books"}
        # print(folder_name, book_names, urls)
        return {"message": "Success"}

    else:

        return {"message": "Correct API KEY USE POST TO ADD BOOKS"}

        # Get lists of book names and URLs
        book_names = request.json.get("bookNames")
        urls = request.json.get("urls")
        # current_user = User.query.filter_by(username='current_username').first()  # Replace with actual session or login logic

        # Fetch the user's Instapaper credentials from the database

        return {"message": "Success"}


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))

    return render_template("register.html", form=form)


# with app.app_context():
#     db.create_all()

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()

        db.create_all()  # Creates database tables
    app.run(debug=True)
