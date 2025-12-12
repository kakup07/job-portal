from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from services import get_job_details, get_full_job_data
from repository import get_user_role, get_jobs_by_employer, update_response_status

employer_bp = Blueprint('employers', __name__, url_prefix='/employers')

@employer_bp.before_request
def login_check():
  user_id = session.get('user_id')
  if not user_id:
    return redirect(url_for('users.login'))
  role = get_user_role(user_id)
  if role != 'employer':
    return render_template('error.html', msg='Not Authorised')

@employer_bp.route('/jobs', methods = ['GET']) 
def jobs(): 
  status = request.args.get('status', 'all') 
  jobs = get_jobs_by_employer(session.get('user_id'), status) 
  return render_template('employer_home.html', jobs=jobs, current_filter=status)

@employer_bp.route('/jobs/<int:job_id>', methods=['GET'])
def job_details(job_id):
  user_id = session['user_id']

  data = get_full_job_data(job_id, user_id)
  if not data:
    return render_template('error.html', msg='Invalid job or unauthorized access')

  return render_template(
    'job_detail.html',
    job=data['job'],
    responses=data['responses']
  )

@employer_bp.route('/jobs/<int:job_id>/responses/<int:response_id>/accept')
def accept_response(job_id, response_id):
  update_response_status(response_id, 'accepted')
  flash('Applicant accepted')
  return redirect(url_for('employers.job_details', job_id=job_id))


@employer_bp.route('/jobs/<int:job_id>/responses/<int:response_id>/reject')
def reject_response(job_id, response_id):
  update_response_status(response_id, 'rejected')
  flash('Applicant rejected')
  return redirect(url_for('employers.job_details', job_id=job_id))

