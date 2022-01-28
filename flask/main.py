# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import render_template, redirect
from flask import session, request
from hashlib import md5

import data_manipulate
from errors import UserErrors

app = Flask(__name__)


def make_hash_password(password: str):
    return md5(bytes(password, encoding="utf-8")).hexdigest()


def get_user(login: str = None, password: str = None):
    """
    Получение данных о пользователе через доступные данные.
    Возвращает None, если пользователь не зашёл в систему.
    Возвращает User если пользователь находится в системе.
    """
    if "token" in session:
        user = data_manipulate.user_authorize(session["token"])
    elif login and password:
        hash_password = make_hash_password(password)
        token = data_manipulate.user_authenticate(login, hash_password)
        if token:
            session["token"] = token.token
            return get_user()
        else:
            user = None
    else:
        user = None

    return user


def registration(email: str, full_name: str,
                 password: str, role: str,
                 school_id: str):
    """
    Регистрация нового пользователя в системе.
    Возвращает User, если новый пользователь создан.
    Возвращает UserError ошибку, если во время работы произошёл конфликт.
    """
    hash_password = make_hash_password(password)
    try:
        school_id = int(school_id)
        return data_manipulate.user_register(
            email=email, full_name=full_name,
            hash_password=hash_password, role=role,
            school_id=school_id
        )
    except UserErrors as error:
        return error
    except ValueError:
        return UserErrors("School ID must be num.")


@app.route("/")
def index():
    return render_template("main_page.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        needed_params = [
            "email", "full_name", "password",
            "role", "school_id"
        ]
        this_request = request.values
        for needed_param in needed_params:
            if needed_param not in this_request:
                return redirect("/register")

        new_user = registration(
            email=this_request["email"],
            full_name=this_request["full_name"],
            password=this_request["password"],
            role=this_request["role"],
            school_id=this_request["school_id"]
        )
        if not new_user:
            return redirect("/register")
        get_user(this_request["email"], this_request["password"])
        return redirect("/")
    else:
        return render_template("registration.html")


@app.route("/login", methods=["GET", "POST"])
def login_user():
    if request.method == "POST":
        this_request = request.values
        if "login" not in this_request or "password" not in this_request:
            return redirect("/login")
        get_user(this_request["login"], this_request["password"])
        return redirect("/")
    return render_template("login.html")


@app.route("/main_page")
def main_page():
    return redirect("/")


@app.route("/my_events")
def my_events():
    return render_template("events.html")


@app.route("/event/<int:event_id>")
def event(event_id: int):
    return render_template("event.html", event_id=event_id)


@app.route("/event/<int:event_id>/stats")
def event(event_id: int):
    return render_template("statistics.html", event_id=event_id)


@app.route("/event/<int:event_id>/feedback")
def feedback(event_id: int):
    return render_template("feedback.html", event_id=event_id)


@app.route("/my_account")
def my_account():
    return render_template("my_account.html")


@app.route("/event_create")
def event_create():
    return render_template("event_create.html")


@app.route("/change_event/<int:event_id>")
def change_event(event_id: int):
    return render_template("change_event.html", event_id=event_id)
