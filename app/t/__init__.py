import os
if os.environ['DATABASE_URL'] != 'sqlite:///:memory:':
    raise AssertionError('The test-scripts are *destructive*; '
                         'do not run them against a real database.')
