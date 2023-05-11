from flask import Flask, request, jsonify, make_response, send_file
import sqlite3

from data_base import get_db, do_query, insert_update_query, return_image, receive_quantity_of_patients
from input_tests import check_date_format, checks_id, is_date_before_today, number_of_days_between_dates, is_patient, \
    amount_of_vaccines

from data_base import create_schema

app = Flask(__name__)

RECOVERY_TIME = 14


# API endpoint for retrieving all employees
@app.route('/api/employees', methods=['GET'])
def get_employees_records():
    records = do_query('SELECT * FROM employees')
    # return jsonify([dict(row) for row in records])
    return jsonify(records)


# API endpoint for retrieving a single employees by ID
@app.route('/api/employees/<int:employee_id>', methods=['GET'])
def get_employee_record(employee_id):
    record = do_query('SELECT * FROM employees WHERE id = ?', [employee_id])
    if not record:
        return jsonify({'error': 'Record not found'}), 404
    # return jsonify(dict(record))
    return jsonify(record)


# API endpoint for adding a new record to employees
@app.route('/api/employees', methods=['POST'])
def add_employee_record():
    print("add_employee_record")
    # Make sure the request contains the required fields
    if not request.json or 'city' not in request.json or 'first_name' not in request.json \
            or 'last_name' not in request.json or 'street' not in request.json \
            or 'number' not in request.json or 'birth_date' not in request.json \
            or 'recovery_date' not in request.json or 'illness_date' not in request.json:
        return jsonify({'error': 'Missing required fields'}), 400
    # Make sure the number is an integer
    try:
        number = int(request.json['number'])
    except ValueError:
        return jsonify({'error': 'number must be an integer'}), 400

    if not check_date_format(request.json['birth_date']):
        return jsonify({'error': 'Invalid date format for birth_date'}), 400

    if not is_date_before_today(request.json['birth_date']):
        return jsonify({'error': 'Invalid birth_date, An unborn person cannot be insured by a health fund'}), 400

    if request.json['illness_date'] != "None":
        if not check_date_format(request.json['illness_date']):
            return jsonify({'error': 'Invalid date format for illness_date'}), 400

        if not is_date_before_today(request.json['illness_date']):
            return jsonify({'error': 'Invalid illness_date, Future patients cannot be predicted'}), 400

    if request.json['recovery_date'] != "None":
        if not check_date_format(request.json['recovery_date']):
            return jsonify({'error': 'Invalid date format for recovery_date'}), 400
        if number_of_days_between_dates(request.json['illness_date'], request.json['recovery_date']) < RECOVERY_TIME:
            return jsonify({'error': 'A recovery date is not possible'}), 400

    try:
        # Insert the new record into the database
        record = insert_update_query(
            '''INSERT INTO employees (id, first_name, last_name, city, street, number, birth_date, recovery_date, 
            illness_date) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            [request.json['id'], request.json['first_name'], request.json['last_name'], request.json['city'],
             request.json['street'], number, request.json['birth_date'], request.json['recovery_date'],
             request.json['illness_date']])

        # Return the new record ID
        return jsonify({'id': record})

    except sqlite3.IntegrityError as e:
        # Handle the error when a duplicate ID is detected
        return jsonify({'error': 'Duplicate ID'}), 400


@app.route('/api/vaccines', methods=['GET'])
def get_vaccines_records():
    records = do_query('SELECT * FROM vaccines')
    return jsonify(records)
    # return jsonify([dict(row) for row in records])


# API endpoint for retrieving a single vaccines by ID
@app.route('/api/vaccines/<int:employee_id>', methods=['GET'])
def get_vaccines_record(employee_id):
    record = do_query('SELECT * FROM vaccines WHERE id = ?', [employee_id])
    if record is None:
        return jsonify({'error': 'Record not found'}), 404
    return jsonify(record)
    # return jsonify([dict(row) for row in record])


# API endpoint for adding a new record
@app.route('/api/vaccines', methods=['POST'])
def add_vaccines_record():
    # Make sure the request contains the required fields
    if not request.json or 'id' not in request.json or 'vaccination_date' not in request.json \
            or 'vaccine_manufacturer' not in request.json:
        return jsonify({'error': 'Missing required fields'}), 400

    # Check if the ID is valid (contains only digits and has length 9)
    if not checks_id(request.json['id']):
        return jsonify({'error': 'Invalid ID'}), 400

    # Checking whether the person is insured by the health insurance fund
    if not is_patient(request.json['id']):
        return jsonify({'error': 'It is impossible to vaccinate a person who is not a patient'}), 400

    # Check if the vaccination_date is a proper date
    if not check_date_format(request.json['vaccination_date']):
        return jsonify({'error': 'Invalid date format for vaccination_date'}), 400

    # Checks if the client has been vaccinated more than 4 times
    if amount_of_vaccines(request.json['id']) > 3:
        return jsonify({'error': 'You cannot be vaccinated more than 4 times !'}), 403

    try:
        # Insert the new record into the database
        record = insert_update_query(
            'INSERT INTO vaccines (id, vaccination_date, vaccine_manufacturer) VALUES (?, ?, ?)',
            [request.json['id'], request.json['vaccination_date'], request.json['vaccine_manufacturer']])
        # Return the new record ID
        return jsonify({'id': record})
    except sqlite3.IntegrityError as e:
        # Handle the error when a duplicate ID is detected
        return jsonify({'error': 'There will not be 2 corona vaccinations on the same day'}), 400


@app.route('/api/insert_image', methods=['POST'])
def insert_image():
    # Get the base64-encoded image data and ID from the request
    image_data = request.files.get('image')
    image_id = request.form['id']

    # Checking whether the person is insured by the health insurance fund
    if not is_patient(image_id):
        return jsonify({'error': 'It is impossible to vaccinate a person who is not patient'}), 400

    image_binary = image_data.read()

    try:
        # Insert the binary image data and ID into the database
        records = insert_update_query("INSERT INTO images (id, image) VALUES (?, ?)",
                                      (image_id, sqlite3.Binary(image_binary)))
        # Return the ID of the newly inserted record
        return jsonify({'id': records})
    except sqlite3.IntegrityError as e:
        # Handle the error when a duplicate ID is detected
        return jsonify({'error': 'There is already an image in the system for this patient'}), 400


@app.route('/api/get_image/<image_id>', methods=['GET'])
def get_image(image_id):
    image_binary = return_image(image_id)

    # If the image is not found, return a 404 error
    if image_binary is None:
        return jsonify({'error': 'Image not found'}), 404

    # Return the binary image data as a response
    response = make_response(image_binary[0])
    response.headers.set('Content-Type', 'image/jpeg')
    return response


@app.route('/api/get_unvaccinated_patients', methods=['GET'])
def get_unvaccinated_patients():
    records = do_query("SELECT id FROM vaccines GROUP BY id ")
    num_of_vaccinated_patients = len(records)
    records = do_query("SELECT id FROM employees")
    num_of_patients = len(records)
    return jsonify({'The number of clients who are not vaccinated': num_of_patients - num_of_vaccinated_patients})


# import datetime
#
#
# @app.route('/api/count_active_patients_per_day_last_month', methods=['GET'])
# def count_active_patients_per_day_last_month():
#     # Calculate the date one month ago
#     one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
#
#     # Create a list to hold the results
#     results = []
#
#     # Loop over each day in the last month
#     for i in range(30):
#         date_to_check = one_month_ago + datetime.timedelta(days=i)
#
#         # Query the database for all patients who were active on this day
#         query = "SELECT COUNT(*) FROM employees WHERE illness_date <= ? AND recovery_date >= ?"
#         db = get_db()
#         count = db.execute(query, (date_to_check, date_to_check)).fetchone()[0]
#
#         # Add the result for this day to the list of results
#         results.append({
#             'date': str(date_to_check),
#             'count': count
#         })
#
#     # Return the results as JSON
#     return jsonify(results)

#
# import datetime
# import matplotlib.pyplot as plt
#
#
# @app.route('/api/count_active_patients_per_day_last_month', methods=['GET'])
# def count_active_patients_per_day_last_month():
#     # Calculate the date one month ago
#     one_month_ago = datetime.date.today() - datetime.timedelta(days=30)
#
#     # Create a list to hold the results
#     results = []
#
#     # Loop over each day in the last month
#     for i in range(30):
#         date_to_check = one_month_ago + datetime.timedelta(days=i)
#
#         # Query the database for all patients who were active on this day
#         query = "SELECT COUNT(*) FROM employees WHERE illness_date <= ? AND recovery_date >= ?"
#         db = get_db()
#         count = db.execute(query, (date_to_check, date_to_check)).fetchone()[0]
#
#         # Add the result for this day to the list of results
#         results.append({
#             'date': str(date_to_check),
#             'count': count
#         })
#
#     # Plot the data using matplotlib
#     dates = [datetime.datetime.strptime(result['date'], '%Y-%m-%d').date() for result in results]
#     counts = [result['count'] for result in results]
#     plt.plot(dates, counts)
#     plt.xlabel('Date')
#     plt.ylabel('Number of active patients')
#     plt.title('Active Patients in the Last Month')
#     plt.grid(True)
#
#     # Save the plot to a file
#     plt.savefig('active_patients_last_month.png')
#
#     # Return the results as JSON
#     return jsonify(results)


import datetime
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt


@app.route('/api/count_active_patients_per_day_last_month', methods=['GET'])
def count_active_patients_per_day_last_month():
    # Calculate the date one month ago
    one_month_ago = datetime.date.today() - datetime.timedelta(days=30)

    # Create a list to hold the results
    results = []

    # Loop over each day in the last month
    for i in range(30):
        date_to_check = one_month_ago + datetime.timedelta(days=i)

        # Query the database for all patients who were active on this day
        query = "SELECT COUNT(*) FROM employees WHERE illness_date <= ? AND recovery_date >= ?"
        db = get_db()
        count = db.execute(query, (date_to_check, date_to_check)).fetchone()[0]

        # # Add the result for this day to the list of results
        # results.append({
        #     'date': str(date_to_check),
        #     'count': count
        # })

        # Add the result for this day to the list of results
        results.append({
            'date': str(date_to_check.day),
            'count': count
        })
    # Create the plot
    dates = [result['date'] for result in results]
    counts = [result['count'] for result in results]

    fig, ax = plt.subplots()
    ax.plot(dates, counts)

    # Save the plot to a file
    fig.savefig('plot.png')

    # Return the file as a response
    return send_file('plot.png', mimetype='image/png')

if __name__ == '__main__':
    create_schema()
    app.run()
