import pytest
from flask import url_for

from lib.tests import assert_status_with_message, ViewTestMixin
from kanban_boards.blueprints.user.models import User


class TestLogin(ViewTestMixin):
    def test_login_page(self):
        """ Login page renders successfully. """
        response = self.client.get(url_for("user.login"))
        assert response.status_code == 200

    def test_login(self):
        """ Login successfully. """
        response = self.login()
        assert response.status_code == 200

    def test_login_activity(self):
        """Login successfully and update the activity stats.

        This executes the users fixture to add different users to the database.
        """
        user = User.find_by_identity("admin@local.host")
        old_sign_in_count = user.sign_in_count
        response = self.login()
        new_sign_in_count = user.sign_in_count

        assert response.status_code == 200
        assert (old_sign_in_count + 1) == new_sign_in_count

    def test_begin_login_fail_logged_in(self, users):
        """ Sign in should redirect to settings. """
        self.login()
        response = self.client.get(url_for("user.login"), follow_redirects=False)
        assert response.status_code == 302

    def test_login_disable(self, users):
        """ Login failure due to account being disabled. """
        response = self.login(identity="disabled@local.host")
        assert_status_with_message(200, response, "This account has been disabled.")

    def test_login_unconfirmed(self, users):
        response = self.login(identity="unconfirmed@local.host")
        assert_status_with_message(200, response, "Please confirm your account!")

    def test_login_fail(self):
        """ Login failure due to invalid login credentials. """
        response = self.login(identity="foo@bar.com", password="password")
        assert_status_with_message(200, response, "Sorry, wrong credentials.")

    def test_logout(self):
        """ Logout successfully. """
        self.login()
        response = self.logout()
        assert_status_with_message(200, response, "You have been logged out.")


class TestSignup(ViewTestMixin):
    def test_signup_page(self):
        """ Signup renders successuflly. """
        response = self.client.get(url_for("user.signup"))
        assert response.status_code == 200

    def test_begin_signup_fail_logged_in(self, users):
        """ Signup should redirect to settings. """
        self.login()
        response = self.client.get(url_for("user.signup"), follow_redirects=False)
        assert response.status_code == 302

    def test_begin_signup_fail(self):
        """ Signup failure due to using an account that exists. """
        user = {"email": "admin@local.host", "password": "password"}
        response = self.client.post(
            url_for("user.signup"), data=user, follow_redirects=True
        )

        assert_status_with_message(200, response, "Already exists.")

    def test_signup(self, users):
        """ Signup successfully. """
        old_user_count = User.query.count()

        user = {"username": "new", "email": "new@local.host", "password": "password"}
        response = self.client.post(
            url_for("user.signup"), data=user, follow_redirects=True
        )

        assert_status_with_message(
            200,
            response,
            "Thank you for signing up with Tides! An email has been sent to {}".format(
                user["email"]
            ),
        )

        new_user_count = User.query.count()
        assert (old_user_count + 1) == new_user_count

        new_user = User.find_by_identity(user["email"])
        assert new_user.password != user["password"]


class TestAccountConfirmation(ViewTestMixin):
    def test_begin_account_confirmation_page(self):
        """ Unconfirmed page renders successfully. """
        self.login(identity="unconfirmed@local.host")
        response = self.client.get(url_for("user.unconfirmed"))
        assert response.status_code == 200

    def test_begin_account_confirmation_as_unconfirmed(self):
        """ Should redirect to the begin acccount confirmation. """
        self.login(identity="unconfirmed@local.host")
        response = self.client.get(url_for("user.settings"), follow_redirects=False)
        assert response.status_code == 302

    def test_begin_account_confirmation_as_confirmed(self):
        """ Begin confirmation should be redirected to settings. """
        self.login()
        response = self.client.get(url_for("user.unconfirmed"), follow_redirects=True)
        assert_status_with_message(200, response, "Your account is already confirmed.")

    def test_begin_account_confirmation_resend_email(self):
        """ Display a message when the user clicks the resend button. """
        self.login(identity="unconfirmed@local.host")

        response = self.client.post(url_for("user.unconfirmed"), follow_redirects=True)
        assert_status_with_message(
            200, response, "A new confirmation email has been sent."
        )

    def test_account_confirmation(self, users):
        """ Account confirmation successful. """
        # Sign in the user to access to the account confirmation endpoint
        self.login(identity="unconfirmed@local.host")

        # Create confirmation token for the unconfirmed user
        user = User.find_by_identity("unconfirmed@local.host")
        token = user.serialize_token()

        response = self.client.get(
            url_for("user.account_confirmation", confirmation_token=token),
            follow_redirects=True,
        )
        assert_status_with_message(200, response, "Your account has been confirmed.")

    def test_account_confirmation_fail(self, token):
        """ Account confirmation fail due to using an already confirmed account. """
        self.login()
        response = self.client.get(
            url_for("user.account_confirmation", confirmation_token=token),
            follow_redirects=True,
        )
        assert_status_with_message(
            200, response, "Your account has been already confirmed."
        )

    def test_account_confirmation_empty_token(self, users):
        """ Account confirmation failure due to an empty confirmation token. """
        # Sign in the user to access to the account confirmation endpoint
        self.login(identity="unconfirmed@local.host")

        response = self.client.get(
            url_for("user.account_confirmation"), follow_redirects=True
        )

        assert_status_with_message(
            200, response, "Your confirmation token has expired or was tampered with."
        )

    def test_account_confirmation_invalid_token(self, users):
        """ Account confirmation failure due to an invalid confirmation token. """
        # Sign in the user to access to the account confirmation endpoint
        self.login(identity="unconfirmed@local.host")

        response = self.client.get(
            url_for(
                "user.account_confirmation",
                confirmation_token="123",
            ),
            follow_redirects=True,
        )
        assert_status_with_message(
            200, response, "Your confirmation token has expired or was tampered with."
        )


class TestPasswordReset(ViewTestMixin):
    def test_begin_password_reset_page(self):
        """ Begin password reset renders successfully. """
        response = self.client.get(url_for("user.begin_password_reset"))
        assert response.status_code == 200

    def test_password_reset_page(self):
        """ Password reset renders successfully. """
        response = self.client.get(url_for("user.password_reset"))
        assert response.status_code == 200

    def test_begin_password_reset_as_logged_in(self):
        """ Begin password reset should redirect to settings. """
        self.login()

        response = self.client.get(
            url_for("user.begin_password_reset"), follow_redirects=False
        )

        assert response.status_code == 302

    def test_password_reset_as_logged_in(self):
        """ Password reset should redirect to settings. """
        self.login()
        response = self.client.get(
            url_for("user.password_reset"), follow_redirects=False
        )

        assert response.status_code == 302

    def test_begin_password_reset_fail(self):
        """ Begin reset failure due to using a non-existing account. """
        user = {"identity": "foo@invalid.com"}
        response = self.client.post(
            url_for("user.begin_password_reset"), data=user, follow_redirects=True
        )

        assert_status_with_message(200, response, "Unable to locate account.")

    def test_begin_password_reset(self):
        """ Begin password reset successfully. """
        user = {"identity": "admin@local.host"}
        response = self.client.post(
            url_for("user.begin_password_reset"), data=user, follow_redirects=True
        )

        assert_status_with_message(
            200, response, "An email has been sent to {0}".format("admin@local.host")
        )

    def test_password_reset(self, token):
        """ Reset successful. """
        reset = {"password": "newpassword", "reset_token": token}
        response = self.client.post(
            url_for("user.password_reset"), data=reset, follow_redirects=True
        )

        assert_status_with_message(200, response, "Your password has been reset.")

        response = self.login(identity="admin@local.host", password=reset["password"])
        assert response.status_code == 200

    def test_password_reset_empty_token(self):
        """ Reset failure due to empty reset token. """
        reset = {"password": "newpassword"}
        response = self.client.post(
            url_for("user.password_reset"), data=reset, follow_redirects=True
        )

        assert_status_with_message(
            200, response, "Your reset token has expired or was tampered with."
        )

    def test_password_reset_invalid_token(self):
        reset = {"password": "newpassword", "token": "123"}
        response = self.client.post(
            url_for("user.password_reset"), data=reset, follow_redirects=True
        )

        assert_status_with_message(
            200, response, "Your reset token has expired or was tampered with."
        )


class TestSettings(ViewTestMixin):
    def test_settings_page(self):
        """ Settings renders successfully. """
        self.login()
        response = self.client.get(url_for("user.settings"))

        assert response.status_code == 200


class TestUpdateCredentials(ViewTestMixin):
    def test_update_credentials_page(self):
        """ Update credentials renders successfully. """
        self.login()
        response = self.client.get(url_for("user.update_credentials"))
        assert response.status_code == 200

    def test_begin_update_credentials_invalid_current(self):
        """ Update credentials failure due to invalid current password. """
        self.login()

        user = {"current_password": "12345", "email": "admin@local.host"}
        response = self.client.post(
            url_for("user.update_credentials"), data=user, follow_redirects=True
        )

        assert_status_with_message(200, response, "Does not match.")

    def test_begin_update_credentials_existing_email(self, users):
        """ Update credentials failure due to existing account w/ email. """
        self.login()

        user = {"current_password": "password", "email": "disabled@local.host"}
        response = self.client.post(
            url_for("user.update_credentials"), data=user, follow_redirects=True
        )

        assert_status_with_message(200, response, "Already exists.")

    def test_begin_update_credentials_email_change(self):
        """ Update credentials but only the e-mail address. """
        self.login()

        user = {"current_password": "password", "email": "admin2@local.host"}
        response = self.client.post(
            url_for("user.update_credentials"), data=user, follow_redirects=True
        )

        assert_status_with_message(200, response, "Your credentials have been updated.")

        old_user = User.find_by_identity("admin@local.host")
        assert old_user is None

        new_user = User.find_by_identity(user["email"])
        assert new_user is not None

    def test_begin_update_credentials_password_change(self):
        """ Update credentials but only the password. """
        self.login()

        user = {
            "current_password": "password",
            "email": "admin@local.host",
            "password": "newpassword",
        }

        response = self.client.post(
            url_for("user.update_credentials"), data=user, follow_redirects=True
        )
        assert response.status_code == 200

        self.logout()
        response = self.login(identity=user["email"], password=user["password"])
        assert response.status_code == 200

    def test_begin_update_credentials_email_password(self, client):
        """ Update both the email and a new password. """
        self.login()

        user = {
            "current_password": "password",
            "email": "admin2@local.host",
            "password": "newpassword",
        }

        response = self.client.post(
            url_for("user.update_credentials"), data=user, follow_redirects=True
        )
        assert response.status_code == 200

        self.logout()
        response = self.login(identity=user["email"], password=user["password"])
        assert response.status_code == 200


class TestUpdateLocale(ViewTestMixin):
    def test_update_locale_page(self, users):
        """ Update locale renders successfully. """
        self.login()
        response = self.client.get(url_for("user.update_locale"))

        assert response.status_code == 200

    def test_locale(self, users):
        """ Locale works succesfully. """
        self.login()

        user = {"locale": "en"}
        response = self.client.post(
            url_for("user.update_locale"), data=user, follow_redirects=True
        )

        assert_status_with_message(
            200, response, "Your locale settings have been updated."
        )
