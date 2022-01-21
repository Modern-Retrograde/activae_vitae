# Здесь происходят основные запросы к Базе Данных.
import datetime
from sqlalchemy.orm.session import Session as SessionObject
from sqlalchemy.orm import Query
from random import choice as random_choice

from models import Session
from models import School, Event, EventPhoto
from models import SavedEvent, EventsForm
from models import User, Token
from configs import token_len, token_symbols, token_expire_date
from errors import EmailAlreadyUsedError, SchoolNotFoundError


def add_school(school_name: str):
    """
    Добавляет школы.
    Возвращает объект School.
    """
    session: SessionObject
    with Session() as session:
        new_school = School(name=school_name)
        session.add(new_school)
        session.commit()

        school = session.query(School).order_by(School.id.desc()).first()
    return school


def get_schools_by_name(school_name: str):
    """
    Поиск школы по имени (по номеру).

    Возвращает объект [School, School...].
    """
    session: SessionObject
    with Session() as session:
        schools = session.query(School).filter(School.name.ilike(f"%{school_name}%")).all()
    return schools


def get_school_by_id(school_id: int):
    session: SessionObject
    with Session() as session:
        school = session.query(School).get(school_id)
    return school


def delete_school(school_id: int):
    """
    Ищет, затем удаляет из БД школу по её ID.

    Возвращает bool: была ли школа в БД.
    """
    session: SessionObject
    with Session() as session:
        school = session.query(School).get(school_id)
        if school:
            session.delete(school)
            session.commit()
    return bool(school)


def add_event(event_name: str, description: str,
              date_of_the_event: datetime,
              organizer_id: int, event_form: int):
    """
    Добавляет новое мероприятие.

    Возвращает объект Event.
    """
    session: SessionObject
    event = Event(
        name=event_name,
        description=description,
        date_of_the_event=date_of_the_event,
        organizer_id=organizer_id,
        event_form=event_form
    )
    with Session(expire_on_commit=False) as session:
        session.add(event)
        session.commit()
    return event


def delete_event(event_id: int):
    """
    Удаляет указанное мероприятие.

    Возвращает bool: было ли событие.
    """
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        event = session.query(Event).get(event_id)
        if event:
            session.delete(event)
            session.commit()
    return bool(event)


def add_photo_to_event(link: str, event_id: int):
    """
    Добавляет фотографию к событию.

    Возвращает объект EventPhoto.
    """
    session: SessionObject
    photo = EventPhoto(event_id=event_id, link=link)
    with Session(expire_on_commit=False) as session:
        session.add(photo)
        session.commit()
    return photo


def delete_photo_from_event(link: str, event_id: int):
    """
    Ищет фотографию.
    Удаляет её из события.

    Возвращает bool: была ли фотография прикреплена.
    """
    session: SessionObject
    with Session() as session:
        photos = session.query(EventPhoto).filter(
            EventPhoto.event_id == event_id and EventPhoto.link == link
        )
        photos = photos.all()
        if photos:
            session.delete(photos[0])
            session.commit()
    return bool(photos[0])


def get_photos_event(event_id: int):
    """
    Ищет все фотографии, прикреплённые к событию.

    Возвращает [EventPhoto, EventPhoto...]
    """
    session: SessionObject
    with Session() as session:
        query: Query
        query = session.query(EventPhoto).filter(EventPhoto.event_id == event_id)
    return query.all()


def add_saved_event(user_id: int, event_id: int):
    """
    Добавить событие в сохранённые.

    Возвращает объект SavedEvent.
    """
    saved_event = SavedEvent(user_id=user_id, event_id=event_id)
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(saved_event)
        session.commit()
    return saved_event


def delete_saved_event(user_id: int, event_id: int):
    """
    Удаляет сохранённое событие.

    Возвращает bool: было ли сохранённое событие.
    """
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        saved_events = session.query(SavedEvent).filter(
            SavedEvent.event_id == event_id and SavedEvent.user_id == user_id
        ).all()
        if saved_events:
            session.delete(saved_events[0])
            session.commit()
    return bool(saved_events)


def get_saved_events(user_id: int):
    """
    Получение всех сохранённых событий у пользователя.

    Возвращает [SavedEvent, SavedEvent...]
    """
    session: SessionObject
    with Session() as session:
        saved_events = session.query(SavedEvent).filter(SavedEvent.user_id == user_id)
    return saved_events.all()


def add_events_form(events_form_name: str, description: str):
    """
    Добавляет форму проведения мероприятия.

    Возвращает объект EventsForm.
    """
    events_form = EventsForm(name=events_form_name, description=description)
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(events_form)
        session.commit()
    return events_form


def delete_events_form(event_form_id: int):
    """
    Удаляет форму проведения мероприятия.

    Возвращает объект EventsForm.
    """
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        events_form = session.query(EventsForm).filter(EventsForm.id == event_form_id)
        events_form = events_form.all()
        if events_form:
            events_form = events_form[0]
            session.delete(events_form)
            session.commit()

    return bool(events_form)


def create_new_user(email: str, full_name: str, hash_password: str, role: str, school_id: int):
    """Создаёт нового пользователя в Базу."""
    new_user = User(
        email=email, full_name=full_name,
        hash_password=hash_password, role=role,
        school_id=school_id
    )

    session: SessionObject
    with Session() as session:
        session.add(new_user)
        session.commit()
    return new_user


def is_email_free(email: str):
    """Проверяет, не занята ли указанная почта."""
    session: SessionObject
    with Session() as session:
        email = session.query(User).filter(User.email == email).all()
    return bool(email)


def user_register(email: str, full_name: str, hash_password: str, role: str, school_id: int):
    """Регистрация пользователя с поднятием соответствующей ошибки."""
    if not is_email_free(email):
        raise EmailAlreadyUsedError(email)
    if not get_school_by_id(school_id):
        raise SchoolNotFoundError(school_id)

    return True, create_new_user(email, full_name, hash_password, role, school_id)


def user_authorize(token: str):
    """
    Сверка токена, авторизация пользователя.
    """
    session: SessionObject
    with Session() as session:
        tokens = session.query(Token).get(token).all()
        if not tokens:
            token = None
        else:
            token = tokens[0]
            if token.expire_date <= datetime.datetime.now():
                token = None
    return bool(token)


def create_token(session: SessionObject = None):
    """
    Создание нового токена.
    Токен гарантированно уникален.
    """
    new_token = ""
    for _ in range(token_len):
        new_token += random_choice(token_symbols)

    if not session:
        session: SessionObject
        with Session() as session:
            token_exists = session.query(Token).get(Token.token == new_token).all()
            if token_exists:
                return create_token(session)
        return token_exists

    token_exists = session.query(Token).get(Token.token == new_token).all()
    if token_exists:
        return create_token(session)
    return token_exists


def user_authenticate(email: str, hash_password: str):
    """Сверка логина и пароля. Получение нового токена."""
    session: SessionObject
    with Session() as session:
        user = session.query(User).filter(User.email == email, User.hash_password == hash_password).all()
        if user:
            user = user[0]
            expire_date = datetime.datetime(
                0, 0, 0,
                second=datetime.datetime.now().second + token_expire_date
            )
            token = Token(user_id=user.id, token=create_token(), expire_date=expire_date)
        else:
            token = None

    return token
