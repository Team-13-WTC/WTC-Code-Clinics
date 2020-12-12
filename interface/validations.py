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
    """
    Checks if a date string conforms to the yyyy-mm-dd format
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
    """

    if not re.fullmatch("\d\d\d\d-\d\d-\d\d", date):
        return False

    return True


def date_valid_day(date):
    """
    Checks if a specific day and month is valid
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
    """

    # The months with 31 days
    days_31 = ['01', '03', '05', '07', '08', '10', '12']

    # The months with 30 days
    days_30 = ['04', '06', '09', '11']

    # Special case for February
    exception_days = ['02']

    date = date.split('-')

    # Check for vaild day ranges
    if date[1] not in chain(days_30, days_31, exception_days):
        return False

    elif date[1] in days_31 and not (int(date[2]) <= 31 and int(date[2]) > 0):
        return False
    
    elif date[1] in days_30 and not (int(date[2]) <= 30 and int(date[2]) > 0):
        return False

    elif date[1] in exception_days and (int(date[0]) % 4 != 0) \
            and not (int(date[2]) <= 28 and int(date[2]) > 0):
        return False

    elif date[1] in exception_days and (int(date[0]) % 4 == 0) \
            and not (int(date[2]) <= 29 and int(date[2]) > 0):
        return False
    
    return True


def date_within_30_days(date):
    """
    Checks if a given day is within 30 days of the the current date
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
    """

    # set current time and time to verify
    current_time = datetime.datetime.utcnow()
    future_time = make_datetime_from_string(date)

    # calculate diference in seconds and then days
    time_difference = current_time - future_time
    duration_in_s = time_difference.total_seconds()
    days = divmod(duration_in_s, 86400)[0]
    
    if -30 <= days <= 0:
        return True

    return False


def date_is_valid(date):
    """
    Call various validation functions to determine if given date string is valid
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
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
    """
    Checks if a time string conforms to the HH:MM format
    Parameter:  string (HH:MM)
    Returns:    True or False
    """

    if not re.fullmatch("\d\d:\d\d", time):
        return False

    return True


def time_valid_slot(time):
    """
    Checks if a time string falls on a valid time slot
    Parameter:  string (HH:MM)
    Returns:    True or False
    """

    valid_time_slot =  ['08:30', '09:00', '09:30', '10:00', '10:30', '11:00',
                        '11:30', '12:00', '12:30', '13:00', '13:30', '14:00',
                        '14:30', '15:00', '15:30', '16:00', '16:30', '17:00']

    if time not in valid_time_slot:
        return False

    return True

    
def time_is_valid(time):
    """
    Call various validation functions to determine if given time string is valid
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
    """

    if not time_correct_format(time):
        print('Incorrect time format. HH:MM')
        return False

    if not time_valid_slot(time):
        print('Incorrect time slot. Time slots are half-hourly', end = '')
        print('from 08h:30 till 17:00.')
        return False

    return True


def description_created(description):
    """
    Check if a description was given
    Parameter:  string (description)
    Returns:    True or False
    """

    if not description:
        print('Please add a description eg. -e "Add description here"')
        return False

    return True


def valid_number_format(days):
    """
    Checks if a day string conforms to the \d\d format
    Parameter:  string (yyy-mm-dd)
    Returns:    True or False
    """

    if not re.fullmatch("\d\d", days) and not re.fullmatch("\d", days):
        return False

    if not days.isdigit():
        return False

    if 0 >= int(days) > 99:
        return False

    return True


def days_created(days):
    """
    Check if amount of days were given
    Parameter:  string (days)
    Returns:    True or False
    """

    if not days:
        return False

    return True


def days_are_valid(days):
    """
    Call various validation functions to determine if given days string is valid
    Parameter:  string (\d\d)
    Returns:    True or False
    """

    if not days_created(days):
        print('Please add amount of days eg. -days "Number between 0 and 99"')
        return False

    if not valid_number_format(days):
        print('Incorrect days format. Number between 0 and 99')
        return False

    return True