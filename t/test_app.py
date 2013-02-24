from __future__ import unicode_literals, division

import os
from sqlalchemy import create_engine

from app import app
import database as db

if os.environ['DATABASE_URL'] != 'sqlite:///:memory:':
    raise AssertionError('The test-scripts are *destructive*; '
                         'do not run them against a real database.')

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

def test_get_index():
    r = client.get('/')
    assert r.status_code == 200
    assert 'I have 1 users!' in r.data
