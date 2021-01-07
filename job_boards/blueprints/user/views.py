from flask import Blueprint, redirect, request, flash, url_for, render_template

user = Blueprint("user", __name__, template_folder="templates")


@user.route("/signup", methods=["GET", "POST"], endpoint="signup")
def signup():
    """ Route for signing up the user. """
    return render_template("user/signup.html")


@user.route("/login", methods=["GET", "POST"], endpoint="login")
def login():
    """ Route for loging in the user. """
    return render_template("user/login.html")


@user.route("/logout", endpoint="logout")
def logout():
    """ Route for loging out the user. """
    pass


@user.route(
    "/account/begin_password_reset",
    methods=["GET", "POST"],
    endpoint="begin_password_reset",
)
def begin_password_reset():
    return render_template("user/begin_password_reset.html")


@user.route(
    "/account/password_reset", methods=["GET", "POST"], endpoint="password_reset"
)
def password_reset():
    return render_template("user/password_reset.html")


@user.route(
    "/account/begin_account_confirmation",
    methods=["GET", "POST"],
    endpoint="begin_account_confirmation",
)
def begin_account_confirmation():
    return render_template("user/begin_account_confirmation.html")


@user.route(
    "/account/account_confirmation",
    methods=["GET", "POST"],
    endpoint="account_confirmation",
)
def account_confirmation():
    return render_template("user/account_confirmation.html")


@user.route("/settings", endpoint="settings")
def settings():
    return render_template("user/settings.html")


@user.route(
    "/settings/update_credentials",
    methods=["GET", "POST"],
    endpoint="update_credentials",
)
def update_credentials():
    return render_template("user/update_credentials.html")


@user.route(
    "/settings/update_locale", methods=["GET", "POST"], endpoint="update_locale"
)
def update_locale():
    return render_template("user/update_locale.html")
