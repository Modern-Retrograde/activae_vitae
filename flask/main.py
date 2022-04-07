# Здесь происходит определение ответов различных запросов Фласком.

from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
from hashlib import md5
from datetime import datetime
from json import loads as json_loads

from configs import date_format, all_roles_in_projects
from errors import UserErrors
from models import User

import api
import behaviour

app = Flask(__name__)
cors = CORS(app)


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
        return token
    return False


def authorize():
    if not request.headers.get("Authorization"):
        return False

    auth = request.headers.get("Authorization").split(" ")
    user = behaviour.user_authorize(auth[1])

    return user


def need_access(right_to_check: str):
    def functionality(func):
        def wrap(*args, **kwargs):
            user: User
            user = authorize()

            if not user:
                return api.Unauthorized().__dict__()
            if not user.verified:
                return api.ErrorResponse(403, "Account isn't verified").__dict__()
            if user.role not in all_roles_in_projects:
                return api.ErrorResponse(403, "Unknown role set").__dict__()
            if not all_roles_in_projects[user.role][right_to_check]:
                return api.ErrorResponse(403, "You have no rights").__dict__()

            return func(*args, **kwargs)
        return wrap
    return functionality


def check_params(needed_params: list):
    def functionality(func):
        def wrap(*args, **kwargs):
            if not all(map(lambda x: x in request.values, needed_params)):
                missed_params = list(set(needed_params) - set(request.values.keys()))
                return api.OneOrMoreParamsMissedError(missed_params).__dict__()
            if not all(map(lambda x: bool(request.values[x]), needed_params)):
                missed_params = list(set(needed_params) - set(request.values.keys()))
                return api.OneOrMoreParamsMissedError(missed_params).__dict__()

            return func(*args, **kwargs)
        return wrap
    return functionality


def is_num(text: str):
    try:
        if not text:
            return False

        int(text)
        return True
    except ValueError:
        return False


def is_correct_date(date: str):
    try:
        return datetime.strptime(date, date_format)
    except ValueError:
        return False


def get_value(key: str, default, check_func=lambda x: x):
    """
    Проверяет request, соответствует ли key установленной функции.
    Если да, то возвращает значение, иначе отдаёт default.
    """

    return request.values.get(key) if check_func(request.values.get(key)) else default


@check_params(["id", ])
def get_event():
    event_id = get_value("id", -1, is_num)

    event = behaviour.get_event_by_id(event_id)
    if not event:
        return api.NotFound().__dict__()

    return api.EventResponse(event).__dict__()


@need_access("create_events")
@check_params(
    ["name", "short_description", "date",
     "format", "photos", "description"]
)
def add_event():
    user: User
    user = authorize()
    this_request = request.values

    event_date = is_correct_date(this_request["date"])
    if not event_date:
        return api.WrongDateEntered().__dict__()
    if len(this_request["name"]) >= 50:
        return api.TooLongEventName(50).__dict__()

    new_event = behaviour.add_event(
        name=this_request["name"],
        short_description=this_request["short_description"],
        description=this_request["description"],
        event_date=event_date, organizer_id=user.id,
        event_format=this_request["format"],
        photos=this_request["photos"].split(",")
    )
    if not new_event:
        return api.ErrorResponse(500, error_text="Error on server side.").__dict__()
    return api.EventResponse(new_event).__dict__()


@need_access("delete_events")
@check_params(["id"])
def del_event():
    event_id = get_value("id", None, is_num)
    if not event_id:
        return api.ErrorResponse(400, "id must be num").__dict__()
    event_id = int(event_id)

    success = behaviour.delete_event(event_id)
    if not success:
        return api.NotFound().__dict__()
    return api.SuccessResponse().__dict__()


@need_access("edit_events")
@check_params(["id", ])
def edit_event():
    event_id = get_value("id", None, is_num)
    if not event_id:
        return api.ErrorResponse(400, "id must be num").__dict__()

    event_id = int(event_id)
    params_list = [
        "name", "short_description", "description",
        "date", "format", "photos"
    ]
    params = dict()
    for param in params_list:
        params[param] = get_value(param, None)

    if params["photos"]:
        params["photos"] = list(map(lambda x: x.strip(), params["photos"].split(",")))
    if params["date"]:
        params["date"] = is_correct_date(params["date"])
        if params["date"] is False:
            return api.ErrorResponse(400, "date in wrong format").__dict__()

    params["event_format"] = get_value("format", None)
    del params["format"]

    success = behaviour.edit_event(event_id=event_id, **params)

    if not success:
        return api.NotFound().__dict__()

    return api.SuccessResponse().__dict__()


@check_params(["event_id", ])
def get_comments():
    event_id = get_value("event_id", None, is_num)
    if not event_id:
        return api.ParamMustBeNum("event_id").__dict__()
    event_id = int(event_id)

    comments = behaviour.get_comments(event_id)

    return api.CommentsResponse(comments).__dict__()


@need_access("add_comments")
@check_params(["event_id", "text"])
def add_comment():
    event_id = get_value("event_id", None, is_num)
    text = get_value("text", None)
    if not event_id:
        return api.ParamMustBeNum("event_id").__dict__()
    event_id = int(event_id)

    user: User
    user = authorize()
    user_id = user.id
    success = behaviour.add_comment(user_id, text, event_id)
    if not success:
        return api.NotFound().__dict__()

    return api.SuccessResponse().__dict__()


@need_access("delete_comments")
@check_params(["id", ])
def delete_comment():
    comment_id = get_value("id", None, is_num)
    if not comment_id:
        return api.ParamMustBeNum("id").__dict__()
    comment_id = int(comment_id)

    success = behaviour.delete_comment(comment_id)
    if not success:
        return api.NotFound().__dict__()
    return api.SuccessResponse().__dict__()


@app.route("/events", methods=["GET", "OPTIONS"])
@cross_origin()
def index():
    query = get_value("query", "", lambda x: bool(x))
    offset = get_value("offset", 0, is_num)
    limit = get_value("limit", 5, is_num)

    events = behaviour.get_events(offset, limit, query)
    if not events:
        return api.NotFound().__dict__()
    return api.EventsResponse(events).__dict__()


@app.route("/my_events", methods=["GET", "OPTIONS"])
@check_params(["limit", "offset"])
@cross_origin()
def my_events():
    offset = get_value("offset", 0, is_num)
    limit = get_value("limit", 10, is_num)
    user: User
    user = authorize()
    if not user:
        return api.Unauthorized().__dict__()

    users_events = behaviour.get_events(offset, limit, user_id=user.id)

    return api.EventsResponse(users_events)


@check_params(["limit", "offset"])
@app.route("/own_events", methods=["GET", "OPTIONS"])
@cross_origin()
def own_events():
    offset = get_value("offset", 0, is_num)
    limit = get_value("limit", 10, is_num)
    user: User
    user = authorize()
    if not user:
        return api.Unauthorized().__dict__()

    users_events = behaviour.get_events(offset, limit, organizer_id=user.id)

    return api.EventsResponse(users_events)


@app.route("/event", methods=["GET", "POST", "DELETE", "PATCH", "OPTIONS"])
@cross_origin()
def event_path():
    if request.method == "GET":
        return get_event()
    elif request.method == "POST":
        return add_event()
    elif request.method == "DELETE":
        return del_event()
    elif request.method == "PATCH":
        return edit_event()


@app.route("/comments", methods=["GET", "POST", "DELETE", "OPTIONS"])
@cross_origin()
def comments_path():
    if request.method == "GET":
        return get_comments()
    elif request.method == "POST":
        return add_comment()
    elif request.method == "DELETE":
        return delete_comment()


@check_params(["hash_password", "email"])
@app.route("/login", methods=["POST", "OPTIONS"])
@cross_origin()
def login():
    this_request = request.values
    token = authenticate(this_request["email"], this_request["hash_password"])
    if token is False:
        return api.WrongPasswordOrEmail().__dict__()

    user = behaviour.get_user_by_id(token.user_id)
    if user is None:
        return api.AccountWasDeleted().__dict__()

    return api.SuccessResponse(
        token=token.key,
        user_id=token.user_id,
        full_name=user.full_name,
        role=user.role,
        verified=user.verified
    ).__dict__()


@app.route('/register', methods=["POST", "OPTIONS"], endpoint="account_register")
@cross_origin()
@check_params(["email", "password", "role", "full_name"])
def account_register():
    this_request = request.values

    user = registration(
        this_request["email"], this_request["full_name"],
        this_request["password"], this_request["role"]
    )
    if user:
        return api.SuccessResponse().__dict__()

    return api.RegistrationError(user.comment).__dict__()


@app.route("/verify", methods=["POST", "OPTIONS"], endpoint="account_verify")
@cross_origin()
@need_access("verify_accounts")
@check_params(["user_id"])
def account_verify():
    user_id = get_value("user_id", None, is_num)
    if not user_id:
        return api.NotFound().__dict__()
    user_id = int(user_id)

    success = behaviour.verify_account(user_id)
    if not success:
        return api.NotFound().__dict__()
    return api.SuccessResponse().__dict__()


@app.route("/accounts", methods=["GET", "OPTIONS"], endpoint="accounts")
@cross_origin()
@need_access("get_accounts_info")
@check_params(["limit", "offset"])
def accounts():
    limit = get_value("limit", None, is_num)
    offset = get_value("offset", None, is_num)

    if not limit:
        return api.ParamMustBeNum("limit").__dict__()
    if not offset:
        return api.ParamMustBeNum("offset").__dict__()

    limit = int(limit)
    offset = int(offset)
    accounts_list = behaviour.get_users(limit, offset)

    if not accounts_list:
        return api.NotFound().__dict__()
    return api.UsersResponse(accounts_list).__dict__()


@app.route("/own_account", methods=["PATCH", "OPTIONS"], endpoint="account")
@cross_origin()
@need_access("edit_own_account")
def correct_own_account():
    role = get_value("role", None)
    full_name = get_value("full_name", None)
    email = get_value("email", None)

    user: User
    user = authorize()
    if not user:
        return api.Unauthorized().__dict__()
    if role:
        if role not in all_roles_in_projects:
            return api.RoleNotFound(role).__dict__()

    user_id = user.id

    success = behaviour.edit_user(user_id, role, email, full_name)
    if not success:
        return api.BusyEmailError().__dict__()
    return api.SuccessResponse().__dict__()


@app.route("/account", methods=["PATCH", "OPTIONS"], endpoint="correct_another_account")
@cross_origin()
@need_access("edit_account_roles")
@check_params(["user_id", "role"])
def correct_another_account():
    role = get_value("role", None)
    if role not in all_roles_in_projects:
        return api.RoleNotFound(role).__dict__()
    user_id = get_value("user_id", None, is_num)
    if not user_id:
        return api.ParamMustBeNum("user_id").__dict__()
    user_id = int(user_id)

    success = behaviour.edit_user(user_id, role, None, None)

    return api.BaseResponse(200 if success else 400).__dict__()


@app.route("/event/save", methods=["POST", "DELETE", "OPTIONS"], endpoint="saving_event")
@cross_origin()
@need_access("event_save")
@check_params(["id", ])
def saving_event():
    user: User
    user = authorize()
    user_id = user.id
    event_id = get_value("id", None, is_num)

    if not event_id:
        return api.ParamMustBeNum("id").__dict__()
    event_id = int(event_id)

    if request.method == "POST":
        success = behaviour.save_event(event_id, user_id)
        if not success:
            success = api.NotFound()
        else:
            success = api.SuccessResponse()
    else:
        success = behaviour.delete_saved_event(event_id, user_id)
        if not success:
            success = api.ErrorResponse(404, "event not saved")
        else:
            success = api.SuccessResponse()

    return success.__dict__()


@app.route("/event/rate", methods=["PUT", "OPTIONS"], endpoint="rating_event")
@cross_origin()
@need_access("event_rate")
@check_params(["id", "rate"])
def rating_event():
    user: User
    user = authorize()
    user_id = user.id

    event_id = get_value("id", None, is_num)
    rate = get_value("rate", None, is_num)

    if not event_id:
        return api.ParamMustBeNum("id").__dict__()
    if not rate:
        return api.ParamMustBeNum("rate").__dict__()

    rate = int(rate)
    if not -1 <= rate <= 1:
        return api.ErrorResponse(400, "'rate' should be from -1 to 1. ").__dict__()
    event_id = int(event_id)

    success = behaviour.set_rate(event_id=event_id, user_id=user_id, rating=rate)
    if not success:
        return api.NotFound().__dict__()
    return api.SuccessResponse().__dict__()


@app.before_request
def before_request():
    """
    Данные, приходящие с фронта приходят
    не в удобном варианте.
    Этот метод нужен для упрощения всей ситуации.
    """
    if request.method == "OPTIONS":
        return
    this_request = request.data.decode("utf-8")

    if this_request:
        data = json_loads(f"{this_request}")
    else:
        data = dict()

    if not request.values:
        request.__setattr__("values", data)


@app.before_first_request
def initializing():
    if not behaviour.initialize():
        print("Initializing failed.")
        exit(-1)
