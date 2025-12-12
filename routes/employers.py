from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from services import get_job_details
from repository import get_user_role, get_jobs_by_employer

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

@employer_bp.route('/jobs/<int:job_id>', methods = ['GET'])
def job_details(job_id):
  user_id = session['user_id']
  job_details = get_job_details(job_id, user_id)
  print(job_details)
  return render_template('job_detail.html', job=job_details['job'], responses=job_details['responses'])