from db import query_db, get_db

def get_all_jobseekers():
  return query_db(
    '''
    select id, name, email, account_status, created_at
    from users
    where user_type = 'job_seeker'
    order by created_at desc
    '''
  )

def toggle_jobseeker_status(user_id):
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