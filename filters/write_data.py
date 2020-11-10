from list_events import list_events
import json
from pprint import pprint

def main():

    events = list_events()

    #Write calendar events for next 7 days to json file
    # print(json.dumps(events, indent=4, sort_keys=True))
    with open('data.json', 'a') as data:
        data.truncate(0)
        data.write(str(events))
        # pprint(str(events))


if __name__ == '__main__':
   main()
