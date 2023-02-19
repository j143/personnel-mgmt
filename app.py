# Import the necessary libraries
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
db = SQLAlchemy(app)


# Define the database models
class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)


class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    min_salary = db.Column(db.Float, nullable=False)
    max_salary = db.Column(db.Float, nullable=False)


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
        hire_date = request.form['hire_date']
        job_id = request.form['job_id']
        salary = request.form['salary']
        commission_pct = request.form['commission_pct']
        manager_id = request.form['manager_id']
        department_id = request.form['department_id']

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
