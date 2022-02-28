# Здесь происходят основные запросы к Базе Данных.
from sqlalchemy.orm.session import Session as SessionObject
from sqlalchemy.orm.query import Query
from sqlalchemy.exc import IntegrityError
from random import choice as random_choice
from datetime import datetime, timedelta

from configs import token_len, token_symbols, token_expire_date
from models import Session, User, Token, Event, EventPhoto, EventComment, EventRate
from errors import EmailAlreadyUsedError


def user_registration(email: str, full_name: str,
                      hash_password: str, role: str,
                      verified: bool = False):
    """Регистрация нового пользователя."""
    try:
        session: SessionObject
        with Session(expire_on_commit=False) as session:
            new_user = User(
                email=email,
                full_name=full_name,
                hash_password=hash_password,
                role=role,
                verified=verified
            )
            session.add(new_user)
            session.commit()
        return new_user
    except IntegrityError:
        return EmailAlreadyUsedError(email)


def verify_account(user_id: int):
    """Подтверждение аккаунта и его принадлежности."""
    session: SessionObject
    with Session() as session:
        query: Query
        user = session.query(User).get(user_id)
        user.verified = True
        session.commit()
    return True


def create_new_token(user_id: int):
    """Создание нового токена для аккаунта."""
    new_key = ""
    for i in range(token_len):
        new_key += random_choice(token_symbols)

    expire_date = datetime.now() + timedelta(seconds=token_expire_date)
    token = Token(user_id=user_id, key=new_key, expire_date=expire_date)

    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(token)
        session.commit()
    return token


def user_authenticate(email: str, hash_password: str):
    """
    Аутентификация пользователя. Выдача токена.
    None - неверный логин/пароль.
    Возвращает: TokenObject
    """
    session: SessionObject
    with Session() as session:
        query: Query
        query = session.query(User).filter(User.email == email).filter(User.hash_password == hash_password)
        user = query.all()
        if user:
            return create_new_token(user[0].id)
    return None


def user_authorize(key: str):
    """Авторизация пользователя. Сверка токена."""
    session: SessionObject
    with Session() as session:
        token = session.query(Token).filter(Token.key == key).all()
        if not token:
            return False
        token = token[0]
        if token.expire_date <= datetime.now():
            return False

        user = session.query(User).filter(User.id == token.user_id).all()
        if not user:
            return False
        user = user[0]

    return user


def get_event_by_id(event_id: int):
    """Получение события и его фотографий."""
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        event = session.query(Event).get(event_id)
        if not event:
            return None
        photos = session.query(EventPhoto).filter(EventPhoto.event_id == event_id)
        photos = photos.all()
    return {
        "event": event,
        "photos": photos
    }


def get_events(offset: int, limit: int, search_by: str):
    """Получение списка событий."""
    session: SessionObject
    with Session() as session:
        query = session.query(Event).filter(Event.name.ilike(f"%{search_by}%"))
        query = query.offset(offset)
        query = query.limit(limit)
    return query.all()


def add_event(
        name: str,
        short_description: str,
        description: str,
        event_date: datetime,
        organizer_id: int,
        event_format: str,
        photos: list):
    """
    Создание нового события.
    """
    event = Event(
        name=name,
        short_description=short_description,
        description=description,
        event_date=event_date,
        organizer_id=organizer_id,
        event_format=event_format
    )
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(event)
        session.commit()

    with Session(expire_on_commit=False) as session:
        for link in photos:
            session.add(EventPhoto(event_id=event.id, link=link))
            session.commit()

    return event


def add_comment(user_id: int, comment: str, event_id: int):
    """Добавление комментария."""
    session: SessionObject
    users_comment = EventComment(
        event_id=event_id,
        text=comment,
        user_id=user_id
    )

    with Session() as session:
        session.add(users_comment)
        session.commit()
    return True


def set_rate(event_id: int, user_id: int, rating: int):
    """Установка рейтинга для события."""
    rate = EventRate(event_id=event_id, user_id=user_id, rating=rating)

    session: SessionObject
    with Session() as session:
        query = session.query(EventRate).filter(EventRate.event_id == event_id)
        query = query.filter(EventRate.user_id == user_id)
        if not query.all():
            session.add(rate)
        else:
            rate = query.one()
            rate.rating = rating
        session.commit()

    return True


def delete_all_users():
    session: SessionObject
    with Session() as session:
        all_users = session.query(User).all()
        for user in all_users:
            session.delete(user)
        session.commit()
    return True


def get_all_users():
    session: SessionObject
    with Session() as session:
        all_users = session.query(User).all()
    return all_users
