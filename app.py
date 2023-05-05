# Import the necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime


# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)


# Define the database models
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    projects = db.relationship('Project', backref='department', lazy=True)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    min_salary = db.Column(db.Float, nullable=False)
    max_salary = db.Column(db.Float, nullable=False)
    employees = db.relationship('Employee', backref='job', lazy=True)


class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    hire_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.Float, nullable=False)
    commission_pct = db.Column(db.Float, nullable=True)
    manager_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    employee_projects = db.relationship('Project', secondary='works_on', backref='project_employees', lazy=True)


class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    deliverables = db.Column(db.String(100), nullable=False)
    clients = db.Column(db.String(100), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=False)
    resources = db.Column(db.String(100), nullable=False)
    employees = db.relationship('Employee', secondary='works_on', backref='projects', lazy=True)
    # works_on = db.relationship('Employee', secondary='works_on', backref='projects', lazy=True)


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    manager = db.Column(db.String(50), nullable=False)
    functional_head = db.Column(db.String(50), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    employees = db.relationship('Employee', backref='role', lazy=True)


class WorksOn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    hours = db.Column(db.Integer, nullable=False)

with app.app_context():
    db.create_all()


# Define the routes and views
@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)


@app.route('/employee/new', methods=['GET', 'POST'])
def new_employee():
    if request.method == 'POST':
        # Get the data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']
        hire_date = datetime.strptime(request.form['hire_date'], '%Y-%m-%d').date()
        job_id = request.form['job_id']
        salary = request.form['salary']
        commission_pct = request.form['commission_pct']
        manager_id = request.form['manager_id']
        department_id = request.form['department_id']

        # Convert empty commission_pct to None
        commission_pct = commission_pct if commission_pct else None
        manager_id = manager_id if manager_id else None

        # Insert the data into the database
        employee = Employee(first_name=first_name, last_name=last_name, email=email, phone_number=phone_number,
                            hire_date=hire_date, job_id=job_id, salary=salary, commission_pct=commission_pct,
                            manager_id=manager_id, department_id=department_id)
        db.session.add(employee)
        db.session.commit()

        # Show a success message
        flash('Employee created successfully.')

        # Redirect to the homepage
        return redirect(url_for('index'))
    else:
        # Get the job and department data for the form
        jobs = Job.query.all()
        departments = Department.query.all()
        return render_template('new_employee.html', jobs=jobs, departments=departments)

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
