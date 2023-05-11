import sqlite3

# Define the database file location
DATABASE = 'Corona_reservoir.db'


# Create a connection to the database
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.Row
    return conn


# Create the database schema if it doesn't exist
def create_schema():
    db = get_db()
    db.execute('''CREATE TABLE IF NOT EXISTS employees
                     (id VARCHAR(9) PRIMARY KEY,
                      first_name TEXT NOT NULL,
                       last_name TEXT NOT NULL,
                       city TEXT NOT NULL,
                       street TEXT NOT NULL,
                       number INTEGER NOT NULL,
                       birth_date DATE NOT NULL,
                      recovery_date DATE,
                      illness_date TIME)''')

    db.execute('''CREATE TABLE IF NOT EXISTS vaccines
                     (id VARCHAR(9) NOT NULL,
                      vaccination_date DATE NOT NULL,
                      vaccine_manufacturer TEXT NOT NULL,
                      PRIMARY KEY (id, vaccination_date),
                      FOREIGN KEY (id) REFERENCES employees(id) ON DELETE CASCADE)''')

    # db.execute('''CREATE TABLE IF NOT EXISTS images
    #              (id VARCHAR(9) PRIMARY KEY,
    #               image BLOB)''')

    db.execute('''CREATE TABLE IF NOT EXISTS images
                    (id VARCHAR(9) PRIMARY KEY,
                     image BLOB,
                     FOREIGN KEY (id) REFERENCES employees(id) ON DELETE CASCADE)''')

    db.commit()
    db.close()


# def do_query(query: str, params: list):
#     conn = get_db()
#     cur = conn.execute(query, params)
#     record = cur.fetchone()
#     conn.close()
#     return record


def do_query(query: str, args=()):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(query, args)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result


def insert_update_query(query: str, params) -> str:
    conn = sqlite3.connect(DATABASE)
    conn.text_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    result = cursor.lastrowid
    cursor.close()
    conn.close()
    return result


def return_image(image_id):
    # Retrieve the binary image data from the database using the ID
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT image FROM images WHERE id = ?", (image_id,))
    image_binary = cursor.fetchone()
    return image_binary


def receive_quantity_of_patients(date_to_check):
    # Query the database for all patients who were active on this day
    query = "SELECT COUNT(*) FROM employees WHERE illness_date <= ? AND recovery_date >= ?"
    db = get_db()
    count = db.execute(query, (date_to_check, date_to_check)).fetchone()[0]
    return count
