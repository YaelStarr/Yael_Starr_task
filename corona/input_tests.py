
import datetime

from data_base import get_db, do_query

# Check if the ID is valid (contains only digits and has length 9)
def checks_id(ID: str) -> bool:
    if not ID.isdigit() or len(ID) != 9:
        return False
    return True


# Check if the date is a proper date
def check_date_format(date: str) -> bool:
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
        return True
    except ValueError:
        return False


# Check if the date is a non-future date
def is_date_before_today(date_: str) -> bool:
    try:
        # convert the date string to a date object
        date_obj = datetime.datetime.strptime(date_, '%Y-%m-%d').date()

        # get today's date
        today_date = datetime.date.today()

        # check if the date is before today's date
        return date_obj < today_date
    except:
        return False


def number_of_days_between_dates(date1: str, date2: str) -> int:
    # convert the date strings to datetime objects
    date1 = datetime.datetime.strptime(date1, '%Y-%m-%d')
    date2 = datetime.datetime.strptime(date2, '%Y-%m-%d')

    # calculate the difference between the two dates
    delta = date2 - date1

    # extract the number of days from the difference
    num_days = delta.days
    return num_days


def is_patient(ID: str) -> bool:
    record = do_query('SELECT * FROM employees WHERE id = ?', [ID])
    if record is None:
        return False
    return True


# Returns the amount of vaccinations the client received
def amount_of_vaccines(ID: str) -> int:
    records = do_query('SELECT * FROM vaccines WHERE id = ?', [ID])
    return len(records)