from repository import count_jobs, count_employers, count_jobseekers, count_responses, get_all_jobs, toggle_job_status, delete_job

def map_range_to_filter(range_key):
  interval_map = {
    'weekly': '-7 days',
    'monthly': '-1 month',
    'yearly': '-1 year',
    'daily': '0 days'
  }
  return interval_map.get(range_key, '-7 days')

def get_admin_stats(range_key):
  range_filter = map_range_to_filter(range_key)
  stats = {
      'total_jobs': count_jobs(range_filter),
      'total_employers': count_employers(range_filter),
      'total_jobseekers': count_jobseekers(range_filter),
      'total_responses': count_responses(range_filter)
  }
  return stats

def admin_list_jobs():
    return get_all_jobs()

def admin_toggle_job(job_id):
    toggle_job_status(job_id)

def admin_delete_job(job_id):
    delete_job(job_id)

