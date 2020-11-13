# This is Maitar code, this gives the direct path for files not in the current folder (instead of cd.. which brings you out of a folder, python doent do that).


# Imports needed for interface to work
import volunteer
import patient



def name():
    """
    Connects to the login and brings in user_name from login name e.g KBintcli
    """
    # This needs to be completed with the user login name.
    print("**************************************")
    print("**Welcome to WTC Code_Clinic booking**")
    print("**************************************")
    user_name = input("What is your username? ")
    if user_name.lower() == 'voldermort':
        print("We welcome you, our Dark Lord.")
    else:
        print("Welcome " + user_name + "!")
    return user_name


def patient_or_volunteer(user_name, command, command_list):
    """
    Determin's if the patient is a volenteer. This should be in another function as both user_interface and volenteer_interface use it.
    """
    # we need to keep a variable saying if the user is a volunteer or a patient
    user_type = 'patient'
    user_input = input("Are you a patient or volunteer? ")

    if user_input.lower() == "patient":
        user_type = 'patient'
        user_help(user_name, command, user_type, command_list)
    elif user_input.lower() == 'volunteer':
        user_type = 'volunteer'
        user_help(user_name, command, user_type, command_list)
    else:
        print("Sorry I cant do that.")
        patient_or_volunteer(user_name, command, command_list)


def validate(user_name, command, user_type, command_list):
    """
    Checks if the command is valid.
    """
    user_input = input("What would you like to do? ")
    command = 0
    # This is a varaible for checking if it is a mutaual command between patient and volunteer.
    not_same = 0
    
    if user_input.lower() == 'off':
        print("This session has ended...")
        return False
    elif user_input.lower() == 'help':
        command = 'help'
        not_same = 1
        user_help(user_name, command, user_type, command_list)
    elif not user_input.lower() in command_list:
        print("Sorry that is an invalid command.")
        not_same = 1
        validate(user_name, command, user_type, command)

    if user_type == 'patient' and not_same == 0:
        if user_input.lower() == 'book':
            command = 'book'
            patient.patient(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'cancel':
            command = 'cancel'
            patient.patient(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'check':
            command = 'check'
            patient.patient(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'create':
            command = 'create'
            patient.patient(user_name, command, user_type,  command_list)
    elif user_type == 'volunteer' and not_same == 0:
        if user_input.lower() == 'book':
            command = 'book'
            volunteer.volunteer(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'cancel':
            command = 'cancel'
            volunteer.volunteer(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'check':
            command = 'check'
            volunteer.volunteer(user_name, command, user_type,  command_list)
        elif user_input.lower() == 'create':
            command = 'create'
            volunteer.volunteer(user_name, command, user_type,  command_list)
        

def user_help(user_name, command, user_type, command_list):
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
    validate(user_name, command, user_type, command_list)


def start():
    command_list = ['book', 'cancel', 'check', 'create', 'help', 'off', 'refresh']
    command = 0
    user_name = name()
    user_type = patient_or_volunteer(user_name, command, command_list)
    if user_type == 'patient':
        patient.patient(user_name, command, user_type)
    elif user_type == 'volunteer':
        volunteer.volunteer(user_name, command, user_type)


if __name__ == "__main__":
    start()