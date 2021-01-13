from kanban_boards.extensions import mail
from kanban_boards.blueprints.contact.tasks import deliver_contact_email


class TestTasks(object):
    def test_deliver_support_email(self):
        """ Deliver contact email. """
        form = {"email": "foo@bar.com", "message": "Test message from Tides"}

        with mail.record_messages() as outbox:
            deliver_contact_email(form.get("email"), form.get("message"))

            assert len(outbox) == 1
            assert form.get("email") in outbox[0].body
