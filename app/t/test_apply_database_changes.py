from nose.tools import with_setup
from mock import patch
import os
from sqlalchemy import create_engine

from .. import apply_database_changes as adc
from .. import database as db

engine = None

expected_scripts = [
    '19560909-01-script.sql',
    '19790707-01-script.py',
]

here = os.path.dirname(__file__)
root = os.path.join(here, 'changes')

root_name = __name__.replace('.t.test_', '.') + '.root'
root_patch = patch(root_name, root)


def setup():
    global engine

    engine = create_engine('sqlite:///:memory:')
    db.Session.configure(bind=engine)


def teardown():
    db.Base.metadata.drop_all(bind=engine)
    db.Session.remove()

with_database = with_setup(setup, teardown)


def test_apply_database_changes():
    session = db.Session()

    with root_patch:
        # Call twice to check we don't double-apply.
        adc.main()
        adc.main()

    applied = session.query(adc.AppliedChanges).all()
    assert [c.name for c in applied] == expected_scripts
