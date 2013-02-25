from nose.tools import with_setup
import os
from sqlalchemy import create_engine

from .. import apply_database_changes as adc
from .. import database as db

engine = None


def setup():
    global engine

    engine = create_engine('sqlite:///:memory:')
    db.Session.configure(bind=engine)


def teardown():
    db.Base.metadata.drop_all(bind=engine)
    db.Session.remove()

with_database = with_setup(setup, teardown)


def test_apply_database_changes():
    here = os.path.dirname(__file__)

    session = db.Session()

    adc.apply_changes(session,
                      os.path.join(here, 'changes'),
                      True)

    applied = session.query(adc.AppliedChanges).all()
    assert [c.name for c in applied] == ['19790707-01-script.sql']
