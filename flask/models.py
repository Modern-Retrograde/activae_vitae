# Здесь происходит декларация Базы Данных.

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker

from sqlalchemy import Column
from sqlalchemy import Integer, VARCHAR, Text, TIMESTAMP, Boolean
from sqlalchemy import PrimaryKeyConstraint, ForeignKeyConstraint, UniqueConstraint


from configs import sqlalchemy_arguments, recreate_database

engine = create_engine(**sqlalchemy_arguments)
engine.connect()

Session: sessionmaker
Session = sessionmaker(bind=engine)

Base = declarative_base(bind=engine)


class User(Base):
    def __repr__(self):
        return f"<User id={self.id}, role='{self.role}'>"

    __tablename__ = "users"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    email = Column("email", VARCHAR(255), nullable=False)
    full_name = Column("full_name", Text, nullable=False)
    hash_password = Column("hash_password", VARCHAR(255), nullable=False)
    role = Column("role", VARCHAR(20), nullable=False)
    verified = Column("verified", Boolean, default=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="user_pk"),
        UniqueConstraint("email")
    )


class Token(Base):
    def __repr__(self):
        return f"<Token user_id={self.user_id}, expire_date='{self.expire_date}'>"

    __tablename__ = "tokens"

    user_id = Column("user_id", Integer, nullable=False)
    key = Column("key", VARCHAR(255), nullable=False)
    expire_date = Column("expire_date", TIMESTAMP, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("key", name="token_pk"),
        ForeignKeyConstraint(("user_id", ), ("users.id", ))
    )


class Event(Base):
    def __repr__(self):
        return f"<Event id={self.id}, name='{self.name}', organizer_id={self.organizer_id}>"

    __tablename__ = "events"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    name = Column("name", VARCHAR(50), nullable=False)
    short_description = Column("short_description", Text, nullable=True)
    description = Column("description", Text, nullable=False)
    event_date = Column("date_of_the_event", TIMESTAMP, nullable=False)
    organizer_id = Column("organizer_id", Integer, nullable=False)
    event_format = Column("event_format", Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("organizer_id", ), ("users.id", )),
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


class EventSaved(Base):
    def __repr__(self):
        return f"<EventSaved event_id={self.event_id}, user_id={self.user_id}>"

    __tablename__ = "events_saved"

    event_id = Column("event_id", Integer, nullable=False)
    user_id = Column("user_id", Integer, nullable=False)

    __table_args__ = (
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
        ForeignKeyConstraint(("user_id", ), ("users.id", )),
        PrimaryKeyConstraint("event_id", "user_id", name="saved_events_pk"),
    )


class EventComment(Base):
    def __repr__(self):
        return f"<EventComment id={self.event_id}, user_id={self.user_id}, event_id={self.event_id}>"

    __tablename__ = "events_comments"

    id = Column("id", Integer, autoincrement=True, nullable=False)
    event_id = Column("event_id", Integer, nullable=False)
    text = Column("text", VARCHAR(100), nullable=False)
    user_id = Column("user_id", Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("id", name="event_comments_pk"),
        ForeignKeyConstraint(("user_id", ), ("users.id", )),
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
    )


class EventRate(Base):
    def __repr__(self):
        return f"<EventRate rating={self.rating}, event_id={self.event_id}, user_id={self.user_id}>"

    __tablename__ = "events_rates"

    event_id = Column("event_id", Integer, nullable=False)
    user_id = Column("user_id", Integer, nullable=False)
    rating = Column("rating", Integer, nullable=False)

    __table_args__ = (
        PrimaryKeyConstraint("event_id",  "user_id", name="event_rates_pk"),
        ForeignKeyConstraint(("event_id", ), ("events.id", )),
        ForeignKeyConstraint(("user_id", ), ("users.id", )),
    )


if recreate_database and __name__ == "__main__":
    print("Recreating whole database...")
    _current_session = Session()

    Base.metadata.drop_all()
    Base.metadata.create_all(bind=engine)

    _current_session.commit()
    _current_session.close()
    print("Recreated...")
