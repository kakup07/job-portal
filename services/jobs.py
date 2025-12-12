from repository import create_job, get_job_details_by_id, create_response
import json

def add_job(job):
  print(job)
  retval = {'status': False, 'data': ''}
  try:
    if not job['title'] or not job['description']:
      retval['data'] = 'Missing required fields.'
    else:
      create_job(job)
      retval['status'] = True
  except Exception as e:
    print('ERROR :: ', e)
    retval['data'] = 'Failure'
  return retval

def get_job_details(job_id, user_id):
  job_details = get_job_details_by_id(job_id, user_id)
  responses = json.loads(job_details['responses'])
  responses = [] if responses is None else responses
  return {'job': job_details, 'responses': responses}

def apply_job(job):
  retval = {'status': False, 'data': ''}
  try:
    if not job['job_id']  or not job['user_id'] or not job['cover_letter']:
      retval['data'] = 'Missing required fields.'
    else:
      create_response(job)
      retval['status'] = True
  except Exception as e:
    print('ERROR :: ', e)
    retval['data'] = 'Failure'
  return retval