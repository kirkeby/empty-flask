from __future__ import unicode_literals, division

from datetime import datetime
import os
from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, Integer, String, \
                       Date, DateTime, Boolean
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import func
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from werkzeug.utils import cached_property

# Configure engine and create session class.
engine = create_engine(os.environ['DATABASE_URL'])

Session = scoped_session(sessionmaker(bind=engine))

# Create declarative mappings.
Base = declarative_base()

# Database errors.
class DatabaseError(Exception):
    pass

class NoSuchUser(DatabaseError):
    pass

class UserExists(DatabaseError):
    pass

# Database mappings.
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    created = Column(DateTime, nullable=False)
    login = Column(String, unique=True, nullable=False)

    @classmethod
    def create(cls, login):
        user = User()
        user.login = login
        user.password_hash = 'x'
        user.created = datetime.utcnow()
        Session().add(user)

        try:
            Session().flush()
        except IntegrityError:
            raise UserExists('User already exists: %s' % login)

        return user

    @classmethod
    def get(cls, id):
        try:
            return Session().query(User).get(id)
        except NoResultFound:
            raise NoSuchUser('No such user: %d' % id)

    @classmethod
    def find(cls, login):
        try:
            return (Session()
                        .query(User)
                        .filter(func.lower(User.login) == login.lower())
                        .one())
        except NoResultFound:
            raise NoSuchUser(login)
