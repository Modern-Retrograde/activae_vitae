# Здесь происходят основные запросы к Базе Данных.
from sqlalchemy.orm.session import Session as SessionObject
from sqlalchemy.orm.query import Query
from sqlalchemy.exc import IntegrityError
from random import choice as random_choice
from datetime import datetime, timedelta

from configs import token_len, token_symbols, token_expire_date
from models import Session, User, Token, Event, EventPhoto, EventComment, EventRate, EventSaved
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
        if not user:
            return False
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
    Выдаётся последний активный токен. Новый не
    будет создан, пока не истечёт срок действия
    старого.

    None - неверный логин/пароль.
    Возвращает: TokenObject
    """
    session: SessionObject
    with Session() as session:
        query: Query
        query = session.query(User).filter(User.email == email).filter(User.hash_password == hash_password)
        user = query.all()
        if not user:
            return None
        user = user[0]

        active_tokens = session.query(Token).filter(
            Token.user_id == user.id,
            Token.expire_date > datetime.now()
        ).all()

    if active_tokens:
        return active_tokens[0]
    return create_new_token(user.id)


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
        query: Query
        query = session.query(
            Event, EventSaved.is_saved
        ).filter(Event.name.ilike(f"%{search_by.lower()}%"))

        query = query.join(
            EventSaved,
            EventSaved.event_id == Event.id,
            isouter=True
        )

        query = query.offset(offset)
        query = query.limit(limit)
        query = query.distinct()
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
    photos_objects = list()
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(event)
        session.commit()

    with Session(expire_on_commit=False) as session:
        for link in photos:
            photos_objects.append(EventPhoto(event_id=event.id, link=link))
            session.add(photos_objects[-1])
        session.commit()

    return {
        "event": event,
        "photos": photos_objects
    }


def edit_event(
        event_id: int, name: str,
        short_description: str, description: str,
        date: datetime, event_format: str,
        photos: list):
    """
    Редактирует уже существующее событие.

    Введённые данные перезаписываются поверх.
    """
    session: SessionObject
    with Session() as session:
        chosen_event: Event
        chosen_event = session.query(Event).get(event_id)
        if not chosen_event:
            return False
        if name:
            chosen_event.name = name
        if short_description:
            chosen_event.short_description = short_description
        if description:
            chosen_event.description = description
        if date:
            chosen_event.event_date = date
        if event_format:
            chosen_event.event_format = event_format

        # Перезапись всех фотографий.
        if photos:
            session.query(EventPhoto).filter(EventPhoto.event_id == event_id).delete()
            for photo in photos:
                event_photo = EventPhoto(event_id=event_id, link=photo)
                session.add(event_photo)

        session.commit()
    return True


def delete_event(event_id: int):
    session: SessionObject
    with Session() as session:
        event = session.query(Event).filter(Event.id == event_id).all()
        if not event:
            return False
        event = event[0]
        session.delete(event)

        session.query(EventRate).filter(EventRate.event_id == event_id).delete()
        session.query(EventPhoto).filter(EventPhoto.event_id == event_id).delete()
        session.query(EventSaved).filter(EventSaved.event_id == event_id).delete()
        session.query(EventComment).filter(EventComment.event_id == event_id).delete()

        session.commit()
    return True


def add_comment(user_id: int, comment: str, event_id: int):
    """Добавление комментария."""
    session: SessionObject
    users_comment = EventComment(
        event_id=event_id,
        text=comment,
        user_id=user_id
    )

    with Session() as session:
        event = session.query(Event).get(event_id)
        if not event:
            return False
        session.add(users_comment)
        session.commit()
    return True


def delete_comment(comment_id: int):
    session: SessionObject
    with Session() as session:
        query = session.query(EventComment).filter(EventComment.id == comment_id)
        if not query.all():
            return False
        query.delete()
        session.commit()
    return True


def get_comments(event_id: int):
    session: SessionObject
    with Session() as session:
        comments = session.query(EventComment).filter(EventComment.event_id == event_id)
        comments = comments.all()
    return comments


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

        all_tokens = session.query(Token).all()
        for token in all_tokens:
            session.delete(token)

        session.commit()
    return True


def get_users(limit: int, offset: int):
    """Поиск пользователя по его ID"""
    session: SessionObject
    with Session() as session:
        users = session.query(User).limit(limit).offset(offset).all()
        print("292 behaviour", users)
    return users


def edit_user(user_id: int, role: str = None, email: str = None, full_name: str = None):
    session: SessionObject
    with Session() as session:
        user = session.query(User).get(user_id)
        if role:
            user.role = role
        if email:
            if session.query(User).filter(User.email == email).all():
                return False
            user.email = email
        if full_name:
            user.full_name = full_name
        session.commit()
    return True


def get_all_users():
    session: SessionObject
    with Session() as session:
        all_users = session.query(User).all()
    return all_users


def initialize():
    from configs import director_account
    from sqlalchemy.exc import OperationalError

    session: SessionObject
    with Session() as session:
        try:
            admin: User
            admin = session.query(User).get(1)
            if admin:
                return True
            admin = user_registration(**director_account)
        except OperationalError:
            print("Set recreate_database into True.\nDB possibly not configured.")
            return False

        if not admin:
            return False
    return True
