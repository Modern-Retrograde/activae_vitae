# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import request, session
from hashlib import md5
from datetime import datetime

from configs import date_format, all_roles_in_projects
from errors import UserErrors
from models import User

import api
import behaviour

app = Flask(__name__)


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


def authenticate(email: str, hash_password: str):
    token = behaviour.user_authenticate(email, hash_password)
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


def is_num(text: str):
    try:
        text = int(text)
        return text
    except ValueError:
        return False


def is_correct_date(date: str):
    try:
        return datetime.strptime(date, date_format)
    except ValueError:
        return False


def get_value(key: str, default, check_func):
    """
    Проверяет request, соответствует ли key установленной функции.
    Если да, то возвращает значение, иначе отдаёт default.
    """
    return request.values.get(key) if check_func(request.values.get(key)) else default


@app.route("/events", methods=["GET"])
def index():
    query = get_value("query", "", lambda x: bool(x))
    offset = get_value("offset", 0, is_num)
    limit = get_value("limit", 5, is_num)

    events = behaviour.get_events(offset, limit, query)
    if not events:
        return api.NotFound().__dict__()
    return api.EventsResponse(events).__dict__()


@app.route("/event", methods=["GET"])
def get_event():
    event_id = get_value("id", -1, is_num)

    event = behaviour.get_event_by_id(event_id)
    if not event:
        return api.NotFound().__dict__()

    return api.EventResponse(event).__dict__()


@app.route("/addEvent", methods=["POST"])
def add_event():
    user: User
    user = authorize(session.get("token"))

    if not user:
        return api.Unauthorized().__dict__()
    if not user.verified:
        return api.ErrorResponse(403, "Account isn't verified").__dict__()
    if user.role not in all_roles_in_projects:
        return api.ErrorResponse(403, "Unknown role set").__dict__()
    if not all_roles_in_projects[user.role]["create_events"]:
        return api.ErrorResponse(403, "You have no rights").__dict__()

    this_request = request.values

    needed_params = [
        "name", "short_description", "event_date",
        "event_format", "photos", "description"
    ]

    params = dict(request.values)
    if not all(map(lambda x: x in needed_params, params)):
        return api.OneOrMoreParamsMissedError().__dict__()

    event_date = is_correct_date(this_request["event_date"])
    if not event_date:
        return api.WrongDateEntered().__dict__()
    event_name = this_request["name"]
    if len(event_name) >= 50:
        return api.TooLongEventName(50)

    new_event = behaviour.add_event(
        name=event_name,
        short_description=this_request["short_description"],
        description=this_request["description"],
        event_date=event_date,
        organizer_id=user.id,
        event_format=this_request["event_format"],
        photos=this_request["photos"].split(",")
    )
    if not new_event:
        return api.ErrorResponse(500, error_text="Error on server side.").__dict__()
    return api.EventResponse(new_event).__dict__()


@app.route("/login", methods=["POST"])
def login():
    this_request = dict(request.values)
    if "hash_password" not in this_request or "email" not in this_request:
        return api.OneOrMoreParamsMissedError().__dict__()
    success = authenticate(this_request["email"], this_request["hash_password"])
    if success:
        return api.SuccessResponse(token=session.get("token")).__dict__()
    return api.WrongPasswordOrEmail().__dict__()


@app.route('/register', methods=["POST"])
def register():
    this_request = dict(request.values)
    needed_params = ["email", "password", "role", "full_name"]
    if not all(map(lambda x: x in this_request, needed_params)):
        """Проверяет сам факт наличия значения"""
        return api.OneOrMoreParamsMissedError().__dict__()
    if not all(map(lambda x: this_request[x], needed_params)):
        """Проверка на пустоту значения: все поля должны быть заполнены"""
        return api.OneOrMoreParamsMissedError().__dict__()

    user = registration(
        this_request["email"], this_request["full_name"],
        this_request["password"], this_request["role"]
    )
    if user:
        return api.SuccessResponse().__dict__()

    return api.RegistrationError(user.comment).__dict__()
