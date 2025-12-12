from db import get_db, query_db

def get_jobs_by_employer(user_id, status):
  query = f'''
      select 
          j.id,
          j.title,
          j.status,
          datetime(j.created_at, '+5 hours', '+30 minutes') as created_at,
          count(r.id) as response_count
      from jobs j
      inner join users u on u.id = j.created_by
      left join responses r on r.job = j.id
      where u.id = ? and {'true ' if status is 'all' else 'j.status = ? '}
      group by j.id, j.title, j.status, j.created_at
      order by j.created_at desc
  '''
  return query_db(
    query,
    (user_id,) if status is 'all' else (user_id, status),
    False
  )

def create_job(job):
  db = get_db()
  db.execute('insert into jobs(title, description, created_by) values (?, ?, ?)', 
             (job['title'], job['description'], job['created_by'])
            )
  db.commit()

def get_job_details(job_id, employer_id):
  return query_db(
    '''
    select 
        j.id,
        j.title,
        j.description,
        j.status,
        datetime(j.created_at, '+5 hours', '+30 minutes') as created_at
    from jobs j
    join users u on u.id = j.created_by
    where j.id = ? and u.id = ?
    ''',
    (job_id, employer_id),
    one=True
  )

def get_job_responses(job_id):
  return query_db(
    '''
    select
        r.id,
        r.cover_letter,
        r.status,
        datetime(r.created_at, '+5 hours', '+30 minutes') as created_at,
        u.name,
        u.email,
        u.file_name,
        u.file_path
    from responses r
    join users u on u.id = r.created_by
    where r.job = ?
    order by r.created_at desc
    ''',
    (job_id,)
  )


def get_job_details_by_id(id, user_id):
  job = query_db(
    '''
      select 
        j.id,
        j.title,
        j.description,
        j.status,
        datetime(j.created_at, '+5 hours', '+30 minutes') as created_at,
        json_group_array(
          json_object(
            'id', r.id,
            'cover_letter', r.cover_letter,
            'status', r.status,
            'name', u2.name,
            'email', u2.email,
            'file_name', u2.file_name,
            'file_path', u2.file_path
          )
        ) AS responses      
      from jobs j
        inner join users u on u.id = j.created_by
        left join responses r on r.job = j.id
        left join users u2 on u2.id = r.created_by
      where
        j.id = ? and u.id = ?
    ''',
    (id,user_id),
    True
  )
  return job


def get_active_jobs(user_id):
  return query_db(
    '''
    select
      j.id,
      j.title,
      datetime(j.created_at, '+5 hours', '+30 minutes') AS created_at,
      u.name AS employer_name,
      u.company_name AS company_name
    from jobs j
    inner join users u ON u.id = j.created_by
    where 
      j.status = 'active'
      AND NOT EXISTS (
        select 1 
        from responses r
        where r.job = j.id
          AND r.created_by = ?
      )
    order by j.created_at DESC
    ''',
    (user_id,),
    False
  )


def get_job_by_id(job_id):
  return query_db(
    '''
      select id, title, description from jobs where id = ?
    ''',
    (job_id,),
    True
  )

def get_applied_jobs(job):
  return query_db(
    '''
    select 
      j.id AS job_id,
      j.title,
      j.description,
      u.company_name,
      u.name AS employer_name,
      j.status AS job_status,
      r.status AS response_status,
      r.cover_letter,
      datetime(r.created_at, '+5 hours', '+30 minutes') AS response_created_at
    from jobs j
    inner join responses r ON r.job = j.id
    inner join users u ON u.id = j.created_by
    where r.created_by = ? and r.status = ?
    ''',
    (job['user_id'], job['job_status']),
    False
  )

def get_all_jobs():
  return query_db(
    '''
    select 
        j.id,
        j.title,
        j.status,
        j.created_at,
        u.name as employer_name
    from jobs j
    join users u on u.id = j.created_by
    order by j.created_at desc
    '''
  )

def toggle_job_status(job_id):
  db = get_db()
  db.execute(
    '''
    update jobs
    set status = case 
      when status = 'active' then 'inactive'
      else 'active'
    end
    where id = ?
    ''',
    (job_id,)
  )
  db.commit()

def delete_job(job_id):
  db = get_db()
  db.execute(
    'delete from jobs where id = ?',
    (job_id,)
  )
  db.commit()