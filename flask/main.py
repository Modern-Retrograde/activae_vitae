# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import render_template, redirect
from flask import request, session

from hashlib import md5
from random import choice as random_choice
from configs import token_symbols, token_len

import behaviour
from errors import UserErrors

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

    return render_template("main.html", user=user)


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
