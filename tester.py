# all the imports
import logging
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
import json


# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
NEW_COUNTER = """
INSERT INTO {table}(increment, counter) VALUES({increment}, {counter})
"""


# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
    

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
    
    
@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    app.logger.debug('index.html')
    return render_template('index.html')
    
    
@app.route('/getcounter/<increment>')
def get_counter(increment=1):
    g.db.cursor().executescript(
        NEW_COUNTER.format(table='counter', increment=increment, counter=0))
    g.db.commit()
    app.logger.debug(g.db.curser.lastrowid)
    return json.dumps(dict(cursor_id=g.db.curser.lastrowid))
    
    

if __name__ == '__main__':
    app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)))