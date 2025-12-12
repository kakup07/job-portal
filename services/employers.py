from repository import get_all_employers, toggle_employer_status
import json

def admin_list_employers():
  return get_all_employers()

def admin_toggle_employer(user_id):
  toggle_employer_status(user_id)
