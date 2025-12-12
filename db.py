import sqlite3
from flask import g, current_app
from werkzeug.security import generate_password_hash

DATABASE = 'database.db'

def get_db():
  db = getattr(g, '_db', None)
  if db is None:
    db = sqlite3.connect(DATABASE)
  db.row_factory = sqlite3.Row
  g._db = db
  return db

def init_db():
  db = get_db()
  with current_app.open_resource('schema.sql', 'r') as f:
    db.executescript(f.read())
  db.execute(
    '''
    INSERT INTO users (name, email, password, user_type)
    VALUES (?, ?, ?, ?)
    ''',
    (
      'name',
      'admin@example.com',
      generate_password_hash('admin123'),
      'admin'
    )
  )    
  db.commit()

def query_db(query, args = (), one = False):
  cur = get_db().execute(query, args)
  rv = cur.fetchall()
  cur.close()
  return (rv[0] if rv else None) if one else rv