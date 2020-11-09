# from list_events import list_events
from pprint import pprint
import json


def read_file(file_name):

    with open(file_name) as f:
        data = json.load(f)
        # print(data)
    return data
    

def filter_for_codeclinic(events):
    '''
    Filters out calendar events given to display 'code clinic' events only
    :parameter: events
    :return: list of code_clinic_events
    '''

    #FILTER OUT ALL EVENTS WITH 'CODE CLINIC' IN SUMMARY
    code_clinic_events = filter(lambda x: 'CODE CLINIC' in x['summary'], events)
    return list(code_clinic_events)
    # pprint(code_clinic_events)


def filter_for_open_slots(code_clinic_events):
    '''
    Filters out events and shows only slots open for booking by checking for events without 'attendees'
    :parameter: code_clinic_events
    :return: list of open_slots
    '''

    # print(code_clinic_events[1]['creator'])
    # open_slots = filter(lambda x: 'attendees' not in x, code_clinic_events)
    open_slots = filter(lambda x: len(x['attendees']) == 1, code_clinic_events)
    # open_slots = filter(lambda x: 'attendees' not in x or (len(x['attendees']) > 2), code_clinic_events)
    return list(open_slots)


def filter_empty_volunteer_slots(code_clinic_events, user_name):
    '''
    Filters out code_clinic_events to show specific volunteer slots where no one has booked
    :parameter: code_clinic_events
    :return: list of not_booked
    '''
    # print(code_clinic_events[1]['creator'])
    # not_booked = filter(lambda x: 'attendees' not in x and user_name in x['creator']['email'], code_clinic_events)
    not_booked = filter(lambda x: len(x['attendees']) == 1 and user_name in x['attendees'][0]['email'], code_clinic_events)

    return list(not_booked)


if __name__ == '__main__':
    
    file_name = 'calendar_pull.json'
    events = read_file(file_name)

    code_clinic_events = filter_for_codeclinic(events)
    print("Here is a list of all the code clinic events: ")
    for event in code_clinic_events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'])


    
    open_slots = filter_for_open_slots(code_clinic_events)
    print("Here is a list of all the open slots for user to book a volunteer's slot: ")
    for event in open_slots:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'])


    user_name = 'mvan-sch'
    not_booked = filter_empty_volunteer_slots(code_clinic_events, user_name)
    print("Here is a list of Melt's's created slots that are still open for booking: ")
    for event in not_booked:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'])