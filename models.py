# Здесь происходит декларация Базы Данных.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy import Column
from sqlalchemy import Integer, VARCHAR, Text, TIMESTAMP, PrimaryKeyConstraint, ForeignKeyConstraint

from configs import sqlalchemy_arguments, recreate_database

engine = create_engine(**sqlalchemy_arguments)
engine.connect()

Session: sessionmaker
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)


class School(Base):
    __tablename__ = "schools"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="school_pk"),
    )


class User(Base):
    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    hash_password = Column("hash_password", VARCHAR(255), nullable=False)
    role = Column("role", VARCHAR(20), nullable=False)
    school_id = Column("school_id", Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("id", ), ("schools.id", )),
        PrimaryKeyConstraint("id", name="user_pk")
    )


class Event(Base):
    __tablename__ = "events"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(50), nullable=False)
    description = Column("description", Text, nullable=False)
    date_of_the_event = Column("date_of_the_event", TIMESTAMP, nullable=False)
    organizer_id = Column("organizer_id", Integer, nullable=False)
    form_of_the_event = Column("form_of_the_event", VARCHAR(30), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("organizer_id", ), ("users.id", )),
        PrimaryKeyConstraint("id", name="events_pk")
    )


class EventPhoto(Base):
    __tablename__ = "event_photos"

    event_id = Column("event_id", Integer, nullable=False)
    link = Column("link", VARCHAR(50), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
        PrimaryKeyConstraint("event_id", "link", name="event_photos_pk")
    )


class SavedEvent(Base):
    __tablename__ = "saved_events"

    event_id = Column("event_id", Integer, nullable=False)
    user_id = Column("user_id", Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
        ForeignKeyConstraint(("user_id", ), ("users.id", )),
        PrimaryKeyConstraint("event_id", "user_id", name="saved_events_pk"),
    )


if recreate_database and __name__ == "__main__":
    print("Recreating whole database...")
    _current_session = Session()

    Base.metadata.drop_all()
    Base.metadata.create_all(bind=engine)

    _current_session.commit()
    _current_session.close()
    print("Recreated...")
