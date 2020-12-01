# This is Maitar code, this gives the direct path for files not in the current folder (instead of cd.. which brings you out of a folder, python doent do that).
# from interface.volunteer_interface.volunteer import check_bookings
import os, sys

# USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
# sys.path.insert(0, USER_PATHS + "/")

# Imports needed for interface to work
from interface import volunteer
from interface import patient
from google import filter



def patient_or_volunteer(command, command_list):
    """
    Determine's if the patient is a volenteer. This should be in another function as both user_interface and volenteer_interface use it.
    """
    # we need to keep a variable saying if the user is a volunteer or a patient
    user_type = input("Are you a patient or volunteer? ")

    if user_type.lower() == "patient":
        user_type = 'patient'
    elif user_type.lower() == 'volunteer':
        user_type = 'volunteer'
    else:
        print("Sorry that is not a possible type.")
        patient_or_volunteer(command, command_list)
    return user_type


def validate(command, command_list):
    """
    Checks if the command is valid.
    """

    user_input = sys.argv[1]

    command = 0

    if user_input.lower() == 'help':
        command = 'help'
        user_help(command, command_list)
    elif user_input.lower() == 'create':
        command = 'create'
        user_type = volunteer
        volunteer.create_slot(command, command_list)
    elif user_input.lower() == 'book':
        command = 'book'
        user_type = patient
        patient.book_slot(command, command_list)
    elif user_input.lower() == 'check':
        command = 'check'
        user_type = patient_or_volunteer(command, command_list)
        if user_type.lower() == 'patient':
            patient.check_bookings(command, command_list)
        elif user_type.lower() == 'volunteer':
            volunteer.check_bookings(command, command_list)
    elif user_input.lower() == 'cancel':
        command = 'cancel'
        user_type = patient_or_volunteer(command, command_list)
        if user_type.lower() == 'patient':
            patient.cancel_bookings(command, command_list)
        elif user_type.lower() == 'volunteer':
            volunteer.cancel_bookings(command, command_list)
    elif not user_input.lower() in command_list:
        print("Sorry that is an invalid command.")
        print("This session has ended...")
        return False


    
def user_help(command, command_list):
    """
    This prints out all the available commands in the terminal
    """
    print("You can:")
    print(" > Book - As a patient you can book a slot.")
    print(" > Cancel - As either a patient or a volenteer you can cancel a slot you have booked or created")
    print(" > Create - As a volenteer you can create a slot.")
    print(" > Check - As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created")
    print(" > Help - Displays all the help commands.")
    print(" > Off - Turns of the Code Clinic")
    print("This session has ended...")
    return False


def start():
    command_list = ['book', 'cancel', 'check', 'create', 'help', 'refresh']
    command = 0
    validate(command, command_list)



def check_bookings(command, command_list):
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """

    filter.list_of_users_clinic_events()


#     # print("Loading.. ")
#     # print("You have these slots booked: ")
#     # print("Here are your booked slots: ")


#     # print("Here are your empty slots: ")


#     # print("This session has ended...")
#     # return 