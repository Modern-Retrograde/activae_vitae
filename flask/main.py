# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import render_template, redirect, abort
from flask import request, session

from hashlib import md5
from random import choice as random_choice
from configs import token_symbols, token_len, date_format

import behaviour
from errors import UserErrors
from configs import all_roles_in_projects
from models import User

app = Flask(__name__)
app.config["CSRF_ENABLED"] = True
app.config["SECRET_KEY"] = "".join([random_choice(token_symbols) for _ in range(token_len)])


def make_hash_password(password: str):
    return md5(bytes(password, encoding="utf-8")).hexdigest()


def registration(email: str, full_name: str,
                 password: str, role: str, verified: bool = False):
    """
    Регистрация нового пользователя в системе.
    Возвращает User, если новый пользователь создан.
    Возвращает UserError ошибку, если во время работы произошёл конфликт.
    """
    hash_password = make_hash_password(password)
    try:
        return behaviour.user_registration(
            email=email, full_name=full_name,
            hash_password=hash_password, role=role, verified=verified
        )
    except UserErrors as error:
        return error


def authenticate(email: str, password: str):
    token = behaviour.user_authenticate(email, make_hash_password(password))
    if token:
        session.setdefault("token", token.key)
        session.setdefault("expire_date", token.expire_date)
        return True
    return False


def authorize(token: str):
    if token:
        user = behaviour.user_authorize(token)
        return user
    return False


@app.route("/")
def index():
    user = authorize(session.get("token"))
    query = request.values.get("query") if "query" in request.values else ""
    events = behaviour.get_events(0, 10, query)
    return render_template(
        "main.html",
        user=user,
        events=events,
        time_to_str=lambda x: x.strftime(date_format)
    )


@app.route("/event/<int:event_id>")
def get_event(event_id: int):
    user = authorize(session.get("token"))
    event = behaviour.get_event_by_id(event_id)
    if not event:
        return redirect("/")

    return render_template(
        "event.html",
        user=user,
        event=event["event"],
        photos=event["photos"],
        enumerate=enumerate
    )


@app.route("/changeEvent/<int:event_id>", methods=["GET", "POST"])
def change_event(event_id: int):
    user: User
    user = authorize(session.get("token"))
    if not user:
        return redirect("/login")
    if not user.verified:
        return redirect("/")
    if user.role not in all_roles_in_projects:
        return redirect("/")
    if not all_roles_in_projects[user.role]["edit_events"]:
        return redirect("/")

    event = behaviour.get_event_by_id(event_id)
    if not event:
        return abort(404)

    if request.method == "GET":
        return render_template("changeEvent.html", event=event["event"], photos=event["photos"])
    needed_params = ["description", "name", "date", "format"]

    params = dict(request.values)
    if not all(map(lambda x: x in needed_params, params)):
        return abort(400)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        this_request = dict(request.values)
        if "password" not in this_request or "email" not in this_request:
            return redirect("/login")
        success = authenticate(this_request["email"], this_request["password"])
        if success:
            return redirect("/")
        return render_template("login.html", error="Неверный логин или пароль.")
    return render_template("login.html")


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        this_request = dict(request.values)
        needed_params = ["email", "password", "role", "full_name"]
        if not all(map(lambda x: x in this_request, needed_params)):
            return render_template("registration.html", error="Все поля должны быть заполнены.")
        if not all(map(lambda x: this_request[x], needed_params)):
            return render_template("registration.html", error="Все поля должны быть заполнены!")

        user = registration(
            this_request["email"], this_request["full_name"],
            this_request["password"], this_request["role"]
        )
        if user:
            return redirect("/login")
        return render_template("registration.html", error=user.comment)
    return render_template("registration.html")


@app.before_first_request
def before():
    print(behaviour.get_all_users())
    print("Deleting USERS", behaviour.delete_all_users())
    print(behaviour.get_all_users())
