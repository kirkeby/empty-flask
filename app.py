from __future__ import unicode_literals, division

from flask import Flask
from flask.ext.genshi import Genshi, render_response
import os

import database as db

app = Flask(__name__)
app.genshi = Genshi(app)

app.config['DEBUG'] = 'DEBUG' in os.environ
app.config['TESTING'] = 'TESTING' in os.environ
app.config['PROPAGATE_EXCEPTIONS'] = True

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = not app.config['DEBUG']

@app.route('/')
def get_index():
    greeting = 'I have %d users!' % db.Session().query(db.User).count()
    app.logger.debug('get index: %s', greeting)
    return render_response('index.html', {'greeting': greeting})
