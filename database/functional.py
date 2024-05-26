from psycopg2 import Error
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from database.tables import Users, Base

engine = create_engine(url="sqlite:///./db.db", echo=False)

s = sessionmaker(engine)


def get_db():
    db = s()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(engine)


def register_user_to_db(username, email, password):
    with s() as db:
        try:
            user = Users(username=username,
                         email=email,
                         password=password
                         )
            db.add(user)
            db.commit()
            return 0
        except (Exception, Error) as error:
            print(error)
            return -1


def get_user(username: str):
    db = s()
    user = db.query(Users).filter_by(username=username).first()
    return user


def username_exists_in_db(username: str) -> bool:
    db = s()
    user = db.query(Users).filter_by(username=username).first()
    return user is not None


def check_user(email, password):
    with s() as session:
        try:
            user = session.query(Users).filter_by(email=email).first()
            pas = user.password

            if pas == password:
                return 0
            else:
                return -1

        except (Exception, Error) as error:
            print(error)
            return -1


def check_role(id):
    with s() as session:
        try:
            user = session.get(Users, id)
            role_id = user.role_id
            if role_id == 0:
                return 0
            elif role_id == 1:
                return 1
            elif role_id == 2:
                return 2
            else:
                return -1

        except (Exception, Error) as error:
            print(error)
            return -1


def get_id_user(email):
    with s() as session:
        try:
            user = session.query(Users).filter_by(email=email).one()
            return user.id

        except (Exception, Error) as error:
            print(error)
            return -1


def get_password_user(email):
    with s() as session:
        try:
            user = session.query(Users).filter_by(email=email).one()
            return user.password

        except (Exception, Error) as error:
            print(error)
            return -1


def get_all_users():
    with s() as session:
        try:
            query = select(Users)
            result = session.execute(query)
            users = result.scalars().all()

            user_list = []
            user_dict = {}
            for user in users:
                user_dict['id'] = user.id
                user_dict['username'] = user.username
                user_dict['email'] = user.email
                user_dict['password'] = user.password
                user_list.append(user_dict)
                user_dict = {}
            return user_list

        except (Exception, Error) as error:
            print(error)
            return -1


create_tables()
# database_service = DatabaseService()
#
# database_service.create_tables()
