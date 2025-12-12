from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from repository import get_user_role, get_job_by_id
from services import add_job, apply_job, verify_user_profile

job_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@job_bp.before_request
def login_check():
  user_id = session.get('user_id')
  if not user_id:
    return redirect(url_for('users.login'))

@job_bp.route('/new', methods = ['GET', 'POST'])
def new_job():
  role = get_user_role(session.get('user_id'))
  if role != 'employer':
    return render_template('error.html', msg='Not Authorised')
  
  if request.method == 'GET':
    return render_template('add_job.html')
  
  profile_check = verify_user_profile({'user_id': session.get('user_id'), 'user_type': role})
  if not profile_check['status']:
    flash(profile_check['msg'])
  else:
    result = add_job({
      'title': request.form.get('title', None), 
      'created_by': session.get('user_id'),
      'description': request.form.get('description', None), 
    })
    if(result['status']):
      flash('Job created.')
    else:
      flash(result['data'])
  return redirect(url_for('jobs.new_job'))

@job_bp.route('/<int:job_id>/apply', methods = ['GET', 'POST'])
def apply_new_job(job_id):
  user_id = session.get('user_id')
  role = get_user_role(user_id)
  if role != 'job_seeker':
    return render_template('error.html', msg='Not Authorised')
  
  if request.method == 'GET':
    job = get_job_by_id(job_id)
    return render_template('apply_job.html', job=job)
  
  cover_letter = request.form.get('cover_letter', None)
  result =  apply_job({
    'job_id': job_id, 
    'user_id': user_id,
    'cover_letter' : cover_letter
    })
  if(result['status']):
    flash('Applied successfully.')
    return redirect(url_for('main.home'))
  else:
    flash(result['data'])
    return redirect(url_for('jobs.apply_new_job', job_id=job_id))

  