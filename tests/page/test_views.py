from flask import url_for

from lib.tests import ViewTestMixin, assert_status_with_message


class TestPage(ViewTestMixin):
    def test_home_page(self):
        """ Home page should response with success 200. """
        response = self.client.get(url_for("page.home"))
        assert response.status_code == 200

    def test_terms_page(self):
        """ Terms page should respond with a success 200. """
        response = self.client.get(url_for("page.terms"))
        assert response.status_code == 200

    def test_privacy_page(self):
        """ Privacy page should respond with a success 200. """
        response = self.client.get(url_for("page.privacy"))
        assert response.status_code == 200

    def test_404_page(self):
        """ 404 errors should show the custom 404 page. """
        response = self.client.get("/thisisaurlthatdoesnotexist")
        assert_status_with_message(404, response, "404")

    def test_401_page(self):
        """ 401 errors (unauthorized) should show the custom 401 page. """
        pass

    def test_500_page(self):
        """ 500 errors (internal server error) should show the custom 401 page. """
        pass

