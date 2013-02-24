from __future__ import unicode_literals, division

from nose.tools import with_setup
from sqlalchemy import create_engine

from app import app
import database as db

__all__ = ['client']

client = app.test_client()
engine = None

def setup():
    global engine

    engine = create_engine('sqlite:///:memory:')
    db.Session.configure(bind=engine)
    db.Base.metadata.create_all(bind=engine)
    db.User.create('root')
    db.Session.commit()

def teardown():
    db.Base.metadata.drop_all(bind=engine)
    db.Session.remove()

with_database = with_setup(setup, teardown)
