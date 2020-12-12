import os, sys
USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
sys.path.insert(0, USER_PATHS + "/")
from google import filter
from google import calendar_api
from interface import pretty_lib as nice
from configparser import ConfigParser
from configuration.create_configuration import full_config


def create_slot(date, time, description):
    """
    As a user you can create a slot on your calendar for volunteering purposes.
    Parameter: date
    Parameter: time
    Parameter: description of what the user can help with
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
    This func allows you to book a patient slot if there are available volunteer
    slots that have been created already
    Parameter: event id
    Parameter: description of what the user needs help with
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
        print(f"Thank you for booking a slot.")

    elif not id:
        print('These are the slots available to book:')
        nice.display_slots(open_slot, "AVAILABLE SLOTS")

    else:
        print("Invalid ID used.")


def delete_slot(id):
    """
    User can delete the slots they have created as a volunteer. Will not show
    slots the user has created where another student (patient) has booked their
    event.
    Paramter: event id
    Return: list of volunteer events user may delete with corresponding id's
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
        print(f"Your slot has been deleted.")

    elif not id:
        print('These are your volunteered slots to delete:')
        nice.display_volunteerd(list_not_booked, "VOLUNTEERD SLOTS")

    else:
        print("Invalid ID used.")


def cancel_booking(id):
    """
    User can delete the slots they have booked as a patient
    Paramter: event id
    Return: list of patient events user may delete with corresponding id's
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
        print(f"You have cancelled your booking successfully.")

    elif not id:
        print('These are your booked slots to cancel:')
        nice.display_slots(list_of_booked, "BOOKED SLOTS")

    else:
        print("Invalid ID used.")


def retrieve_calendar():
    """
    User can view all their code clinic calendar events
    """

    volunteered_events, booked_events = filter.list_of_users_clinic_events()

    if volunteered_events:
        print("Here are the events you have volunteered for:")
        nice.display_slots(volunteered_events , "VOLUNTEERD SLOTS")
    else:
        print("You have not volunteered slots.")
    

    if booked_events:
        print()
        print('Here is a list of events you booked to get some help:')
        nice.display_booked_slots(booked_events, "BOOKED")
    else:
        print("You have no booked slots.")


def update_config_date(days):
    """
    Changes the no_of_calendar_days stored in config file
    Paramter: days
    """

    config_object = ConfigParser()
    config_object.read(full_config)

    config_object["user_info"]['days_to_get'] = days

    with open(full_config, 'w') as update:
        config_object.write(update)

    print(f"Amount of days to retrieve has been updated to {days}")


def retrieve_personal_cal():
    """
    User you can check their personal/primary calendar events
    """
    personal_events = calendar_api.get_personal_cal()
    if personal_events:
        print("Here are the events in your primary calendar:")
        nice.display_personal(personal_events, "PERSONAL")
    else:
        print("There are no events to display.")


def get_help():
    start_bold = "\033[1m"
    end_bold = "\033[0;0m"

    print(start_bold+ """
    Here is a list of commands available to use that can be used in the 
    code-clinic booking programme:
    wtc-clinic [command arg]""" + end_bold +"""

    -v or --volunteer -date "yyyy-mm-dd" -time "HH:MM" -e "enter description here"
    -b or --book -id "xxx" -e "enter description here"
    -c or --cancel -id "xxx"
    -d or --delete -id "xxx"
    -r or --retrieve
    -p or --personal
    -u -days "enter a number here"
    -h or --help: Command displays all commands available to the code-clinic 
    booking system.
        
    *For detailed information on what each command does, just add the single 
    letter flag to -h.
    e.g for more help on:
    -v --> python3 code_clinic.py -hv
    -b --> python3 code_clinic.py -hb
    -c --> python3 code_clinic.py -hc
    -d --> python3 code_clinic.py -hd
    -r --> python3 code_clinic.py -hr
    -p --> python3 code_clinic.py -hp
    -u --> python3 code_clinic.py -hu
    """)


def get_more_help_change_days():
    print("""
------------------------------------------------------------------------------------------
    >> -u -days:
    The change days command allows you to alter the number of days you wish to
    work with
    on your calendars.

    Eg: -u -days 10
-----------------------------------------------------------------------------------------
    """)


def get_more_help_volunteer():
    print("""
-----------------------------------------------------------------------------------------
    >> -v or --volunteer:

    When using the "volunteer" command you as the user will volunteer your time 
    to assist a fellow WTC student at either the JHB or CT campus. This operation
    will create an event on your personal WTC Google calendar. 
    
    ARGUMENTS FOR CLI:
    The -v or --volunteer command requires 3 additional arguments:

    -date --> With this flag enter the date you wish to volunteer for yyyy-mm-dd
    -time --> With this flag enter the time you wish to volunteer for HH:MM
        *note: Valid times are houly or half-hourly ONLY!
        i.e. 08:00 and 13:30 are VALID, 08:15 and 13:50 are INVALID
    -e --> Add a description to your event (mandatory)

    Eg: -v -date 2020-12-18 -time 09:00 -e "I can't help you with recursion."
-----------------------------------------------------------------------------------------
    """)


def get_more_help_book():
    print("""
-----------------------------------------------------------------------------------------
    >> -b --book:
    "wtc-clinic -b" will display slots that are available to you to book. Once 
    you have selected the best suited slot by selecting the event id, the event
    will be added to your personal WTC Google calendar. 

    ARGUMENTS FOR CLI:

    The -b or --book command requires 2 additional arguments:
    -id --> With this flag copy the event id corresponding to the time of your
    choosing
    -e --> Add a description to your booking (mandatory)
    
    Eg: -b -id 4i3ngbd4ghj... -e "I need help with lambdas."
-----------------------------------------------------------------------------------------
    """)


def get_more_help_retrieve():
    print("""
------------------------------------------------------------------------------------------
    >> -r --retrieve:
    The retrieve command displays all your booked and volunteered for code clinic
    events.

    Eg: -r
-----------------------------------------------------------------------------------------
    """)


def get_more_help_personal():
    print("""
------------------------------------------------------------------------------------------
    >> -p or --personal:
    The personal command displays all your personal calendar events.

    Eg: -p
-----------------------------------------------------------------------------------------
    """)


def get_more_help_cancel():
    print("""
-----------------------------------------------------------------------------------------
    >> -c or --cancel:
    "wtc-clinic -c" will diplay a list of slots you have booked as a patient and
    their corresponding event id's.

     ARGUMENTS FOR CLI:

    The -c or --cancel command requires 1 additional arguments:
    -id --> With this flag copy the event id corresponding to the time of your
    choosing

     Eg: -c -id 4i3ngbd4ghj...
    
    *note: If someone has already booked a slot you created as a volunteer you
    will NOT be able to cancel the event.
-----------------------------------------------------------------------------------------
    """)


def get_more_help_delete():
    print("""
-----------------------------------------------------------------------------------------
    >> -d or --delete:
    "wtc-clinic -d" will diplay a list of unbooked events you have created as a
    volunteer and their corresponding event id's.  If someone has already booked
    a slot you created as a volunteer you will NOT be able to cancel the event.

    ARGUMENTS FOR CLI:

    The -d or --delete command requires 1 additional arguments:
    -id --> With this flag copy the event id corresponding to the time of your
    choosing

     Eg: -d -id 4i3ngbd4ghj...
-----------------------------------------------------------------------------------------
    """)
