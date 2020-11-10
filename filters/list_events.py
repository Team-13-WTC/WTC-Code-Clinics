import datetime
from cal_setup import get_calendar_service
import json
from pprint import pprint


def list_events():


   service = get_calendar_service()
   # Call the Calendar API
   now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
   end = (datetime.datetime.now() + datetime.timedelta(days=6)).isoformat() + 'Z'
   print('Getting List of this weeks events')
   events_result = service.events().list(
       calendarId='primary', timeMin=now,timeMax = end,
       maxResults=100, singleEvents=True,
       orderBy='startTime').execute()
   events = events_result.get('items', [])

   return events
   

def print_events(events):

   for event in events:
       start = event['start'].get('dateTime', event['start'].get('date'))
       print(start, event['summary'])


#Prints out events or no events
#    if not events:
#        print('No upcoming events found.')
#    for event in events:
#        start = event['start'].get('dateTime', event['start'].get('date'))
#        print(start, event['summary'])

if __name__ == '__main__':
   events = list_events()
   print_events(events)
