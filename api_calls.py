from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from datetime import timedelta
import datetime
import os.path
import pickle
import json

"""
TODO:   change calendar_id to be a variable retrieved from config instead of hard coded
        days_to_get variable retrieved from config instead of sent as a parameter
        username variable retrieved from config instead of sent as a parameter
        location variable retrieved from config instead of sent as a parameter


"""

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

def get_calendar(days_to_get):
    """
    Retrieves Code Clinic calendar and stores the events in a JSON file
    Parameter:  int - How many days in advance to retrieve the events
    Returns:    nothing
    """

    service = populate_credentials()

    # set start and end time of events to get
    start_filter = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time

    end_filter = (datetime.datetime.utcnow()+timedelta(days = days_to_get)).isoformat() + 'Z'
    
    # Call the Calendar API
    events_result = service.events().list(calendarId = 'ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', 
                    timeMin = start_filter, 
                    timeMax = end_filter, 
                    singleEvents = True,                              
                    orderBy = 'startTime').execute()

    # store data in json
    with open('calendar_pull.json', 'w') as outfile:
        json.dump(events_result, outfile, indent=4)


def create_event(location, speciality, date, time, username):
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
    event = service.events().insert(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', body=event, sendUpdates = 'all').execute()


def add_attendee(id, username, support_needed):
    """
    Sends API request to add an attendee to an event
    Parameter:  id: event identifier
                username: username of attendee to be added
                support_needed: what user needs help with
    Returns:    link to the event
    """

    service = populate_credentials()

    # First retrieve the event from the API.
    event = service.events().get(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', eventId=id).execute()

    # update attendee
    event['attendees'] = [
        {'email': f"{username}@student.wethinkcode.co.za"},
    ]

    # update description
    event['description'] = f"{event['description']} - {support_needed}"

    # API call to send updated information
    service.events().update(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', eventId=event['id'], body=event, sendUpdates = 'all').execute()


def remove_attendee(id):
    """
    Sends API request to remove an attendee from an event
    Parameter:  id: event identifier
    Returns:    link to the event
    """
   
    service = populate_credentials()

    # First retrieve the event from the API.
    event = service.events().get(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', eventId=id).execute()

    # update attendee
    event['attendees'] = [
    ]

    # revert description to volunteer's speciality
    event['description'] = (event['description'].split(" -"))[0]

    # API call to send updated information
    service.events().update(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', eventId=event['id'], body=event, sendUpdates = 'all').execute()


def delete_event(id):
    """
    Sends API request to remove an event
    Parameter:  id: event identifier
    Returns:    nothing
    """

    service = populate_credentials()

    service.events().delete(calendarId='ugs23ckjeisrk564oao0va6d3o@group.calendar.google.com', eventId=id, sendUpdates = 'all').execute()


"""
mock function calls
"""

# get_calendar(30)
# create_event("CPT", "anything goes", '2020-12-10', '10:00', 'not_valid')
# add_attendee("22dptob08akf4lklv2j9d37sbc", "not_valid", 'my TDD broke')
# remove_attendee("22dptob08akf4lklv2j9d37sbc")
# delete_event("22dptob08akf4lklv2j9d37sbc")

