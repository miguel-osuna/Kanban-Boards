from flask import Blueprint, redirect, request, flash, url_for, render_template
from flask_login import login_required, login_user, current_user, logout_user

from lib.safe_next_url import safe_next_url
from kanban_boards.blueprints.user.decorators import anonymous_required
from kanban_boards.blueprints.user.models import User
from kanban_boards.blueprints.user.forms import (
    LoginForm,
    BeginPasswordResetForm,
    PasswordResetForm,
    SignupForm,
    UpdateCredentialsForm,
    UpdateLocaleForm,
)

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/signup", methods=["GET", "POST"], endpoint="signup")
@anonymous_required()
def signup():
    """ Route for signing up the user. """
    form = SignupForm()

    if form.validate_on_submit():
        user = User()

        form.populate_obj(user)
        user.password = User.encrypt_password(request.form.get("password"))
        user.save()

        if login_user(user):
            flash("Thank you for signing up to Tides!", "success")
            return redirect(url_for("user.begin_account_confirmation"))

    return render_template("user/signup.html", form=form)


@user.route("/login", methods=["GET", "POST"], endpoint="login")
@anonymous_required()
def login():
    """ Route for loging in the user. """
    # Add next query param in case of a redirection from the login page
    form = LoginForm(next=request.args.get("next"))

    if form.validate_on_submit():
        user = User.find_by_identity(request.form.get("identity"))

        if user and user.authenticated(password=request.form.get("password")):
            # If remember me checkbox was selected, add it to the user cookie for
            # the browser

            # If the user is not active, login_user will return False
            if login_user(user, remember=request.form.get("remember", False)):
                user.update_activity_tracking(request.remote_addr)

                # Handle optionally redirecting to the next URL safely
                # This next_url is taken from the hidden form field
                next_url = request.form.get("next")

                if next_url:
                    return redirect(safe_next_url(next_url))

                return redirect(url_for("user.settings"))

        else:
            flash("Sorry, wrong credentials.", "error")

    return render_template("user/login.html", form=form)


@user.route("/logout", endpoint="logout")
@login_required
def logout():
    """ Route for loging out the user. """
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for("user.login"))


@user.route(
    "/account/begin_password_reset",
    methods=["GET", "POST"],
    endpoint="begin_password_reset",
)
@anonymous_required()
def begin_password_reset():
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        user = User.initialize_password_reset(request.form.get("identity"))

        flash("An email has been sent to {0}".format(user.email), "success")
        return redirect(url_for("user.login"))

    return render_template("user/begin_password_reset.html", form=form)


@user.route(
    "/account/password_reset", methods=["GET", "POST"], endpoint="password_reset"
)
@anonymous_required()
def password_reset():
    form = PasswordResetForm(reset_token=request.args.get("reset_token"))

    if form.validate_on_submit():
        user = User.deserialize_token(request.form.get("reset_token"))

        if user is None:
            flash("Your reset token has expired or was tampered with.", "error")
            return redirect(url_for("user.begin_password_reset"))

        form.populate_obj(user)
        user.password = User.encrypt_password(request.form.get("password"))
        user.save()

        if login_user(user):
            flash("Your password has been reset.", "success")
            return redirect(url_for("user.settings"))

    return render_template("user/password_reset.html", form=form)


@user.route(
    "/account/begin_account_confirmation",
    methods=["GET", "POST"],
    endpoint="begin_account_confirmation",
)
@login_required
def begin_account_confirmation():
    return render_template("user/begin_account_confirmation.html")


@user.route(
    "/account/account_confirmation",
    methods=["GET", "POST"],
    endpoint="account_confirmation",
)
@login_required
def account_confirmation():
    return render_template("user/account_confirmation.html")


@user.route("/settings", endpoint="settings")
@login_required
def settings():
    return render_template("user/settings.html")


@user.route(
    "/settings/update_credentials",
    methods=["GET", "POST"],
    endpoint="update_credentials",
)
@login_required
def update_credentials():
    form = UpdateCredentialsForm(obj=current_user)

    if form.validate_on_submit():
        # This won't change the user's email unless he changes it
        current_user.email = request.form.get("email")
        new_password = request.form.get("password")

        # If the user updated his password, encrypt it
        if new_password:
            current_user.password = User.encrypt(new_password)

        current_user.save()

        flash("Your credentials have been updated.", "success")
        return redirect(url_for("user.settings"))

    return render_template("user/update_credentials.html", form=form)


@user.route(
    "/settings/update_locale", methods=["GET", "POST"], endpoint="update_locale"
)
@login_required
def update_locale():
    form = UpdateLocaleForm(locale=current_user.locale)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash("Your locale settings have been updated.", "success")
        return redirect(url_for("user.settings"))

    return render_template("user/update_locale.html", form=form)
