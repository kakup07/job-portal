from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from services import register_user, login_user, update_user_profile
from repository import get_user_by_id

user_bp = Blueprint('users', __name__, url_prefix='/')

@user_bp.route('/register', methods = ['GET', 'POST'])
def register():
  user_id = session.get('user_id')
  if(user_id):
    return redirect(url_for('main.home'))
  
  if(request.method == 'GET'):
    return render_template('register.html')

  result = register_user({
    'name': request.form.get('name', None),
    'email': request.form.get('email', None),
    'password': request.form.get('password', None),
    'user_type': request.form.get('user_type', None)
  })
  if(result['status']):
    flash('Registration successful. Please log in.')
    return redirect('/login')
  else:
    flash(result['data'])
    return redirect('/register')
  

@user_bp.route('/login', methods = ['GET', 'POST'])
def login():
  user_id = session.get('user_id')
  if(user_id):
    return redirect(url_for('main.home'))
  
  if(request.method == 'GET'):
    return render_template('login.html')

  result = login_user({
    'email': request.form.get('email', None), 
    'password': request.form.get('password', None)
  })

  if(result['status']):
    session['user_id'] = result['user_id']
    return redirect('/')
  else:
    flash(result['data'])
    return redirect('/login')
  
@user_bp.route('/logout', methods = ['GET'])
def logout():
  session.clear()
  return redirect(url_for('main.home'))


@user_bp.route('/profile/edit', methods=['GET'])
def edit_profile():
  user_id = session.get('user_id')
  if(not user_id):
    return redirect(url_for('main.home'))
  
  user_id = session['user_id']
  user = get_user_by_id(user_id)
  return render_template('profile_edit.html', user=dict(user))


@user_bp.route('/profile/edit', methods=['POST'])
def update_profile():
  user_id = session['user_id']

  name = request.form.get('name')
  email = request.form.get('email')
  password = request.form.get('password')  # optional
  company_name = request.form.get('company_name')
  resume = request.files.get('resume')

  update_user_profile(
    user_id, name, email, password, company_name, resume
  )

  flash("Profile updated successfully.")
  return redirect(url_for('main.edit_profile'))