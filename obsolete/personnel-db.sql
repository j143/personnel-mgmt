CREATE TABLE departments (
  department_id INT PRIMARY KEY,
  department_name VARCHAR(50)
);

CREATE TABLE employees (
  employee_id INT PRIMARY KEY,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  email VARCHAR(100) UNIQUE,
  phone_number VARCHAR(20),
  hire_date DATE,
  job_id INT,
  salary FLOAT,
  commission_pct FLOAT,
  manager_id INT,
  department_id INT,
  CONSTRAINT fk_job FOREIGN KEY (job_id) REFERENCES jobs (job_id),
  CONSTRAINT fk_manager FOREIGN KEY (manager_id) REFERENCES employees (employee_id),
  CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments (department_id)
);

CREATE TABLE jobs (
  job_id INT PRIMARY KEY,
  job_title VARCHAR(50),
  min_salary FLOAT,
  max_salary FLOAT
);

CREATE TABLE locations (
  location_id INT PRIMARY KEY,
  street_address VARCHAR(100),
  postal_code VARCHAR(20),
  city VARCHAR(50),
  state_province VARCHAR(50),
  country_id INT,
  CONSTRAINT fk_country FOREIGN KEY (country_id) REFERENCES countries (country_id)
);

CREATE TABLE countries (
  country_id INT PRIMARY KEY,
  country_name VARCHAR(50)
);

CREATE TABLE regions (
  region_id INT PRIMARY KEY,
  region_name VARCHAR(50)
);
