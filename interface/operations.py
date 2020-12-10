# import os, sys
# USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
# sys.path.insert(0, USER_PATHS + "/")
from google import filter
from google import calendar_api
from interface import pretty_lib as nice

def create_slot(date, time, description):
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """
    
    if filter.filter_available_creation(date, time):
        calendar_api.create_event(description, date, time)
        print("Thank you for creating a slot. Here are the details:")
        print("Date: " + str(date))
        print("Time: " + str(time))
        print("Description: " + description + ".")

    else:
        print("This date and time conflicts with another event on your calendar.")


def book_slot(id, description):
    """
    This func allows you to book a slot
    """

    open_slot = filter.filter_for_booking()

    if not open_slot:
        print("You have no elegible slots to book.")
        return

    to_book_list = []

    for event in open_slot:
        to_book_list.append(event['id'])

    if id and id in to_book_list:
        calendar_api.add_attendee(id, description)
        print(f"Thank you for booking a slot with {id}")

    elif not id:
        print('These are the slots available to book:')

        for event in open_slot:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], event['id'])

    else:
        print("Invalid ID used.")



def delete_slot(id):
    """
    As either a patient or a volenteer you can cancel a slot you have booked or created.
    """
    
    list_not_booked = filter.filter_my_empty_volunteer_slots()

    if not list_not_booked:
        print("You have no elegible slots to delete.")
        return
    
    delete_list= []

    for event in list_not_booked:
        delete_list.append(event['id'])

    if id and id in delete_list:
        calendar_api.delete_event(id)

    elif not id:
        print('These are your volunteered slots to delete:')

        for event in list_not_booked:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], event['id'])

    else:
        print("Invalid ID used.")


def cancel_booking(id):
    """
    As either a patient or a volenteer you can cancel a slot you have booked or created.
    """

    list_of_booked = filter.filter_my_patient_slots()

    if not list_of_booked:
        print("You have no elegible slots to cancel.")
        return
    
    cancel_list= []

    for event in list_of_booked:
        cancel_list.append(event['id'])

    if id and id in cancel_list:
        calendar_api.remove_attendee(id)

    elif not id:
        print('These are your booked slots to cancel:')

        for event in list_of_booked:
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(start, event['summary'], event['id'])

    else:
        print("Invalid ID used.")



def retrieve_calendar():
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """

    volunteered_events, booked_events = filter.list_of_users_clinic_events()

    # print(len(volunteered_events))
    print("Here are the events you have volunteered for:")
    nice.display_slots(volunteered_events , "SLOTS")
    

    # print(len(booked_events))
    print()
    print('Here is a list of events you booked to get some help:')
    nice.display_slots(booked_events, "BOOKED")

# You have not volunteered for anything.

# You have no booked slots.