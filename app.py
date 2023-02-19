from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

conn = sqlite3.connect('employees.db', check_same_thread=False)

# @app.route('/')
# def hello_world():  # put application's code here
#     return 'Hello World!'

@app.route('/')
def index():
    # Fetch all employees from the database
    c = conn.cursor()
    c.execute('SELECT * FROM employees')
    employees = c.fetchall()

    # Render the employees template with the employee data
    return render_template('employees.html', employees=employees)


@app.route('/new_employee', methods=['GET', 'POST'])
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
        c = conn.cursor()
        c.execute(
            'INSERT INTO employees (first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id, department_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (first_name, last_name, email, phone_number, hire_date, job_id, salary, commission_pct, manager_id,
             department_id))
        conn.commit()

        # Redirect to the home page
        return redirect(url_for('index'))

    # Render the new employee form
    return render_template('new_employee.html')


if __name__ == '__main__':
    app.run()
