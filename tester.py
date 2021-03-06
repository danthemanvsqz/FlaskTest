# all the imports
import logging
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify
from contextlib import closing


# configuration
DATABASE = 'flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'


NEW_COUNTER = """
INSERT INTO counter(increment, counter) VALUES({increment}, {counter})
"""

INCREMENT_COUNTER = """
UPDATE counter
SET counter={count}
WHERE rowid={rowid}
"""

RETRIEVE_COUNTER = """
SELECT *
FROM counter
WHERE rowid={rowid}
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
    app.logger.debug('Connecting to db')
    g.db = connect_db()
    g.db.row_factory = sqlite3.Row
    app.logger.debug('Successfully connected to db:\n%s', g.db)


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        app.logger.debug('Closing db')
        db.close()

@app.route('/')
def index():
    app.logger.debug('Homepage')
    return render_template('index.html')
    
    
@app.route('/getcounter')
def get_counter():
    app.logger.debug('Aquiring cursor')
    cursor = g.db.cursor()
    app.logger.debug('Cursor aquired:\n%s', cursor)
    increment = request.args.get('increment')
    counter = request.args.get('counter')
    cursor.execute(
        NEW_COUNTER.format(
            table='counter',
            increment=increment if increment else 1,
            counter=counter if counter else 0))
    lastrowid = cursor.lastrowid
    app.logger.debug('lastrowid: %s', lastrowid)
    g.db.commit()
    return jsonify(rowid=lastrowid)

@app.route('/increment/<rowid>')
def increment(rowid=None):
    app.logger.debug('Aquiring cursor')
    cursor = g.db.cursor()
    app.logger.debug('Cursor aquired:\n%s', cursor)
    cursor.execute(RETRIEVE_COUNTER.format(rowid=rowid))
    counter = cursor.fetchone()
    new_count = int(counter['counter']) + int(counter['increment'])
    cursor.execute(INCREMENT_COUNTER.format(count=new_count, rowid=rowid))
    g.db.commit()
    return jsonify(counter=new_count)
    
    

if __name__ == '__main__':
    app.run()
