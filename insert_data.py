import sqlite3

def create_connection():
    conn = sqlite3.connect('employees.db')
    cursor = conn.cursor()
    return conn, cursor

def create_tables():
    conn, cursor = create_connection()

    # Create the job table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS job (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            min_salary REAL NOT NULL,
            max_salary REAL NOT NULL
        );
    ''')

    # Create the employee table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            id INTEGER PRIMARY KEY,
            first_name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            hire_date TEXT NOT NULL,
            job_id INTEGER NOT NULL,
            FOREIGN KEY (job_id) REFERENCES job (id)
        );
    ''')

    conn.commit()
    cursor.close()
    conn.close()

def insert_sample_data():
    conn, cursor = create_connection()

    # Insert sample job data
    jobs_data = [
        ('Manager', 10000, 20000),
        ('Developer', 5000, 15000),
        ('Salesperson', 3000, 10000)
    ]
    add_job = "INSERT INTO job (title, min_salary, max_salary) VALUES (?, ?, ?)"
    cursor.executemany(add_job, jobs_data)

    # Insert sample employee data
    employees_data = [
        ('John', 'Doe', 'john.doe@example.com', '123-456-7890', '2022-02-19', 1),
        ('Jane', 'Doe', 'jane.doe@example.com', '234-567-8901', '2022-02-20', 2),
        ('Bob', 'Smith', 'bob.smith@example.com', '345-678-9012', '2022-02-21', 3),
        ('Alice', 'Johnson', 'alice.johnson@example.com', '456-789-0123', '2022-02-22', 1),
        ('Dave', 'Williams', 'dave.williams@example.com', '567-890-1234', '2022-02-23', 2)
    ]
    add_employee = "INSERT INTO employee (first_name, last_name, email, phone, hire_date, job_id) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(add_employee, employees_data)

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == '__main__':
    create_tables()
    insert_sample_data()
