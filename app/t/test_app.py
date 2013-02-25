from __future__ import unicode_literals, division

from .testing import client, with_database


@with_database
def test_get_index():
    r = client.get('/')
    assert r.status_code == 200
    assert 'I have 1 users!' in r.data
