import os, sys

USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
sys.path.insert(0, USER_PATHS + "/")

# import user
#from vol_interface import volunteer
from google import filter
from google import calendar_api


def book_slot(command, command_list):
    """
    This func allows you to book a slot
    """
    proceed = input("Would you like to book a slot? (y/n) ")
    
    if proceed == 'y':
        print("These are the slots available for booking'.")
        
        # These functions are to keep this current function from looking to messy. They hold the data needed to collect.


        #Need this from the api
        # user_name = 'Fille'

        open_slot = filter.filter_for_booking()
        book_dict = {}
        count = 1

        for event in open_slot:
            book_dict[count] = event['id']
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(count, start, event['summary'])
            count = count + 1

        time = int(input("Choose a time slot. ")) #timing() 
        #location = user_location()
        description = user_description()
        calendar_api.add_attendee(book_dict[int(time)], description)
        #title = "Title: CODE CLINIC PATIENT"

        # print("Thank you for booking a slot. Here are the details")
        # print("Date: " + str(date))
        # print("Title: CODE CLINIC PATIENT")
        # print("Volunteer:" + user_name)
        # if location == 'CPT':
        #     print("Location: Cape Town main campus.")
        # else:
        #     print("Location: Johanesburg campus 3.")
        # print("Time: " + str(time))
        # print("Description: " + description + ".")
        print("This session has ended...")
        return False
    elif proceed == 'n':
        print("This session has ended...")
        return False
    else:
        print("Sorry that is invalid.")
        book_slot(command, command_list)


def user_location():
    """
    This helps with sorting out if the review is going to be from CPT OR JHB.
    """

    location = input("Are you from JHB or CPT? ")

    if location.upper() == 'CPT':
        return location.upper()
    elif location.upper == 'JHB':
        return location.upper()
    else:
        print("Sorry that is an invalid location.")
        user_location()


def dates():
    """
    This is the date the user wants to book a new slot.
    """

    # The months with 31 days to see if the date is valid
    days_31 = ('01', '03', '05', '07', '08', '10', '12')
    # The months with 30 days to see if the date is valid
    days_30 = ('04', '06', '09', '11')
    # Seperates feburaruy cause it has 28 days
    exception_days = ('02')

    date_str = "-"
    
    date = input("What date would you like?" 
    " [(e.g 2020-06-30 ) You can only plan 30 days in advance.]: " )

    date = date.split('-')

    if len(date) == 3:
        if date[1].upper() in days_31:
            if int(date[2]) <= 31 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the chosen month.")
                dates()
        elif date[1].upper() in days_30:
            if int(date[2]) <= 30 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the chosen month.")
                dates()
        elif date[1].upper() in exception_days:
            if int(date[2]) <= 28 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day in the chosen month.")
                dates()
        else:
            print("Please choose an actual month.")
            dates()
    else: 
        print("Please formulate the date properly")
        dates()


def user_description():
    """
    This gives a descirption of the type of help the user is willing to give.
    """
    description = input("Give a description of the help you need. ")
    return description


def cancel_bookings(command, command_list):
    """
    As either a patient or a volenteer you can cancel a slot you have booked or created.
    """

    deleting = input("You can only cancel an empty slot. Are you sure you wish to cancel a slot? (y/n) ")

    if deleting == 'y':
        print("You have confirmed you want to delete a slot.")
        list_not_booked = filter.filter_my_patient_slots()

        if not list_not_booked:
            print("You have no elegible slots to cancel.")
            print("This session has ended...")
            # This terminates the program the right way.
            return 

        cancel_dict = {}
        count = 1

        for event in list_not_booked:
            cancel_dict[count] = event['id']
            start = event['start'].get('dateTime', event['start'].get('date'))
            print(count, start, event['summary'])
            count = count + 1

        deleted_slot = input("Which slot do you want to delete: ")
        calendar_api.remove_attendee(cancel_dict[int(deleted_slot)])

        # print("Thank you for submitting, you have canceled your booking on: ")
        
        print("This session has ended...")
        return
    elif deleting =='n':
        print("You have chosen not to delete a slot.")
        print("This session has ended...")
        return
    else: 
        print("Sorry you must choose a valid input.")
        cancel_bookings(command,  command_list)



def check_bookings(command, command_list):
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """

    filter.list_of_users_clinic_events()
#     print("loading.. ")
#     print("You have these slots booked: ")
#     print("Here are your booked slots: ")
#     print("Here are your empty slots: ")

#     # user.validate(command, user_type,  command_list)
#     print("This session has ended...")
#     return False