from flask import session, render_template, Blueprint, url_for, redirect, request, flash
from repository import get_user_role, get_user_by_id
from services import update_user_profile

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

@main_bp.route('/profile/edit', methods=['GET'])
def edit_profile():
  user_id = session['user_id']
  user = get_user_by_id(user_id)
  print(user)
  return render_template('profile_edit.html', user=dict(user))


@main_bp.route('/profile/edit', methods=['POST'])
def update_profile():
  user_id = session['user_id']

  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')  # optional
  company_name = request.form.get('company_name')
  resume = request.files.get('resume')

  # call service layer
  update_user_profile(
    user_id, name, email, password, company_name, resume
  )

  flash("Profile updated successfully.")
  return redirect(url_for('main.edit_profile'))