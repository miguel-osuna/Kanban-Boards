from kanban_boards.blueprints.user.models import User


class TestUser(object):
    def test_serialize_token(self, token):
        """ Token serializer serializes a JWS correctly. """
        assert token.count(".") == 2

    def test_deserialize_token(self, app, token):
        """ Token de-serializer de-serializes a JWS correctly. """
        user = User.deserialize_token(token)
        assert user.email == app.config["SEED_ADMIN_EMAIL"]

    def test_deserialize_token_tampered(self, token):
        user = User.deserialize_token(f"{token}123")
        assert user is None

