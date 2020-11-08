from cal_setup import get_calendar_service

def main():
    # Delete the event
    service = get_calendar_service()

    # event_to_cancel = 'command from user specifying which slot - the function that handles this must have access to data.json'

    try:
        service.events().delete(
            calendarId='primary',
            #event id comes from eid=9e8m...-
            eventId='event_to_cancel',
        ).execute()
    except googleapiclient.errors.HttpError:
        print("Failed to delete event")

    print("Event deleted")

if __name__ == '__main__':
    main()

# def cancel_event():
#     1: must only display events shared by volunteer and code clinic
#     2: can do this by using api to list those events and store list of event_ids filtering by eid=...-
#     3. must return event to cancel id to use here
