from db import query_db

def count_jobs(range_filter):
  return query_db('SELECT COUNT(*) AS total FROM jobs WHERE created_at >= DATE("now", ?)',
    (range_filter,),
    one=True
  )['total']

def count_employers(range_filter):
  return query_db(
    '''
      SELECT COUNT(*) AS total 
      FROM users 
      WHERE user_type = "employer"
      AND created_at >= DATE("now", ?)
    ''',
    (range_filter,),
    one=True
  )['total']

def count_jobseekers(range_filter):
  return query_db(
    '''
      SELECT COUNT(*) AS total 
      FROM users 
      WHERE user_type = "job_seeker"
      AND created_at >= DATE("now", ?)
    ''',
    (range_filter,),
    one=True
  )['total']

def count_responses(range_filter):
  return query_db(
    '''
      SELECT COUNT(*) AS total 
      FROM responses 
      WHERE created_at >= DATE("now", ?)
    ''',
    (range_filter,),
    one=True
  )['total']
