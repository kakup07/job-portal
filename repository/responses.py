from db import get_db, query_db

def create_response(job):
  db = get_db()
  db.execute(
    '''
      insert into responses(cover_letter, created_by, job) values (?, ?, ?)
    ''',
    (job['cover_letter'], job['user_id'], job['job_id']),
  )
  db.commit()