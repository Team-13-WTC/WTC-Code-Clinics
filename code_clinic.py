from argparse import ArgumentParser
from interface import run_clinic


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

    ap.add_argument('-description', nargs='?', dest= "description", help = 'Add some info')

    ap.add_argument('-id', nargs='?', dest= "id", help = 'id of event')

    args = ap.parse_args()

    return args


if __name__ == "__main__":
    
    run_clinic.start(create_arguments())
    