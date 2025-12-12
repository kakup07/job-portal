from flask import session, render_template, Blueprint, url_for, redirect
from repository import get_user_role

main_bp = Blueprint('main', __name__, url_prefix='/')

@main_bp.route('/', methods = ['GET'])
def home():
  user_id = session.get('user_id')
  if(user_id is None):
    return redirect(url_for('users.login'))
  role = get_user_role(user_id)
  if(role == 'job_seeker'):
    return redirect('/job_seekers/jobs')
  elif (role == 'employer'):
    return redirect(url_for('employers.jobs'))
  else:
    return redirect(url_for('admin.dashboard'))
  
@main_bp.route('/logout', methods = ['GET'])
def logout():
  session.clear()
  return redirect(url_for('main.home'))