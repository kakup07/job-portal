from flask import Flask, session, send_from_directory, g
from routes import user_bp, main_bp, employer_bp, job_bp, js_bp, admin_bp
from repository import get_user_name
from db import init_db
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "/uploads/resumes")

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'uploads')

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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

@app.route('/uploads/<path:filename>')
def uploaded_files(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.cli.command('init-db')
def init_db_command():
  init_db()
  print('Initialized the database.')

def close_db(e=None):
  db = getattr(g, "_db", None)
  if db is not None:
    db.close()

app.teardown_appcontext(close_db)

if __name__ == "__main__":
    app.run(debug=True)