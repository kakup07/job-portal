from db import get_db, query_db

def get_all_employers():
  return query_db(
    '''
    select id, name, email, account_status, created_at
    from users
    where user_type = 'employer'
    order by created_at desc
    '''
  )

def toggle_employer_status(user_id):
  db = get_db()
  db.execute(
    '''
    update users
    set account_status = case
      when account_status = 'active' then 'inactive'
      else 'active'
    end
    where id = ?
    ''',
    (user_id,),
  )
  db.commit()

