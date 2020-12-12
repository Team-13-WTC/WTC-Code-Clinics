import os, sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
sys.path.insert(0, USER_PATHS + "/")

from googleapiclient.discovery import build
from google import calendar_api
from configuration import create_configuration as config


def filter_for_codeclinic():
    '''
    Filters out calendar events given to display 'code clinic' events only
    Returns: list of code_clinic_events
    '''

    events = calendar_api.get_calendar().get('items', [])
    code_clinic_events = filter(lambda x: 'Code Clinic' in x['summary'], events)
    return list(code_clinic_events)


def filter_for_booking():
    '''
    Gives all available slots that may be booked by current user. The filter 
    searches for events where there is only one person attached to the event and
    that the user did not create the event i.e. you cannot book yourself 
    for help.
    Returns: list of open_slots
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    open_slots = filter(lambda x: len(x['attendees']) == 1 and username \
                    not in x['creator']['email'] 
                    and filter_available_creation(x['start']['dateTime'][:10], 
                            x['start']['dateTime'][11:16]), code_clinic_events)
    
    return list(open_slots)


def filter_my_empty_volunteer_slots():
    '''
    Filters out code_clinic_events to show specific volunteer slots 
    where no one has booked
    Returns: list of not_booked
    '''
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    not_booked = filter(lambda x: len(x['attendees']) == 1 \
                    and username in x['creator']['email'], code_clinic_events)

    return list(not_booked)


def filter_my_patient_slots():
    '''
    Filters out code_clinic_events events for events where user's patient slots
    are extracted - this is used in cancel operation. 
    It only removes the patient.
    Returns: list of events where you are the patient
    '''

    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    patients_booked_slots = filter(lambda x: len(x['attendees']) == 2  \
                            and username in x['attendees'][1]['email'] \
                            and username not in x['creator']['email'], \
                            code_clinic_events)

    return list(patients_booked_slots)


def filter_available_creation(date_to_volunteer, time):
    '''
    Assesses which 30min slots may be seleted by volunteer on a 
    specified date_to_volunteer
    Returns: list of open_slots
    '''

    available_creation = calendar_api.freebusy(date_to_volunteer, time)
    
    if available_creation:
        return False
    else:
        return True


def list_of_users_clinic_events():
    '''
    Filters out specific users code clinic events they have 
    booked and volunteered for
    Returns: list of events booked and volunteered for
    '''
    
    username = config.retrieve_variable('username')
    code_clinic_events = filter_for_codeclinic()
    volunteered_events = []
    booked_events = []

    for event in code_clinic_events:
        if username in event['creator']['email']:
            volunteered_events.append(event)
            
        else:
            for attendee in event['attendees']:
                if username in attendee['email']:
                    booked_events.append(event)
    
    return volunteered_events, booked_events