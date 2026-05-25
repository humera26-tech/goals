-- SQL script to create timesheet table manually
-- Run this in psql if Alembic migrations don't work due to corruption

CREATE TABLE IF NOT EXISTS timesheets (
    timesheet_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    task_id INTEGER,
    project_id INTEGER,
    work_date TIMESTAMP NOT NULL,
    hours_worked DOUBLE PRECISION NOT NULL,
    description VARCHAR(500),
    status VARCHAR(50) DEFAULT 'Pending',
    submitted_at TIMESTAMP,
    approved_by INTEGER,
    approved_at TIMESTAMP,
    CONSTRAINT fk_timesheet_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_timesheet_approved_by FOREIGN KEY (approved_by) REFERENCES users(id)
);

CREATE INDEX IF NOT EXISTS ix_timesheets_timesheet_id ON timesheets(timesheet_id);
