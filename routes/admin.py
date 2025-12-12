from flask import session, render_template, Blueprint, url_for, redirect, request, flash
from services import get_admin_stats, admin_list_jobs, admin_delete_job, admin_toggle_job, admin_list_employers, admin_toggle_employer, admin_toggle_jobseeker, admin_list_jobseekers
from repository import get_user_role

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
def admin_guard():
    user_id = session.get('user_id')
    if not user_id:
        return render_template('error.html', msg='Login required')

    role = get_user_role(user_id)
    if role != 'admin':
        return render_template('error.html', msg='Not Authorised')

@admin_bp.route('/dashboard', methods = ['GET'])
def dashboard():
  range = request.args.get('range', 'daily')
  stats = get_admin_stats(range)
  return render_template(
    'admin_dashboard.html',
    stats=stats,
    current_range=range
  )

@admin_bp.route('/jobs')
def admin_jobs():
  jobs = admin_list_jobs()
  return render_template('admin_jobs.html', jobs=jobs)


@admin_bp.route('/jobs/<int:job_id>/toggle')
def admin_job_toggle(job_id):
  admin_toggle_job(job_id)
  flash('Job status updated')
  return redirect('/admin/jobs')


@admin_bp.route('/jobs/<int:job_id>/delete')
def admin_job_delete(job_id):
  admin_delete_job(job_id)
  flash('Job deleted successfully')
  return redirect('/admin/jobs')

@admin_bp.route('/employers')
def admin_employers():
  employers = admin_list_employers()
  return render_template('admin_employers.html', employers=employers)

@admin_bp.route('/employers/<int:user_id>/toggle')
def admin_toggle_employer_route(user_id):
  admin_toggle_employer(user_id)
  flash('Employer status updated')
  return redirect('/admin/employers')

@admin_bp.route('/jobseekers')
def admin_jobseekers():
  seekers = admin_list_jobseekers()
  return render_template('admin_jobseekers.html', seekers=seekers)

@admin_bp.route('/jobseekers/<int:user_id>/toggle')
def admin_toggle_jobseeker_route(user_id):
  admin_toggle_jobseeker(user_id)
  flash('Jobseeker status updated')
  return redirect('/admin/jobseekers')
