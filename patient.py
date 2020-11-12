from filter import filter_available_booking
import user
import filter
import calendar_api


def patient(user_name, command, user_type, command_list):
    """
    This allows for the function to be used depending on the command.
    """
    if command == 0:
        user.validate(user_name, command, user_type,  command_list)
    if command == "book":
        create_booking(user_name, command, user_type,  command_list)
    elif command == "check":
        check_bookings(user_name, command, user_type,  command_list)
    elif command == "cancel":
        cancel_bookings(user_name, command, user_type,  command_list)
    elif command == "create":
        print("Sorry you can't do that as a patient.")
        user.validate(user_name, command, user_type,  command_list)


def create_booking(user_name, command, user_type, command_list):
    """
    This function allows the patient to book a slot
    """
    proceed = input("Would you like to book a new slot? (y/n) ")
    if proceed == 'y':
        open_slots = filter.filter_available_booking(user_name)
        dictionary_of_available_slots = {}
        count = 1
        for event in open_slots:
            start = event['start'].get('dateTime', event['start'].get('date'))
            start = str(start)
            dictionary_of_available_slots[count] = event['id']
            print(f"{count}. {start.replace('T', ' ').replace(':00+02:00', '')}, {event['summary']}")
            count += 1
        slot_selection = int(input('Choose a slot: '))
        description = user_description()                            #stores the user description
        calendar_api.add_attendee(dictionary_of_available_slots[slot_selection], user_name, description)
        # print("The event will be called 'CODE CLINIC PATIENT'.")
        # location = user_location(user_name, command)                #stores user location
        # date = dates()                                              #stores the date the user has chosed
        # time = timing()                                             #stores the time the user has set
        print("Thank you for booking a slot. Here are the details")

        # print("Title: CODE CLINIC PATIENT")
        # print("Patient: " + user_name)
        # if location == 'CPT':
        #     print("Location: Cape Town main campus.")
        # else:
        #     print("Location: Johanesburg campus 3 is not allowed.")
        # print("Date: " + date)
        # print("Time: " + time)
        # print("Description: " + description + ".")
        user.validate(user_name, command, user_type,  command_list)
    elif proceed == 'n':
        user.validate(user_name, command, user_type,  command_list)
    else:
        print("Sorry that is invalid.")
        create_booking(user_name, command, user_type,  command_list)


def user_location(user_name, command):
    """
    This function checks whether the user is from cpt or jhb.
    if user = jhb the program exits 
    """
    location = input("Are you from JHB or CPT? ")

    if location.upper() == 'CPT':
        return location.upper()
    elif location.upper == 'JHB':
        print("The session will end now. Bye.")
        exit()
    else:
        print("That is an invalid location. Please try again.")
        user_location()


def dates():
    """
    This function creates the date for when the user wants to book a slot
    """
    days_31 = ('JAN', 'MAR', 'MAY', 'JUL', 'AUG', 'OCT', 'DEC') #months which have 31 days
    days_30 = ('APR', 'JUN', 'SEP', 'NOV')                      #months with 30 days 
    exception_days = ('FEB')                                    #month with 28 days
    date_str = " "                                               
    date = input("What day do you want to book a slot?" 
    " [(e.g 27 DEC) You can only plan 30 days in advance.]: " )

    date = date.split(' ')

    if len(date) == 2:
        if date[1].upper() in days_31:
            if int(date[0]) <= 31 and int(date[0]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the given month.")
        if date[1].upper() in days_30:
            if int(date[0]) <= 30 and int(date[0]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the given month.")
        if date[1].upper() in exception_days:
            if int(date[0]) <= 28 and int(date[0]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day in the given month.")
        else:
            print("Please choose a valid month.")
    else: 
        print("Please formulate the date properly.")
        dates()


def timing():
    """
    This function sets a time for when the user wants to book a slot.
    """
    time = input("""These are the times available to book a slot on this day:"
    09:30 
    12:00 
    16:00 
    What time do you want to book a slot? (24H time): """)

    time_hour = ''
    time_min = ""
    time_str = " "
    semi_colons = ':'

    time = time.split(':')

    if int(time[1]) >= 0 and (24 >= int(time[0]) > 0):
        time_hour = time[0]
        time_min = time[1] 
        time_str = time_hour + semi_colons + time_min
        return time_str
    else:
        print("Please choose a valid time.")
        timing()  


def user_description():
    """
    This function asks the user what help they need to receive.
    """
    description = input("Please give a description of the help you need: ")
    return description


def cancel_bookings(user_name, command, user_type,  command_list):
    """
    Enables the patient to cancel a booking they've created.
    """
    ask_user = input("Are you sure you want to cancel the booking? (y/n): ")
    if ask_user == "y":
        print("Your booking has been canceled.")
    else:
        ask_user == "n"
        print("You have been redirected.")
    user.validate(user_name, command, user_type, command_list)


def check_bookings(user_name, command, user_type,  command_list):
    """
    A patient can check which slots they've booked
    """
    print("checking the bookings you have made..")
    print("loading..  ")
    print("This is a list of bookings you've made so far:")
    print("You dont have any bookings saved yet. This is just a trial.")
    user.validate(user_name, command, user_type,  command_list)

