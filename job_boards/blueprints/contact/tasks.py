import os

from lib.flask_mailplus import send_template_message
from job_boards.extensions import celery


@celery.task()
def deliver_contact_email(email, message):
    """
    Send a contact e-mail.

    :param email: E-mail address of the visitor
    :type user_id: str
    :param message: E-mail message
    :type user_id: str
    :return: None
    """
    ctx = {"email": email, "message": message}

    send_template_message(
        subject="[Tides] Contact",
        sender=email,
        recipients=[os.getenv("MAIL_USERNAME")],
        reply_to=email,
        template="contact/mail/index",
        ctx=ctx,
    )

    return None
