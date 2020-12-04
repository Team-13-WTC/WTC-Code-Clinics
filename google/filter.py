import os, sys


"""
This gets the path right if the file is in another module.
"""
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
sys.path.insert(0, USER_PATHS + "/")

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from pprint import pprint
import json
from google import calendar_api
from configuration import read_config as config


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


    events = calendar_api.get_calendar().get('items', [])
    code_clinic_events = filter(lambda x: 'Code Clinic' in x['summary'], events)
    return list(code_clinic_events)


def filter_for_booking():
    '''
    Filters out events and shows only slots open for booking by checking for events without 'attendees' and removing events where user has volunteered
    :return: list of open_slots
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    open_slots = filter(lambda x: len(x['attendees']) == 1 and username not in x['creator']['email'], code_clinic_events)
    # open_slots = filter(lambda x: len(x['attendees']) == 1, code_clinic_events)
    
    return list(open_slots)


def filter_my_empty_volunteer_slots():
    '''
    Filters out code_clinic_events to show specific volunteer slots where no one has booked
    :return: list of not_booked
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    not_booked = filter(lambda x: len(x['attendees']) == 1 and username in x['creator']['email'], code_clinic_events)
    # not_booked = filter(lambda x: len(x['attendees']) == 1 and user_name in x['attendees'][0]['email'], code_clinic_events)

    return list(not_booked)


def filter_my_patient_slots():
    '''
    Filters out code_clinic_events events for events where user's patient slots are extracted
    :return: list of events where you are the patient
    '''

    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    patients_booked_slots = filter(lambda x: len(x['attendees']) == 2 and username in x['attendees'][1]['email'] and username not in x['creator']['email'], code_clinic_events)

    return list(patients_booked_slots)


def filter_available_creation(date_to_volunteer, time):
    '''
    Assesses which 30min slots may be seleted by volunteer on a specified date_to_volunteer
    :return: list of open_slots
    '''

    all_slot_dictionary =  [ '08:30',  '09:00', '09:30',  '10:00', '10:30',  '11:00',
                        '11:30',  '12:00',  '12:30',  '13:00', '13:30',  '14:00',
                         '14:30', '15:00',  '15:30',  '16:00',  '16:30', '17:00']
    
    available_creation = calendar_api.freebusy(date_to_volunteer, time)
    
    if available_creation or time not in all_slot_dictionary:
        return False
    else:
        return True



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
        if username in all_users_events['creator']['email']:
            volunteered_events.append(all_users_events)
            
        if 'attendees' in all_users_events and username not in all_users_events['creator']['email']:
            for attendee in all_users_events['attendees']:
                if username in attendee['email']:
                    booked_events.append(all_users_events)
    
    # print(len(volunteered_events))
    print("Here are the events you have volunteered for:")
    for event in volunteered_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    # print(len(booked_events))
    print('Here is a list of events you booked to get some help:')
    for event in booked_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])

    return volunteered_events, booked_events

print(filter_for_booking())