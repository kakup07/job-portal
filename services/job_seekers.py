from repository import get_all_jobseekers, toggle_jobseeker_status

def admin_list_jobseekers():
  return get_all_jobseekers()

def admin_toggle_jobseeker(user_id):
  toggle_jobseeker_status(user_id)