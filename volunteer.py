import user
import filter
import calendar_api


def volunteer(user_name, command, user_type, command_list):
    """
    This directs a user to the function they want to use.
    """
    # as user_input is never returned it can be used as a variable again and again
    if command == 0:
        user.validate(user_name, command, user_type, command_list)
    if command == "create":
        create_slot(user_name, command, user_type, command_list)
    elif command == "check":
        check_bookings(user_name, command, user_type, command_list)
    elif command == "cancel":
        cancel_bookings(user_name, command, user_type, command_list)
    elif command == "book":
        print("Sorry you cant do that as a volunteer.")
        user.validate(user_name, command, user_type, command_list)


def create_slot(user_name, command, user_type,  command_list):
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """
    proceed = input("Would you like to create a new slot? (y/n) ")
    
    if proceed == 'y':
        print("The event will be called 'CODE CLINIC VOLUNTEERING'.")
        
        # These functions are to keep this current function from looking to messy. They hold the data needed to collect.
        date = dates()
        open_slot = filter.filter_available_creation('2020-11-11', user_name)
        for key in open_slot:
            print(f'{key}: {open_slot[key]}')

        
        time = int(input("Choose a time slot. ")) #timing() 
        title = input("Title ?: ")
        location = user_location()
        description = user_description()


        print("Thank you for creating a slot. Here are the details")
        print("Date: " + date)
        print("Title: CODE CLINIC VOLUNTEERING")
        print("Volunteer:" + user_name)
        if location == 'CPT':
            print("Location: Cape Town main campus.")
        else:
            print("Location: Johanesburg campus 3.")
        print("Time: " + open_slot[time])
        print("Description: " + description + ".")
        calendar_api.create_event(title, location, description, date, open_slot[time], user_name)
        user.validate(user_name, command, user_type,  command_list)
    elif proceed == 'n':
        user.validate(user_name, command, user_type,  command_list)
    else:
        print("Sorry that is invalid.")
        create_slot(user_name, command, user_type,  command_list)


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
    This is the date the volunteer wahts to create a new slot.
    """
    # This needs to formualted properly and completed with a 30 day in advnace implmented.

    # days_31 = ('JAN', 'MAR', 'MAY', 'JUL', 'AUG', 'OCT', 'DEC')
    # days_30 = ('APR', 'JUN', 'SEP', 'NOV')
    # exception_days = ('FEB')


    # The months with 31 days to see if the date is valid
    days_31 = ('01', '03', '05', '07', '08', '10', '12')
    # The months with 30 days to see if the date is valid
    days_30 = ('04', '06', '09', '11')
    # Seperates feburaruy cause it has 28 days
    exception_days = ('02')

    date_str = "-"
    
    date = input("What day are you wanting to create a slot?" 
    " [(e.g 2020-06-30 ) You can only plan 30 days in advance.]: " )

    #return date
    date = date.split('-')

    if len(date) == 3:
        if date[1].upper() in days_31:
            if int(date[2]) <= 31 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the chosen month.")
        if date[1].upper() in days_30:
            if int(date[2]) <= 30 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day within the chosen month.")
        if date[1].upper() in exception_days:
            if int(date[2]) <= 28 and int(date[2]) > 0:
                date_str = date_str.join(date)
                return date_str.upper()
            else:
                print("Please choose a valid day in the chosen month.")
        else:
            print("Please choose an actual month.")
    else: 
        print("Please formulate the date properly")
        dates()


def timing():
    """
    This will get the time the volunteer wants to create a slot for.
    """

    time = input("What time do you want to create you slot? (24H time) ")

    time_hour = ""
    time_min = ""
    time_str = " "
    semi_colons = ':'

    time = time.split(':')

    if (60 > int(time[1]) >= 0) and (24 > int(time[0]) >= 0):
        time_hour = time[0]
        time_min = time[1] 
        time_str = time_hour + semi_colons + time_min
        return time_str 
    else:
        print("Please choose a valid time.")
        timing()  


def user_description():
    """
    This gives a descirption of the type of help the volunteer is willing to give.
    """
    description = input("Give a description of the help you are willing to give. ")
    return description


def cancel_bookings(user_name, command, user_type,  command_list):
    """
    As either a patient or a volenteer you can cancel a slot you have booked or created.
    """
    
    deleting = input("You can only cancel an empty slot. Are you sure you wish to cancel a slot? (y/n) ")

    if deleting == 'y':
        deleted = input("You have confirmed you want to deleted a slot, what day slot do you want to delete? (if you decide not to delete a slot type 'back') e.g 12:12 2 Dec ")
        print("Thank you for submitting, you have canceled you booking on: " + deleted)
        user.validate(user_name, command, user_type,  command_list)
    elif deleting =='n':
        print("You have chosen not to delete a slot.")
        user.validate(user_name, command, user_type,  command_list)
    else: 
        print("Sorry you must choose a valid input.")
        cancel_bookings(user_name, command, user_type,  command_list)


def check_bookings(user_name, command, user_type,  command_list):
    """
    As patient you can check what slots you have signed up for, as a volenteer you can check what slots you have created.
    """
    print("loading.. ")
    print("You have these slots booked: ")
    print("Here are your booked slots: ")
    print("Here are your empty slots: ")
    user.validate(user_name, command, user_type,  command_list)

