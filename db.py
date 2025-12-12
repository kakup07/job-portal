import sqlite3
from flask import g, current_app

DATABASE = 'database.db'

def get_db():
  db = getattr(g, '_db', None)
  if db is None:
    db = g._db = sqlite3.connect(DATABASE)
  db.row_factory = sqlite3.Row
  return db

def init_db():
  db = get_db()
  with current_app.open_resource('schema.sql', 'r') as f:
    db.executescript(f.read())
  db.commit()

def query_db(query, args = (), one = False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv