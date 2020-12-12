import argparse
from argparse import ArgumentParser
from interface import run_clinic
import os.path as path
from configuration import create_configuration


def create_arguments():

    
    ap = argparse.ArgumentParser(add_help=False)

    ap.add_argument('-p', '--personal', default = False, action = 'store_true', help = "Allows user to work on their personal calendar instead of the Code Clinic calendar")

    ap.add_argument('-b', '--book', default = False, action = 'store_true', help = "book an event")

    ap.add_argument('-c', '--cancel', default = False, action = 'store_true', help = "cancel an event")

    ap.add_argument('-d', '--delete', default = False, action = 'store_true', help = "delete an event")

    ap.add_argument('-v', '--volunteer', default = False, action = 'store_true', help = "create an event")

    ap.add_argument('-r', '--retrieve', default = False, action = 'store_true', help = "See your calendar")

    ap.add_argument('-date', nargs='?', dest= "date", help = 'yyyy-mm-dd')

    ap.add_argument('-time', nargs='?', dest= "time", help = 'HH:MM')

    ap.add_argument('-e', '--description', nargs='?', dest= "description", help = 'Add some info')

    ap.add_argument('-id', nargs='?', dest= "id", help = 'id of event')

    ap.add_argument('-u', "--update", default = False, action = 'store_true', help = "give it number")

    ap.add_argument('-days', nargs='?', dest= "days", help = 'HH:MM')

    ap.add_argument('-h', '--help', default = False, action = 'store_true', help = "Print help menu")

    ap.add_argument('-hv', default = False, action = 'store_true', help = "Print help volunteer menu")

    ap.add_argument('-hb', default = False, action = 'store_true', help = "Print help book menu")

    ap.add_argument('-hr', default = False, action = 'store_true', help = "Print help retrieve menu")

    ap.add_argument('-hc', default = False, action = 'store_true', help = "Print help cancel menu")

    ap.add_argument('-hd', default = False, action = 'store_true', help = "Print help delete menu")

    ap.add_argument('-hp', default = False, action = 'store_true', help = "Personal calendar help")

    ap.add_argument('-hu', default = False, action = 'store_true', help = "Change calendar days help")


    args = ap.parse_args()

    return args


if __name__ == "__main__":
    
    create_configuration.setup_config()
    run_clinic.start(create_arguments())
    
#sphe clean up create_config
# change print('Valid operations are --volunteer --book --delete --cancel --retrieve') to help function call