from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash
from website import db
from flask_login import login_required, login_user, logout_user, current_user

auth = Blueprint("auth", __name__)


# login
@auth.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(mail=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You have logged in successfully!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("This password is incorrect, try again.", category="error")
        else:
            flash("E-mail does not exist.", category="error")


    return render_template("login.html", user= current_user)

# logout
@auth.route("/logout")
@login_required
def logout():

    logout_user()
    flash("You've logged out successfully.", category="success")
    return redirect(url_for("auth.login"))

# sign-up
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():

    if request.method == "POST":

        email = request.form["email"]
        firstName = request.form["firstName"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        print(request.form)

        user = User.query.filter_by(mail=email).first()

        if user:
            flash("This E-mail has already been registered", category="error")
        elif len(email) < 4:
            flash("E-mail must have more than 3 characters!", category="error")
        elif len(firstName) < 2:
            flash("First name must have more than 1 character!", category="error")
        elif password1 != password2:
            flash("Passwords do not match!", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 6 characters.", category="error")
        else:
            newUser = User(mail= email, first_name= firstName, password= generate_password_hash(password1))
            db.session.add(newUser)
            db.session.commit()
            flash("Account created!", category="success")

            return redirect(url_for("views.home"))
    else:

        return render_template("sign_up.html", user= current_user)