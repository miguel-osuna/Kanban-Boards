from flask import Blueprint, render_template

page = Blueprint("page", __name__, template_folder="templates")


@page.route("/", endpoint="home")
def home():
    return render_template("page/home.html")


@page.route("/terms", endpoint="terms")
def terms():
    return render_template("page/terms.html")


@page.route("/privacy", endpoint="privacy")
def privacy():
    return render_template("page/privacy.html")
