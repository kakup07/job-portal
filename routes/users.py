from flask import Blueprint, request, render_template, flash, redirect, url_for, session
from services import register_user, login_user

user_bp = Blueprint('users', __name__, url_prefix='/')

@user_bp.before_request
def login_check():
    user_id = session.get('user_id')
    if(user_id):
      return redirect(url_for('main.home'))

@user_bp.route('/register', methods = ['GET', 'POST'])
def register():
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
  print('here')
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