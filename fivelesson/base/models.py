from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    age = Column(Integer)


class Post(Base):
    __tablename__ = 'Posts'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    body = Column(String)
    author_id = Column(Integer, ForeignKey('Users.user_id'))

    author = relationship("User")
