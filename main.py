# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import render_template, redirect
import models

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/register")
def register():
    return render_template("registration.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/main_page")
def main_page():
    return redirect("/")


@app.route("/my_events")
def my_events():
    return render_template("events.html")


@app.route("/event/<int:event_id>")
def event(event_id: int):
    print(event_id)
    return render_template("event.html", event_id=event_id)


@app.route("/event/<int:event_id>/feedback")
def feedback(event_id: int):
    print(event_id)
    return render_template("feedback.html", event_id=event_id)


@app.route("/my_account")
def my_account():
    return render_template("my_account.html")


@app.route("/event_create")
def event_create():
    return render_template("event_create.html")


@app.route("/change_event/<int:event_id>")
def change_event(event_id: int):
    print(event_id)
    return render_template("change_event.html", event_id=event_id)
