# USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
# sys.path.insert(0, USER_PATHS + "/")

# Imports needed for interface to work
from interface import operations
from interface import validations


def split_operation(operation, args):
    """
    Checks if the command is valid.
    args.volunteer, args.book, args.delete, args.cancel, args.retrieve
    """

    if operation == 0:
        if validations.date_is_valid(args.date) and validations.time_is_valid(args.time) and validations.description_created(args.description):
            operations.create_slot(args.date, args.time, args.description)

    elif operation == 1:
        if not args.id:
            operations.book_slot(args.id, args.description)

        elif validations.description_created(args.description):
            operations.book_slot(args.id, args.description)

    elif operation == 2:
        operations.delete_slot(args.id)

    elif operation == 3:
        operations.cancel_booking(args.id)
        
    elif operation == 4:
        operations.retrieve_calendar()


def only_one_operation(args):

    operations = [args.volunteer, args.book, args.delete, args.cancel, args.retrieve]

    if operations.count(True) > 1:
        print('Only one operation at a time')

    elif operations.count(True) == 0:
        print('Valid operations are --volunteer --book --delete --cancel --retrieve')

    else:
        return operations.index(True)


def start(args):
    
    split_operation(only_one_operation(args), args)