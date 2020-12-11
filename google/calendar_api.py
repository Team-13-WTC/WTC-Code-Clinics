
from __future__ import print_function
import os, sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta
import datetime
import os.path
import pickle
import json
from google import mailer


USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
sys.path.insert(0, USER_PATHS + "/")

from configuration import create_configuration as config

def make_datetime_from_string(string):
    """
    Creates a datetime object form a given string
    Parameter:  string (yyy-mm-ddTHH:MM:00+0200)
    Returns:    datetime object
    """
    return datetime.datetime.strptime(string, "%Y-%m-%dT%H:%M:%S%z")


def get_personal_cal():
    """
    Retrieves Code Clinic calendar and stores the events in a JSON file
    Parameter:  nothing
    Returns:    Dictionary of events on the calendar
    """
    # assign variables stored in the user's config file
    days_to_get = int(config.retrieve_variable('days_to_get'))    
    service = config.user_login()
    # set start and end time of events to get
    start_filter = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    end_filter = (datetime.datetime.utcnow()+timedelta(days = days_to_get)).isoformat() + 'Z'
    # Call the Calendar API
    events_result = service.events().list(calendarId = 'primary', 
                    timeMin = start_filter, 
                    timeMax = end_filter, 
                    singleEvents = True,                              
                    orderBy = 'startTime').execute()
    my_events = events_result.get('items', [])
    return my_events


def get_calendar():
    """
    Retrieves Code Clinic calendar and stores the events in a JSON file
    Parameter:  nothing
    Returns:    Dictionary of events on the calendar
    """

    # assign variables stored in the user's config file
    days_to_get = int(config.retrieve_variable('days_to_get'))    
    calendar = config.retrieve_variable('calendar')
    service = config.user_login()

    # set start and end time of events to get
    start_filter = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    end_filter = (datetime.datetime.utcnow()+timedelta(days = days_to_get)).isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(calendarId = calendar, 
                    timeMin = start_filter, 
                    timeMax = end_filter, 
                    singleEvents = True,                              
                    orderBy = 'startTime').execute()

    # store data in json
    with open('google/calendar_pull.json', 'w') as outfile:
        json.dump(events_result, outfile, indent=4)

    return events_result


def create_event(speciality, date, time):
    """
    Sends API request to create an event
    Parameter:  speciality: what volunteer can help with
                date: when event should be made
                time: what time event should be made
    Returns:    Nothing
    """

    # assign variables stored in the user's config file
    location = config.retrieve_variable('campus')
    username = config.retrieve_variable('username')
    calendar = config.retrieve_variable('calendar')

    service = config.user_login()

    # add 30 minutes to the start time
    end_time = datetime.datetime.strptime(f"{date}{time}", '%Y-%m-%d%H:%M') + timedelta(minutes = 30)
    end_time = (str(end_time)).replace(" ", "T") + "+02:00"

    # details for the event to be created
    event = {                                                                              
    'summary': f"Code Clinic - {username}",
    'location': location,
    'description': speciality,
    'start': {
        'dateTime': f"{date}T{time}:00+02:00",
        'timeZone': 'Africa/Johannesburg',
    },
    'end': {
        'dateTime': end_time,
        'timeZone': 'Africa/Johannesburg',
    },
    'attendees':[
        {'email': f"{username}@student.wethinkcode.co.za"},
    ]
    }

    # call API to create event
    event = service.events().insert(calendarId=calendar, body=event, sendUpdates = 'all').execute()


def add_attendee(id, support_needed):
    """
    Sends API request to add an attendee to an event and notify volunteer of the booking
    Parameter:  id: event identifier
                support_needed: what user needs help with
    Returns:    link to the event
    """

    # assign variables stored in the user's config file
    username = config.retrieve_variable('username')
    service = config.user_login()
    calendar = config.retrieve_variable('calendar')

    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendar, eventId=id).execute()

    # update attendee
    event['attendees'] = [
        event['attendees'][0],
        {'email': f"{username}@student.wethinkcode.co.za"},
    ]

    # update description
    event['description'] = f"{event['description']} - {support_needed}"

    # API call to send updated information
    service.events().update(calendarId=calendar, eventId=event['id'], body=event, sendUpdates = 'all').execute()

    # call function to mail the volunteer
    mailer.booked_event(username, event)


def remove_attendee(id):
    """
    Sends API request to remove an attendee from an event
    Parameter:  id: event identifier
    Returns:    nothing
    """

    # assign variables stored in the user's config file
    username = config.retrieve_variable('username')   
    calendar = config.retrieve_variable('calendar')
    service = config.user_login()

    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendar, eventId=id).execute()

    # update attendee
    event['attendees'] = [
        event['attendees'][0],
    ]

    # revert description to volunteer's speciality
    event['description'] = (event['description'].split(" -"))[0]

    # API call to send updated information
    service.events().update(calendarId=calendar, eventId=event['id'], body=event, sendUpdates = 'all').execute()

    # call function to mail the volunteer
    mailer.cancelled_event(username, event)


def delete_event(id):
    """
    Sends API request to remove an event
    Parameter:  id: event identifier
    Returns:    nothing
    """

    # assign variables stored in the user's config file
    calendar = config.retrieve_variable('calendar')
    service = config.user_login()

    # API call to send updated information
    service.events().delete(calendarId=calendar, eventId=id, sendUpdates = 'all').execute()


def freebusy(date, time):
    """
    Sends API request to retrieve times that the calendar contains events between two time ranges
    Parameter:  date (yyy-mm-dd), time (HH:MM)
    Returns:    list of times that the calendar contains events
    """

    # assign variables stored in the user's config file
    service = config.user_login()
    username = config.retrieve_variable('username')

    # add 30 minutes to the start time
    start_filter = (make_datetime_from_string(f'{date}T{time}:00+0200')).isoformat()
    end_filter = (make_datetime_from_string(f'{date}T{time}:00+0200')+timedelta(minutes = 30)).isoformat()

    # create body to be used by Freebusy request
    busy_body = {
  "timeMin": start_filter,
  "timeMax": end_filter,
  "timeZone": 'Africa/Johannesburg',
  "items": [
    {
      "id": f'{username}@student.wethinkcode.co.za'
    }
  ]
}
    # API call to retrieve busy information
    results = service.freebusy().query(body=busy_body).execute()

    # refine returned date to only have list of busy times
    busy_dict = results[u'calendars']

    busy_list = busy_dict[f'{username}@student.wethinkcode.co.za']['busy']

    return busy_list


    
"""
mock function calls
"""

# get_calendar()
# print(freebusy('2020-12-11', '10:00'))
# create_event("anything goes", '2020-12-15', '08:00')
# add_attendee("sjfh15a9pvc8fnu0s8re49imgk", 'my TDD broke')
# remove_attendee("sjfh15a9pvc8fnu0s8re49imgk")
# delete_event("d29jdh52tuv6g9r3b9f92b0dqk")

