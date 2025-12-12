BEGIN;
CREATE TABLE users (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  user_type TEXT CHECK (user_type IN ('job_seeker', 'employer', 'admin')),
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  last_modified TEXT,
  file_name TEXT,
  file_path TEXT,
  company_name TEXT,
  account_status TEXT DEFAULT 'active'
);
CREATE INDEX idx_users_id ON users(id);


CREATE TABLE jobs (
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  created_by INTEGER NOT NULL,
  last_modified TEXT,
  location TEXT,
  status TEXT CHECK (status IN ('active', 'inactive')) DEFAULT 'active',
  FOREIGN KEY (created_by) REFERENCES users (id)
);
CREATE INDEX idx_jobs_id ON jobs(id);


CREATE TABLE responses (
  id INTEGER PRIMARY KEY,
  created_by INTEGER NOT NULL,
  job INTEGER NOT NULL,
  cover_letter TEXT NOT NULL,
  status TEXT CHECK (status IN ('applied', 'accepted', 'rejected')) DEFAULT 'applied',
  created_at TEXT DEFAULT CURRENT_TIMESTAMP,
  last_modified TEXT,
  FOREIGN KEY (created_by) REFERENCES users (id),
  FOREIGN KEY (job) REFERENCES jobs (id)

);
CREATE INDEX idx_responses_id ON responses(id);

COMMIT;