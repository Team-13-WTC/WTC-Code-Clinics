from argparse import ArgumentParser
from interface import run_clinic
import os.path as path
from configuration import create_configuration

# # print(full_config)
# if not path.exists(create_configuration.full_config):
#     create_configuration.setup_config()


def create_arguments():

    
    ap = ArgumentParser()

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

    ap.add_argument('-days', nargs='?', dest= "days", help = 'give it a number of days.')

    args = ap.parse_args()

    return args


if __name__ == "__main__":
    
    run_clinic.start(create_arguments())
    
#add extended help
#add argument for create config
#sphe clean up create_config
#melt delete service function and change to sphe's
#add pretty print
#Hiranya TDD Validations.py / run_clinic.py
# change print('Valid operations are --volunteer --book --delete --cancel --retrieve') to help function call