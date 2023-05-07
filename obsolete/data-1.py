from app import db, Department

# create and add the sample data
departments = [
    {'name': 'Engineering'},
    {'name': 'Marketing'},
    {'name': 'Sales'}
]

for d in departments:
    department = Department(name=d['name'])
    db.session.add(department)

# commit the changes
db.session.commit()
