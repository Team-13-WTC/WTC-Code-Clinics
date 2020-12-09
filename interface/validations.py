from itertools import chain
import datetime
import re

def make_datetime_from_string(string):
    """
    Creates a dattime object form a given string
    Parameter:  string (yyy-mm-ddTHH:MM:00+0200)
    Returns:    datetime object
    """
    return datetime.datetime.strptime(string, "%Y-%m-%d")

def date_correct_format(date):

    if not re.search("\d\d\d\d-\d\d-\d\d", date):
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
        print('incorrect date format')
        return False
    
    elif not date_valid_day(date):
        print('Invalid month/day combination')
        return False

    elif not date_within_30_days(date):
        print('Selected date not within 30 days')
        return False

    return True

def time_correct_format(time):

    if not re.search("\d\d:\d\d", time):
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
        print('incorrect time format')
        return False

    if not time_valid_slot(time):
        print('incorrect time slot')
        return False

    return True

def description_created(description):

    if not description:
        print('Please add a description')
        return False

    return True