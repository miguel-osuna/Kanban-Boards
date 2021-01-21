from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message
from kanban_boards.blueprints.user.models import User


class TestDashboard(ViewTestMixin):
    def test_dashboard_page(self):
        """ Admin dashboard page renders successfully. """
        self.login()
        response = self.client.get(url_for("admin.dashboard"))
        assert bytes("User".encode("utf-8")) in response.data

class TestUsers(ViewTestMixin):
    def test_index_page(self):
        """ Users index page renders successfully. """
        self.login()
        response = self.client.get(url_for("admin.users"))
        assert response.status_code == 200

    def test_edit_page(self):
        """ Edit user page renders successfully. """
        self.login()
        admin = User.find_by_identity("admin@local.host")
        response = self.client.get(url_for("admin.users_edit", id=int(admin.id)))
        assert_status_with_message(200, response, "admin@local.host")

    def test_edit_resource(self):
        """ Edit this resource successfully. """
        params = {"role": "admin", "username": "foo", "active": True}
        self.login()
        admin = User.find_by_identity("admin@local.host")
        response = self.client.post(
            url_for("admin.users_edit", id=int(admin.id)),
            data=params,
            follow_redirects=True,
        )

        assert_status_with_message(200, response, "User has been saved successfully.")

    def test_bulk_delete_nothing(self):
        """ Try to delete al users (which is only admin). Last admin account should not get deleted. """
        self.login()
        old_count = User.query.count()
        admin = User.find_by_identity("admin@local.host")
        params = {"bulk_ids": [int(admin.id)], "scope": "all_selected_items"}
        response = self.client.post(
            url_for("admin.users_bulk_delete"), data=params, follow_redirects=True
        )
        assert_status_with_message(
            200, response, "0 user(s) were scheduled to be deleted."
        )

        new_count = User.query.count()
        assert new_count == old_count

