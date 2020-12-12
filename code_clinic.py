import argparse
from interface import run_clinic
from configuration import create_configuration


def create_arguments():
    """
    Setup all the arguments that can be interpreted by the program
    and assigns the arguments entered by the user to the apropriate 
    argument variable
    Parameter: Nothing
    Return: Namespace of all possible arguments and their attributes
    """
    
    ap = argparse.ArgumentParser(add_help=False)

    # View your Calendar
    ap.add_argument('-p', '--personal', default = False, action = 'store_true')

    # book an event
    ap.add_argument('-b', '--book', default = False, action = 'store_true')

    # cancel an event
    ap.add_argument('-c', '--cancel', default = False, action = 'store_true')

    # delete an event
    ap.add_argument('-d', '--delete', default = False, action = 'store_true')

    # create an event
    ap.add_argument('-v', '--volunteer', default = False, action = 'store_true')

    # View Code Clinic Calendar
    ap.add_argument('-r', '--retrieve', default = False, action = 'store_true')

    # yyyy-mm-dd
    ap.add_argument('-date', nargs='?', dest= "date")

    # HH:MM
    ap.add_argument('-time', nargs='?', dest= "time")

    # Add what you can help with or what you need help with
    ap.add_argument('-e', '--description', nargs='?', dest= "description")

    # id of event
    ap.add_argument('-id', nargs='?', dest= "id")

    # amount of days to view calendar for
    ap.add_argument('-u', "--update", default = False, action = 'store_true')

    # number between 0 and 100
    ap.add_argument('-days', nargs='?', dest= "days")

    # Print help menu
    ap.add_argument('-h', '--help', default = False, action = 'store_true')

    # Print help volunteer menu
    ap.add_argument('-hv', default = False, action = 'store_true')

    # Print help book menu
    ap.add_argument('-hb', default = False, action = 'store_true')

    # Print help retrieve menu
    ap.add_argument('-hr', default = False, action = 'store_true')

    # Print help cancel menu
    ap.add_argument('-hc', default = False, action = 'store_true')

    # Print help delete menu
    ap.add_argument('-hd', default = False, action = 'store_true')
 
    # Personal calendar help
    ap.add_argument('-hp', default = False, action = 'store_true')

    # Change calendar days help
    ap.add_argument('-hu', default = False, action = 'store_true')

    args = ap.parse_args()

    return args


if __name__ == "__main__":
    
    create_configuration.setup_config()
    run_clinic.start(create_arguments())