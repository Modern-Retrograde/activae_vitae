# Здесь происходят основные запросы к Базе Данных.
from datetime import datetime
from sqlalchemy.orm.session import Session as SessionObject
from sqlalchemy.orm import Query

from models import Session
from models import School, Event, EventPhoto
from models import SavedEvent, EventsForm

from errors import EventPhotoNotFoundError, SavedEventNotFoundError
from errors import EventsFormNotFoundError


def add_school(school_name: str):
    session: SessionObject
    with Session() as session:
        new_school = School(name=school_name)
        session.add(new_school)
        session.commit()

        school = session.query(School).order_by(School.id.desc()).first()
        return school


def get_schools_by_name(school_name: str):
    session: SessionObject
    with Session() as session:
        schools = session.query(School).filter(School.name.ilike(f"%{school_name}%")).all()
        return schools


def delete_school(school_id: int):
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
    return True, event


def delete_event(event_id: int):
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        event = session.query(Event).get(event_id)
        session.delete(event)
        session.commit()
    return True, event


def add_photo_to_event(link: str, event_id: int):
    session: SessionObject
    photo = EventPhoto(event_id=event_id, link=link)
    with Session(expire_on_commit=False) as session:
        session.add(photo)
        session.commit()
    return True, photo


def delete_photo_from_event(link: str, event_id: int):
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        photo = session.query(EventPhoto).filter(
            EventPhoto.event_id == event_id and EventPhoto.link == link
        )
        photo = photo.all()
        if not photo:
            return EventPhotoNotFoundError(event_id, link)
        photo = photo[0]
        session.delete(photo)
        session.commit()
    return True, photo


def get_photos_event(event_id: int):
    session: SessionObject
    with Session() as session:
        query: Query
        query = session.query(EventPhoto).filter(EventPhoto.event_id == event_id)
        return query.all()


def add_saved_event(user_id: int, event_id: int):
    saved_event = SavedEvent(user_id=user_id, event_id=event_id)
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(saved_event)
        session.commit()
    return True, saved_event


def delete_saved_event(user_id: int, event_id: int):
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        saved_event = session.query(SavedEvent).filter(
            SavedEvent.event_id == event_id and SavedEvent.user_id == user_id
        ).all()
        if not saved_event:
            raise SavedEventNotFoundError(event_id, user_id)
        saved_event = saved_event[0]
        session.delete(saved_event)
        session.commit()
    return True, saved_event


def get_saved_events(user_id: int):
    session: SessionObject
    with Session() as session:
        saved_events = session.query(SavedEvent).filter(SavedEvent.user_id == user_id)
        return saved_events.all()


def add_events_form(events_form_name: str, description: str):
    events_form = EventsForm(name=events_form_name, description=description)
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        session.add(events_form)
        session.commit()
    return True, events_form


def delete_events_form(event_form_id: int):
    session: SessionObject
    with Session(expire_on_commit=False) as session:
        events_form = session.query(EventsForm).filter(EventsForm.id == event_form_id)
        events_form = events_form.all()
        if not events_form:
            raise EventsFormNotFoundError(event_form_id)
        events_form = events_form[0]

        session.delete(events_form)
        session.commit()
        return True, events_form
