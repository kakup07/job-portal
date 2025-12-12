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
    one=True
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

def update_user(user_id, name, email, password, company_name, resume):
  fields = []
  values = []

  fields.append("name = ?")
  values.append(name)

  fields.append("email = ?")
  values.append(email)

  if password:
      fields.append("password = ?")
      values.append(password)

  if company_name is not None:
      fields.append("company_name = ?")
      values.append(company_name)

  if resume:
      fields.append("file_path = ?")
      values.append(resume)

  values.append(user_id)
  db = get_db()
  db.execute(
    f"UPDATE users SET {', '.join(fields)} WHERE id = ?",
    tuple(values),
  )
  db.commit()

def get_user_by_id(user_id):
  return query_db(
    '''
    select 
        id,
        name,
        email,
        user_type,
        account_status,
        file_name,
        file_path,
        company_name,
        created_at
    from users
    where id = ?
    ''',
    (user_id,),
    one=True
  )