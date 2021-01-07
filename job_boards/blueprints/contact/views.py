from flask import Blueprint, flash, redirect, request, url_for, render_template

# from flask_login import current_user

from job_boards.blueprints.contact.forms import ContactForm

contact = Blueprint("contact", __name__, template_folder="templates")


@contact.route("/contact", methods=["GET", "POST"], endpoint="index")
def index():
    form = ContactForm()

    if form.validate_on_submit():
        # This prevents circular imports
        from job_boards.blueprints.contact.tasks import deliver_contact_email

        # Get form data
        email = request.form.get("email")
        message = request.form.get("message")

        # Create celery task
        deliver_contact_email.delay(email, message)

        flash(
            "Thank you for your message. We will contact you as soon as possible.",
            "success",
        )
        return redirect(url_for("contact.index"))

    return render_template("contact/index.html", form=form)

