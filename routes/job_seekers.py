from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from repository import get_user_role, get_active_jobs, get_applied_jobs, get_all_jobseekers, toggle_jobseeker_status

js_bp = Blueprint('job_seekers', __name__, url_prefix='/job_seekers')

@js_bp.route('/jobs', methods = ['GET'])
def new_job():
  user_id = session['user_id']
  role = get_user_role(user_id)
  if role != 'job_seeker':
    return render_template('error.html', msg='Not Authorised')
  jobs = get_active_jobs()
  return render_template('jb_home.html', jobs=jobs)

@js_bp.route('/applications', methods = ['GET'])
def job_applied():
  user_id = session['user_id']
  role = get_user_role(user_id)
  if role != 'job_seeker':
    return render_template('error.html', msg='Not Authorised')
  job_status = request.form.get('status', 'applied')
  jobs = get_applied_jobs({
    'user_id': user_id,
    'job_status': job_status
  })
  return render_template('applied_jobs.html', jobs=jobs)

def admin_list_jobseekers():
  return get_all_jobseekers()

def admin_toggle_jobseeker(user_id):
  toggle_jobseeker_status(user_id)