from itertools import chain
import datetime
import re

def make_datetime_from_string(string):
    """
    Creates a dattime object form a given string
    Parameter:  string (yyy-mm-dd)
    Returns:    datetime object
    """
    return datetime.datetime.strptime(string, "%Y-%m-%d")

def date_correct_format(date):

    if not re.fullmatch("\d\d\d\d-\d\d-\d\d", date):
        return False

    return True

def date_valid_day(date):

    # The months with 31 days to see if the date is valid
    days_31 = ['01', '03', '05', '07', '08', '10', '12']

    # The months with 30 days to see if the date is valid
    days_30 = ['04', '06', '09', '11']

    # Seperates feburaruy cause it has 28 days
    exception_days = ['02']

    date = date.split('-')

    if date[1] not in chain(days_30, days_31, exception_days):
        return False

    elif date[1] in days_31 and not (int(date[2]) <= 31 and int(date[2]) > 0):
        return False
    
    elif date[1] in days_30 and not (int(date[2]) <= 30 and int(date[2]) > 0):
        return False

    elif date[1] in exception_days and (int(date[0]) % 4 != 0) and not (int(date[2]) <= 28 and int(date[2]) > 0):
        return False

    elif date[1] in exception_days and (int(date[0]) % 4 == 0) and not (int(date[2]) <= 29 and int(date[2]) > 0):
        return False
    
    return True


def date_within_30_days(date):

    current_time = datetime.datetime.utcnow()

    future_time = make_datetime_from_string(date)

    time_difference = current_time - future_time

    duration_in_s = time_difference.total_seconds()

    days = divmod(duration_in_s, 86400)[0]
    
    if -30 <= days <= 0:
        return True

    return False


def date_is_valid(date):
    """
    This is the date the user wants to book a new slot.
    """
    
    if not date_correct_format(date):
        print('Incorrect date format. yyyy-mm-dd')
        return False
    
    elif not date_valid_day(date):
        print('That is not a real date.')
        return False

    elif not date_within_30_days(date):
        print('Selected date not within 30 days from today.')
        return False

    return True

def time_correct_format(time):

    if not re.fullmatch("\d\d:\d\d", time):
        return False

    return True

def time_valid_slot(time):

    valid_time_slot =  ['08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
                        '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                        '14:30', '15:00', '15:30', '16:00', '16:30', '17:00']

    if time not in valid_time_slot:
        return False

    return True

    
def time_is_valid(time):

    if not time_correct_format(time):
        print('Incorrect time format. HH:MM')
        return False

    if not time_valid_slot(time):
        print('Incorrect time slot. Time slots are half-hourly from 08h:30 till 17:00.')
        return False

    return True

def description_created(description):

    if not description:
        print('Please add a description eg. -e "Add description here"')
        return False

    return True