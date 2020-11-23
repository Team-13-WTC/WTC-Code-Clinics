from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta
import datetime
import os.path
import pickle
import json
from resources import read_conf as config


def populate_credentials():
    """
    TODO: write this docstring
    """
    
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']

    creds = None

    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials = creds)
        
    return service

def get_calendar():
    """
    Retrieves Code Clinic calendar and stores the events in a JSON file
    Parameter:  int - How many days in advance to retrieve the events
    Returns:    nothing
    """
    days_to_get = int(config.retrieve_variable('days_to_get'))
    calendar = config.retrieve_variable('calendar')

    service = populate_credentials()

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
    with open('calendar_pull.json', 'w') as outfile:
        json.dump(events_result, outfile, indent=4)

    return events_result


def create_event(speciality, date, time):
    """
    Sends API request to create an event
    Parameter:  title: name of event
                campus: Where the volunteer is from
                speciality: what volunteer can help with
                date: when event should be made
                time: what time event should be made
                username: username of volunteer
    Returns:    link to the event
    """
    location = config.retrieve_variable('campus')
    username = config.retrieve_variable('username')
    calendar = config.retrieve_variable('calendar')

    service = populate_credentials()

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
    }
    }

    # call API to create event
    event = service.events().insert(calendarId=calendar, body=event, sendUpdates = 'all').execute()


def add_attendee(id, support_needed):
    """
    Sends API request to add an attendee to an event
    Parameter:  id: event identifier
                username: username of attendee to be added
                support_needed: what user needs help with
    Returns:    link to the event
    """

    username = config.retrieve_variable('username')
    service = populate_credentials()
    calendar = config.retrieve_variable('calendar')

    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendar, eventId=id).execute()

    # update attendee
    event['attendees'] = [
        {'email': f"{username}@student.wethinkcode.co.za"},
    ]

    # update description
    event['description'] = f"{event['description']} - {support_needed}"

    # API call to send updated information
    service.events().update(calendarId=calendar, eventId=event['id'], body=event, sendUpdates = 'all').execute()


def remove_attendee(id):
    """
    Sends API request to remove an attendee from an event
    Parameter:  id: event identifier
    Returns:    link to the event
    """
   
    calendar = config.retrieve_variable('calendar')
    service = populate_credentials()

    # First retrieve the event from the API.
    event = service.events().get(calendarId=calendar, eventId=id).execute()

    # update attendee
    event['attendees'] = [
    ]

    # revert description to volunteer's speciality
    event['description'] = (event['description'].split(" -"))[0]

    # API call to send updated information
    service.events().update(calendarId=calendar, eventId=event['id'], body=event, sendUpdates = 'all').execute()


def delete_event(id):
    """
    Sends API request to remove an event
    Parameter:  id: event identifier
    Returns:    nothing
    """

    calendar = config.retrieve_variable('calendar')
    service = populate_credentials()

    service.events().delete(calendarId=calendar, eventId=id, sendUpdates = 'all').execute()


"""
mock function calls
"""

# get_calendar()
# create_event("anything goes", '2020-12-11', '10:00')
# add_attendee("e2lfek90lahil4ip1bt41efe54", 'my TDD broke')
# remove_attendee("e2lfek90lahil4ip1bt41efe54")
# delete_event("e2lfek90lahil4ip1bt41efe54")

