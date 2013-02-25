#!/usr/bin/env python

'Apply database-changes scripts.'

from datetime import datetime
from glob import glob
import os
import sys
from sqlalchemy import Column, String, DateTime

from .database import Session, Base

here = os.path.dirname(__file__)


# The database migration models
class AppliedChanges(Base):
    __tablename__ = 'applied_changes'

    applied = Column(DateTime, nullable=False)
    name = Column(String, primary_key=True)


def parse_sql_script(f):
    return filter(None, [s.strip() for s in f.read().strip().split('\n\n')])


def apply_script(session, script):
    with open(script) as file:
        if script.endswith('.sql'):
            cnx = session.connection()
            for statement in parse_sql_script(file):
                cnx.execute(statement)

        elif script.endswith('.py'):
            code = compile(file.read(), script, 'exec')
            eval(code, {'session': session})


def apply_changes(session, root, really):
    applied = 0

    AppliedChanges.__table__.create(session.get_bind(), checkfirst=True)

    for script in sorted(glob(os.path.join(root, '*'))):
        if script.endswith('~'):
            continue

        name = os.path.basename(script)
        if session.query(AppliedChanges).get(name):
            continue

        print 'Applying %s . . .' % name
        applied += 1

        if really:
            apply_script(session, script)

        change = AppliedChanges(applied=datetime.utcnow(), name=name)
        session.add(change)
        session.commit()

    if not applied:
        print 'No database-changes is good news!'


def main():
    really = '-n' not in sys.argv
    root = os.path.join(here, 'sql', 'changes')

    session = Session()
    try:
        apply_changes(session, root, really)
    finally:
        Session.remove()

if __name__ == '__main__':
    main()
