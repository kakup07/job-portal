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

def update_response_status(response_id, status):
  db = get_db()
  db.execute(
    '''
    UPDATE responses
    SET status = ?
    WHERE id = ?
    ''',
    (status, response_id),
  )
  db.commit()
