from flask import Flask, session
from routes import user_bp, main_bp, employer_bp, job_bp, js_bp, admin_bp
from repository import get_user_name
from db import init_db
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(user_bp)
app.register_blueprint(main_bp)
app.register_blueprint(job_bp)
app.register_blueprint(employer_bp)
app.register_blueprint(js_bp)
app.register_blueprint(admin_bp)


@app.context_processor
def user_name():
  user_name = None
  user_id = session.get('user_id')
  if(user_id):
    user_name = get_user_name(user_id)
  return {'current_user': user_name}


@app.cli.command('init-db')
def init_db_command():
  init_db()
  print('Initialized the database.')

if __name__ == "__main__":
    app.run(debug=True)