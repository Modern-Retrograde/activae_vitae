# Здесь происходит декларация Базы Данных.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy import Column
from sqlalchemy import Integer, VARCHAR, Text, TIMESTAMP, Boolean
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint


from configs import sqlalchemy_arguments, recreate_database

engine = create_engine(**sqlalchemy_arguments)
engine.connect()

Session: sessionmaker
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)


class School(Base):
    def __repr__(self):
        return f"<School id={self.id}; name='{self.name}'>"

    __tablename__ = "schools"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(50), nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="school_pk"),
    )


class User(Base):
    def __repr__(self):
        return f"<User id={self.id}, role='{self.role}'>"

    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    email = Column("email", VARCHAR(255), nullable=False)
    full_name = Column("full_name", Text, nullable=False)
    hash_password = Column("hash_password", VARCHAR(255), nullable=False)
    role = Column("role", VARCHAR(20), nullable=False)
    school_id = Column("school_id", Integer, nullable=False)
    verified = Column("verified", Boolean, default=False)

    __table_args__ = (
        ForeignKeyConstraint(("id", ), ("schools.id", )),
        PrimaryKeyConstraint("id", name="user_pk")
    )


class Token(Base):
    def __repr__(self):
        return f"<Token user_id={self.user_id}, expire_date='{self.expire_date}'>"

    __tablename__ = "tokens"

    user_id = Column("user_id", Integer, nullable=False)
    token = Column("token", VARCHAR(255), nullable=False)
    expire_date = Column("expire_date", TIMESTAMP, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("user_id", "token", name="token_pk"),
        ForeignKeyConstraint(("user_id", ), ("users.id", ))
    )


class EventsForm(Base):
    def __repr__(self):
        return f"<EventsForm id={self.id}, name='{self.name}'>"

    __tablename__ = "events_form"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(30), nullable=False)
    description = Column("description", Text, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="events_form_pk")
    )


class Event(Base):
    def __repr__(self):
        return f"<Event id={self.id}, name='{self.name}', organizer_id={self.organizer_id}>"

    __tablename__ = "events"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(50), nullable=False)
    description = Column("description", Text, nullable=False)
    date_of_the_event = Column("date_of_the_event", TIMESTAMP, nullable=False)
    organizer_id = Column("organizer_id", Integer, nullable=False)
    event_form = Column("event_form", Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("organizer_id", ), ("users.id", )),
        ForeignKeyConstraint(("event_form", ), ("events_form.id", )),
        PrimaryKeyConstraint("id", name="events_pk")
    )


class EventPhoto(Base):
    def __repr__(self):
        return f"<EventPhoto event_id={self.event_id}, link='{self.link}'>"

    __tablename__ = "event_photos"

    event_id = Column("event_id", Integer, nullable=False)
    link = Column("link", VARCHAR(50), nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
        PrimaryKeyConstraint("event_id", "link", name="event_photos_pk")
    )


class SavedEvent(Base):
    def __repr__(self):
        return f"<SavedEvent event_id={self.event_id}, user_id={self.user_id}>"

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
