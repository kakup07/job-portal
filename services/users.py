from repository import add_user, validate_and_get_user, validate_email, get_user_profile, update_user
import bcrypt
import os
from werkzeug.utils import secure_filename
from flask import current_app
from werkzeug.security import generate_password_hash


def validate_password(password):
  # can add more validations
  if(len(password) > 8):
    return True
  return False


def register_user(user):
  retval = {'status': False, 'data': ''}
  try:
    if not user['name'] or not user['password'] or not user['user_type'] or not user['email']:
      retval['data'] = 'Missing required fields.'
    elif(not validate_password(user['password'])):
      retval['data'] = 'Password is short'
    elif(not validate_email(user['email'])):
      retval['data'] = 'Email already exists.'  
    elif(user['user_type'] not in ('job_seeker', 'employer')):
      retval['data'] = 'Incorrect user Type'  
    else:
      user['password'] = generate_password_hash(user['password'])
      add_user(user)
      retval['status'] = True
  except Exception as e:
    print('ERROR :: ', str(e))
    retval['data'] = 'Failure'
  return retval
    

def login_user(user):
  retval = {'status': False, 'data': ''}
  try:
    if not user.get('email') or not user.get('password'):
      retval['data'] = 'Missing required fields.'
    else:
      is_valid = False
      user_details = validate_and_get_user(user['email'])
      if(user_details):
        is_valid = bcrypt.checkpw(
          user['password'].encode('utf-8'), 
          user_details['password'].encode('utf-8')
        )
      if(is_valid):
          retval['user_id'] = user_details['id']
          retval['status'] = True
      else:
        retval['data'] = 'Invalid credentials.'
  except Exception as e:
    print('ERROR :: ', str(e))
    retval['data'] = 'Failure'
  return retval

def verify_user_profile(user):
  retval = {'status': True, 'msg': ''}
  user_details = get_user_profile(user['user_id'])
  if user_details['account_status'] == 'inactive':
    retval['status'] = False
    retval['msg'] = 'Account Inactive'
  else:
    if(user['user_type'] == 'employer'):
      if not user_details['company_name']:
        retval['status'] = False
        retval['msg'] = 'Please update company name in profile'
    else:
      if not user['file_name']:
        retval['status'] = False
        retval['msg'] = 'Please update resume in profile'
  return retval

def update_user_profile(user_id, name, email, password, company_name, resume):
  # hash password if provided
  if password.strip():
    password = hash_password(password)
  else:
    password = None  # means "don’t change"

  # save resume if provided
  resume_file_path = None
  if resume and resume.filename:
    filename = secure_filename(resume.filename)
    save_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
    resume.save(save_path)
    resume_file_path = filename
  update_user(
    user_id, name, email, password, company_name, resume_file_path
  )
