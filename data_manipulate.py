# Здесь происходят основные запросы к Базе Данных.
from models import Session
from sqlalchemy.orm.session import Session as SessionObject
from models import School


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
