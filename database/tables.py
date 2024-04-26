import uuid
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import create_engine, Column, String, Integer, Boolean, ForeignKey
# from sqlalchemy import UUID as PGUUID


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    token = Column(String, default='')
