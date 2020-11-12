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

def filter_available_creation(date_to_volunteer, username):

    with open('calendar_pull.json') as json_file:                                                  # same functionality as quickstart print, but from json file
        events = json.load(json_file)

    all_slot_dictionary = { 1 : '08:30', 2 : '09:00', 3 : '09:30', 4 : '10:00', 5 : '10:30', 6 : '11:00',
                        7 : '11:30', 8 : '12:00', 9 : '12:30', 10 : '13:00', 11 : '13:30', 12 : '14:00',
                        13 : '14:30', 14 : '15:00', 15 : '15:30', 16 : '16:00', 17 : '16:30', 18 : '17:00'}

    open_slot = all_slot_dictionary.copy()
    
    for event in events:
        if len(event['attendees']) == 2:
            if username in event['attendees'][0]['email'] or username in event['attendees'][1]['email']:
                for key in all_slot_dictionary:
                    if date_to_volunteer in event['start']['dateTime'] and all_slot_dictionary[key] in event['start']['dateTime']:
                        open_slot.pop(key)
        elif username in event['attendees'][0]['email']:
            for key in all_slot_dictionary:
                if date_to_volunteer in event['start']['dateTime'] and all_slot_dictionary[key] in event['start']['dateTime']:
                    open_slot.pop(key)

    return open_slot

def filter_available_booking(username):

    with open('calendar_pull.json') as json_file:                                                  # same functionality as quickstart print, but from json file
        events = json.load(json_file)

    
    open_slots = filter(lambda x: len(x['attendees']) == 1 and username not in x['attendees'][0]['email'], events)


    return open_slots


def filter_by_id(id):
    pass
#     print(open_slot)

# open_slots = filter(lambda x: len(x['attendees']) == 1 and user_name not in x['attendees'][0]['email'], code_clinic_events)

# all_slot_dictionary = { 1 : '08:30',
#                             2 : '10:00',
#                             3 : '11:30',
#                             4 : '13:00',
#                             5 : '14:30',
#                             6 : '16:00'}
# filter_available_creation('2020-11-11', all_slot_dictionary, 'mvan-sch')




if __name__ == '__main__':
    
    file_name = 'calendar_pull.json'
    events = read_file(file_name)

    # code_clinic_events = filter_for_codeclinic(events)
    # print("Here is a list of all the code clinic events: ")
    # for event in code_clinic_events:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])


    
    # open_slots = filter_for_open_slots(code_clinic_events)
    # print("Here is a list of all the open slots for user to book a volunteer's slot: ")
    # for event in open_slots:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])


    # user_name = 'mvan-sch'
    # not_booked = filter_empty_volunteer_slots(code_clinic_events, user_name)
    # print("Here is a list of Melt's's created slots that are still open for booking: ")
    # for event in not_booked:
    #    start = event['start'].get('dateTime', event['start'].get('date'))
    #    print(start, event['summary'])
    
 # 08:30 10:00 11:30 13:00 14:30 16:00   

