from db import get_db, query_db

def add_user(user):
  db = get_db()
  db.execute('insert into users(name, email, password, user_type) values (?, ?, ?, ?)', 
             (user['name'], user['email'], user['password'], user['user_type'])
            )
  db.commit()
  return True

def validate_and_get_user(email):
  user = query_db(
    'select id, password, user_type, email from users where email = ?',
    (email,),
    True
  )
  if(user):
    return user
  return None

def get_user_role(user_id):
  role = query_db(
    'select user_type from users where id = ?', 
    (user_id,),
    True
  )
  return role['user_type']

def get_user_name(user_id):
  name = query_db(
    'select name from users where id = ?', 
    (user_id,),
    True
  )
  return name['name']

def validate_email(email):
  email = query_db(
    'select id from users where email = ?', 
    (email,),
    True
  )
  return True if email is None else False

def get_user_profile(user_id):
  return query_db('''
    select file_name, company_name, account_status from users where id = ? ''',
    (user_id,),
    True
  )