from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
import json
import api_calls
from resources import read_conf as config


def read_file(file_name):

    with open(file_name) as f:
        data = json.load(f)
        # print(data)
    return data
    

def filter_for_codeclinic():
    '''
    Filters out calendar events given to display 'code clinic' events only
    :return: list of code_clinic_events
    '''

    events = api_calls.get_calendar().get('items', [])
    code_clinic_events = filter(lambda x: 'Code Clinic' in x['summary'], events)
    return list(code_clinic_events)


def filter_for_open_slots():
    '''
    Filters out events and shows only slots open for booking by checking for events without 'attendees' and removing events where user has volunteered
    :return: list of open_slots
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    open_slots = filter(lambda x: 'attendees' not in x and username not in x['creator']['email'], code_clinic_events)
    # open_slots = filter(lambda x: len(x['attendees']) == 1, code_clinic_events)
    
    return list(open_slots)


def filter_empty_volunteer_slots():
    '''
    Filters out code_clinic_events to show specific volunteer slots where no one has booked
    :return: list of not_booked
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    not_booked = filter(lambda x: 'attendees' not in x and username in x['creator']['email'], code_clinic_events)
    # not_booked = filter(lambda x: len(x['attendees']) == 1 and user_name in x['attendees'][0]['email'], code_clinic_events)

    return list(not_booked)


def filter_empty_patient_slots():
    '''
    Filters out code_clinic_events events for events where user's patient slots are extracted
    :return: list of events where you are the patient
    '''

    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    patients_booked_slots = filter(lambda x: 'attendees' in x and username in x['attendees'][0]['email'] and username not in x['creator']['email'], code_clinic_events)

    return list(patients_booked_slots)


def filter_available_creation(date_to_volunteer):
    '''
    Assesses which 30min slots may be seleted by volunteer on a specified date_to_volunteer
    :return: list of open_slots
    '''

    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()

    all_slot_dictionary = { 1 : '08:30', 2 : '09:00', 3 : '09:30', 4 : '10:00', 5 : '10:30', 6 : '11:00',
                        7 : '11:30', 8 : '12:00', 9 : '12:30', 10 : '13:00', 11 : '13:30', 12 : '14:00',
                        13 : '14:30', 14 : '15:00', 15 : '15:30', 16 : '16:00', 17 : '16:30', 18 : '17:00'}

    open_slot = all_slot_dictionary.copy()

    for event in code_clinic_events:

        if 'attendees' not in event:
            if username in event['creator']['email']:
                for key in all_slot_dictionary:
                    if date_to_volunteer in event['start']['dateTime'] and all_slot_dictionary[key] in event['start']['dateTime']:
                        open_slot.pop(key)
       
        elif len(event['attendees']) == 1:
            if username in event['attendees'][0]['email']:
                    for key in all_slot_dictionary:
                        if date_to_volunteer in event['start']['dateTime'] and all_slot_dictionary[key] in event['start']['dateTime']:
                            open_slot.pop(key)
    return open_slot


def list_of_users_clinic_events():
    '''
    Filters out specific users code clinic events they have booked and volunteered for
    :return: list of events booked and volunteered for
    '''
    
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    volunteered_events = []
    booked_events = []

    
    for all_users_events in code_clinic_events:
        if 'attendees' not in all_users_events and username in all_users_events['creator']['email']:
            volunteered_events.append(all_users_events)
            
        if 'attendees' in all_users_events and username not in all_users_events['creator']['email']:
            for attendee in all_users_events['attendees']:
                if username in attendee['email']:
                    booked_events.append(all_users_events)
    
    print(len(volunteered_events))
    print("Here are the events you have volunteered for:")
    for event in volunteered_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    print(len(booked_events))
    print('Here is a list of events you booked to get some help:')
    for event in booked_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return volunteered_events, booked_events

