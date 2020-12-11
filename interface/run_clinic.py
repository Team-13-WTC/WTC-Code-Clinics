# USER_PATHS = os.path.abspath(os.path.join(os.path.dirname( __file__ ), "../"))
# sys.path.insert(0, USER_PATHS + "/")
from interface import operations
from interface import validations


def split_operation(operation, args):
    """
    Based on operation selected by user, calls apropriate validations and operation with required parameters
    Parameter:  operation (int), args (full list of posible arguments)
    Returns:    Nothing
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

    elif operation == 5:
        operations.get_help()

    elif operation == 6:
        operations.get_more_help_volunteer()

    elif operation == 7:
        operations.get_more_help_book()
    
    elif operation == 8:
        operations.get_more_help_retrieve()
    
    elif operation == 9:
        operations.get_more_help_cancel()
    
    elif operation == 10:
        operations.get_more_help_delete()


def only_one_operation(args):
    """
    Verifies that user only specified to run one operation
    Parameter:  args (full list of posible arguments)
    Returns:    int (index position of True operation if only one selected) or Nothing
    """

    operations = [args.volunteer, args.book, args.delete, args.cancel, args.retrieve, args.help, args.hv, args.hb, args.hr, args.hc, args.hd]

    if operations.count(True) > 1:
        print('Only one operation at a time')

    elif operations.count(True) == 0:
        print('Valid operations are --volunteer --book --delete --cancel --retrieve --update')

    else:
        return operations.index(True)


def start(args):
    
    split_operation(only_one_operation(args), args)