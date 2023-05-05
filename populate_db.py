from flask import Flask
from app import db, Department, Job, Employee, Project, WorksOn

from datetime import datetime

# create Flask app object
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# create app context
app.app_context().push()

# Create the departments
hr_department = Department(name='Human Resources')
sales_department = Department(name='Sales')
engineering_department = Department(name='Engineering')

# Add the departments to the database
db.session.add_all([hr_department, sales_department, engineering_department])
db.session.commit()

# Create the jobs
hr_manager = Job(title='HR Manager', min_salary=5000, max_salary=7000)
hr_generalist = Job(title='HR Generalist', min_salary=4000, max_salary=5000)
sales_representative = Job(title='Sales Representative', min_salary=3000, max_salary=4000)
software_engineer = Job(title='Software Engineer', min_salary=6000, max_salary=8000)

# Add the jobs to the database
db.session.add_all([hr_manager, hr_generalist, sales_representative, software_engineer])
db.session.commit()

# # Create the employees
# john_smith = Employee(first_name='John', last_name='Smith', email='john.smith@example.com',
#                       phone_number='555-1234', hire_date='2022-01-01', salary=6000, department=engineering_department,
#                       job=software_engineer)
# Create the employees
john_smith = Employee(first_name='John', last_name='Smith', email='john.smith@example.com',
                      phone_number='555-1234', hire_date=datetime.strptime('2022-01-01', '%Y-%m-%d'), salary=6000, department_id=engineering_department.id,
                      job_id=software_engineer.id)

jane_doe = Employee(first_name='Jane', last_name='Doe', email='jane.doe@example.com',
                    phone_number='555-5678', hire_date=datetime.strptime('2022-01-01', '%Y-%m-%d'), salary=5000, department_id=hr_department.id,
                    job_id=hr_manager.id, manager_id=john_smith.id)

# Add the employees to the database
db.session.add_all([john_smith, jane_doe])
db.session.commit()

# Create the projects
project1 = Project(start_date=datetime.strptime('2022-01-01', '%Y-%m-%d'), end_date=datetime.strptime('2022-06-30', '%Y-%m-%d'), deliverables='Design and implement new feature',
                   clients='Acme Corp', department=engineering_department, resources='Python, Flask, PostgreSQL')
project2 = Project(start_date=datetime.strptime('2022-02-01', '%Y-%m-%d'), end_date=datetime.strptime('2022-05-31', '%Y-%m-%d'), deliverables='Develop marketing strategy',
                   clients='Globex Corp', department=sales_department, resources='Salesforce, Hubspot')
project3 = Project(start_date=datetime.strptime('2022-03-01', '%Y-%m-%d'), end_date=datetime.strptime('2022-08-31', '%Y-%m-%d'), deliverables='Improve HR policies and procedures',
                   clients='Internal', department=hr_department, resources='HRIS')

# Add the projects to the database
db.session.add_all([project1, project2, project3])
db.session.commit()

# Assign employees to projects
# WorksOn(employee=jane_doe, project=project1, hours=40)
# WorksOn(employee=jane_doe, project=project2, hours=20)
# WorksOn(employee=john_smith, project=project1, hours=60)

# Assign employees to projects
jane_doe_works_on1 = WorksOn(employee_id=jane_doe.id, project=project1, hours=40)
jane_doe_works_on2 = WorksOn(employee_id=jane_doe.id, project=project2, hours=20)
john_smith_works_on1 = WorksOn(employee_id=john_smith.id, project=project1, hours=60)

# # Add the works on relationships to the database
# db.session.add_all([WorksOn(employee=jane_doe, project=project1, hours=40),
#                     WorksOn(employee=jane_doe, project=project2, hours=20),
#                     WorksOn(employee=john_smith, project=project1, hours=60)])

db.session.add_all([jane_doe_works_on1, jane_doe_works_on2, john_smith_works_on1])
db.session.commit()
