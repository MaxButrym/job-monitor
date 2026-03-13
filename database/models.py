from sqlalchemy import Column, Integer, String
from .db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)


class Job(Base):

    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True)
    title = Column(String)