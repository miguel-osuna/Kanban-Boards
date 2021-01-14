from flask import Blueprint, redirect, request, flash, url_for, render_template
from flask_login import login_required, login_user, current_user, logout_user
from flask_babel import gettext as _

from lib.safe_next_url import safe_next_url
from lib.util_datetime import tzaware_datetime
from kanban_boards.blueprints.user.decorators import (
    anonymous_required,
    confirmed_required,
)
from kanban_boards.blueprints.user.models import User
from kanban_boards.blueprints.user.forms import (
    LoginForm,
    BeginPasswordResetForm,
    PasswordResetForm,
    SignupForm,
    UpdateCredentialsForm,
    UpdateLocaleForm,
    AccountUnconfirmedForm,
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

        # Begin account confirmation by sending an email to the user
        user.initialize_account_confirmation(user.email)
        flash(
            _(
                "Thank you for signing up with Tides! An email has been sent to {}".format(
                    user.email
                )
            ),
            "success",
        )

        if login_user(user):
            # Update the users activity, since he is signed in after the sign up
            user.update_activity_tracking(request.remote_addr)

            # Redirect to the account confirmation page
            # in case the user needs to resend the link
            return redirect(url_for("user.unconfirmed"))

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
            flash(_("Sorry, wrong credentials."), "error")

    return render_template("user/login.html", form=form)


@user.route("/logout", endpoint="logout")
@login_required
def logout():
    """ Route for loging out the user. """
    logout_user()
    flash(_("You have been logged out."), "success")
    return redirect(url_for("user.login"))


@user.route(
    "/account/begin_password_reset",
    methods=["GET", "POST"],
    endpoint="begin_password_reset",
)
@anonymous_required()
def begin_password_reset():
    """ Route to begin account password reset. """
    form = BeginPasswordResetForm()

    if form.validate_on_submit():
        user = User.initialize_password_reset(request.form.get("identity"))

        flash(_("An email has been sent to {0}".format(user.email)), "success")
        return redirect(url_for("user.login"))

    return render_template("user/begin_password_reset.html", form=form)


@user.route(
    "/account/password_reset", methods=["GET", "POST"], endpoint="password_reset"
)
@anonymous_required()
def password_reset():
    """ Route to reset password. """
    form = PasswordResetForm(reset_token=request.args.get("reset_token"))

    if form.validate_on_submit():
        user = User.deserialize_token(request.form.get("reset_token"))

        if user is None:
            flash(_("Your reset token has expired or was tampered with."), "error")
            return redirect(url_for("user.begin_password_reset"))

        form.populate_obj(user)
        user.password = User.encrypt_password(request.form.get("password"))
        user.save()

        if login_user(user):
            flash(_("Your password has been reset."), "success")
            return redirect(url_for("user.settings"))

    return render_template("user/password_reset.html", form=form)


@user.route(
    "/account/unconfirmed", methods=["GET", "POST"], endpoint="unconfirmed",
)
@login_required
def unconfirmed():
    form = AccountUnconfirmedForm()

    # Redirect user if he is already confirmed to avoid sending any emails
    if current_user.confirmed:
        flash(_("Your account is already confirmed."), "success")
        return redirect(url_for("user.settings"))

    # Send a new email if the user presses the button
    if form.validate_on_submit():
        current_user.initialize_account_confirmation(current_user.email)
        flash(_("A new confirmation email has been sent."), "success")
        return redirect(url_for("user.unconfirmed"))

    return render_template("user/unconfirmed.html", form=form)


@user.route(
    "/account/account_confirmation", methods=["GET"], endpoint="account_confirmation",
)
@login_required
def account_confirmation():
    confirmation_token = request.args.get("confirmation_token")
    user = User.deserialize_token(confirmation_token)

    if user is None:
        print(user)
        flash(_("Your confirmation token has expired or was tampered with."), "error")
        return redirect(url_for("user.login"))

    # Notice the user in case he tries to confirm his account again
    if user.confirmed:
        flash(_("Your account has been already confirmed."), "success")

    # Confirm the user account
    else:
        user.confirmed = True
        user.confirmed_on = tzaware_datetime()
        user.save()

        flash(_("Your account has been confirmed."), "success")

    login_user(user)
    return redirect(url_for("user.settings"))


@user.route("/settings", endpoint="settings")
@login_required
@confirmed_required()
def settings():
    return render_template("user/settings.html")


@user.route(
    "/settings/update_credentials",
    methods=["GET", "POST"],
    endpoint="update_credentials",
)
@login_required
@confirmed_required()
def update_credentials():
    form = UpdateCredentialsForm(obj=current_user)

    if form.validate_on_submit():
        # This won't change the user's email unless he changes it
        current_user.email = request.form.get("email")
        new_password = request.form.get("password")

        # If the user updated his password, encrypt it
        if new_password:
            current_user.password = User.encrypt_password(new_password)

        current_user.save()

        flash(_("Your credentials have been updated."), "success")
        return redirect(url_for("user.settings"))

    return render_template("user/update_credentials.html", form=form)


@user.route(
    "/settings/update_locale", methods=["GET", "POST"], endpoint="update_locale"
)
@login_required
@confirmed_required()
def update_locale():
    form = UpdateLocaleForm(locale=current_user.locale)

    if form.validate_on_submit():
        form.populate_obj(current_user)
        current_user.save()

        flash(_("Your locale settings have been updated."), "success")
        return redirect(url_for("user.settings"))

    return render_template("user/update_locale.html", form=form)
