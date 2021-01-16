from flask import Blueprint, redirect, request, flash, url_for, render_template
from flask_login import login_required, current_user
from flask_babel import _

from sqlalchemy import text

from kanban_boards.blueprints.admin.models import Dashboard
from kanban_boards.blueprints.admin.forms import SearchForm, BulkDeleteForm, UserForm
from kanban_boards.blueprints.user.decorators import role_required
from kanban_boards.blueprints.user.models import User

admin = Blueprint("admin", __name__, template_folder="templates", url_prefix="/admin")


@admin.before_request
@login_required
@role_required("admin")
def before_request():
    """ Protect all of the admin endpoints. """
    pass


# Dashboard
@admin.route("", methods=["GET"], endpoint="dashboard")
def dashboard():
    group_and_count_users = Dashboard.group_and_count_users()

    return render_template(
        "admin/page/dashboard.html", group_and_count_users=group_and_count_users
    )


# Users
@admin.route("/users", defaults={"page": 1})
@admin.route("/users/page/<int:page>", methods=["GET"], endpoint="users")
def users(page):
    search_form = SearchForm()
    bulk_form = BulkDeleteForm()

    sort_by = User.sort_by(
        request.args.get("sort", "created_on"), request.args.get("direction", "desc")
    )
    order_values = "{0} {1}".format(sort_by[0], sort_by[1])

    paginated_users = (
        User.query.filter(User.search(request.args.get("q", "")))
        .order_by(User.role.asc(), text(order_values))
        .paginate(page, 50, True)
    )

    return render_template(
        "admin/user/index.html",
        form=search_form,
        bulk_form=bulk_form,
        users=paginated_users,
    )


@admin.route("/users/edit/<int:id>", methods=["GET", "POST"], endpoint="users_edit")
def users_edit(id):
    user = User.query.get(id)
    form = UserForm(obj=user)

    if form.validate_on_submit():

        if User.is_last_admin(
            user, request.form.get("role"), request.form.get("active")
        ):
            flash(_("You are the last admin, you cannot do that."), "error")
            return redirect(url_for("admin.users"))

        form.populate_obj(user)

        user.save()

        flash(_("User has been saved successfully."), "success")
        return redirect(url_for("admin.users"))

    return render_template("admin/user/edit.html", form=form, user=user)


@admin.route("/users/bulk_delete", methods=["POST"], endpoint="users_bulk_delete")
def users_bulk_delete():
    form = BulkDeleteForm()

    if form.validate_on_submit():
        ids = User.get_bulk_action_ids(
            request.form.get("scope"),
            request.form.getlist("bulk_ids"),
            omit_ids=[current_user.id],
            query=request.args.get("q", text("")),
        )

        # Prevent circular imports
        from kanban_boards.blueprints.user.tasks import delete_users

        delete_users.delay(ids)

        flash(
            _("%(users)s user(s) were scheduled to be deleted.", users=len(ids)),
            "success",
        )

    else:
        flash(_("No users were deleted, something went wrong"), "error")

    return redirect(url_for("admin.users"))
