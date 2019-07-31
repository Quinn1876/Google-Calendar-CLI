import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

class CalendarAPI:
    SCOPES = [
        'https://www.googleapis.com/auth/calendar.readonly',
        'https://www.googleapis.com/auth/calendar.events',
        'https://www.googleapis.com/auth/calendar',
        'https://www.googleapis.com/auth/calendar.settings.readonly',
        'https://www.googleapis.com/auth/calendar.events.readonly'
    ]
    def __init__(self):
        creds = None
        # The file token.pickle stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('calendar', 'v3', credentials=creds)

    def getEvents(self, numberOfEvents, date):
        pass

    def addEvent(self, event):
        if type(event) != Event:
            raise TypeError("event must be of type Event.")
        self.service.events().insert(calendarId=event.owner, body=event())
        print ('Event created: {}'.format(event.get('htmlLink')))




class Event:
    # name
    # Date start - datetime
    # Date End - datetime
    # repetition
    # Location
    # Description of Event
    # What Calendar it belongs to
    # Notification options
    def __init__(self, Name, StartDate, EndDate, Repetition=None, Location=None, Description=None, Owner='primary', Notifications=None):
        self.__name = Name
        self.__startDate = StartDate
        self.__endDate = EndDate
        self.__owner = Owner
        if Repetition:
            self.__repetition = Repetition
        if Location:
            self.__location = Location
        if Description:
            self.__description = Description
        if Notifications:
            self.__notifications = Notifications

    def __call__(self):
        payload = {
            'summary' : self.__name,
            'start' : {
                'dateTime' : "{}-{}-{}T{}:{}:{}-04:00".format(self.__startDate.year, self.__startDate.month, self.__startDate.day, self.__startDate.hour, self.__startDate.minute, self.__startDate.second),
                'timeZone' : 'America/Toronto'
            },
            'end' : {
                'dateTime' : "{}-{}-{}T{}:{}:{}-04:00".format(self.__endDate.year, self.__endDate.month, self.__endDate.day, self.__endDate.hour, self.__endDate.minute, self.__endDate.second),
                'timeZone' : 'America/Toronto'
            }
        }
        try:
            payload['location'] = self.__location
        except:
            pass

        try:
            payload['description'] = self.__description
        except:
            pass

        try:
            payload['reminders'] = {
                'useDefault' : False,
                'overrides': self.__notifications
            }
        except:
            payload['reminders'] = {
                'useDefault' : False,
                'overrides': [
                    {'method' : "email", 'minutes' : 24 * 60},
                    {'method' : 'popup', 'minutes' : 10}
                ]
            }
        return payload

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, newName):
        self.__name = newName

    @property
    def startDate(self):
        return self.__startDate

    @startDate.setter
    def startDate(self, newDate):
        if type(newDate) != datetime.datetime:
            raise InvalidDateException
        self.__startDate = newDate

    @property
    def endDate(self):
        return self.__endDate

    @endDate.setter
    def endDate(self, newDate):
        if type(newDate) != datetime.datetime:
            raise InvalidDateException
        self.__endDate = newDate

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, newOwner):
        self.__owner = newOwner

    @property
    def repetition(self):
        if hasattr(self, "__repetion"):
            return self.__repetition
        else:
            raise MissingInformationException

    @repetition.setter
    def repetition(self, newRepetition):
        self.__repetition = newRepetition

    @property
    def location(self):
        if hasattr(self, "__location"):
            return self.__location
        else:
            raise MissingInformationException

    @location.setter
    def location(self, newLocation):
        self.__location = newLocation


    @property
    def description(self):
        if hasattr(self, "__description"):
            return self.__description
        else:
            raise MissingInformationException

    @description.setter
    def description(self, newDescription):
        self.__description = newDescription

    @property
    def notifications(self):
        if hasattr(self, "__notifications"):
            return self.__notifications
        else:
            raise MissingInformationException

    @notifications.setter
    def notifications(self, newNotifcations):
        raise SettingNotificationException

    def addNotification(self, method, minutes=NONE, hours=NONE, days=None):
        if minutes is None and hours is None and days is None:
            raise AttributeError("You must include a time")
        if hasattr(self, "__notificaitons"):
            self.__notifications = []

        self.__notifications.append({'method' : method, 'minutes' : (((days * 24) + hours) * 60) + minutes})

    def deleteNotification(self, index=None):
        if index is None or not index in range(len(self.__notificaitons)):
            print("Which notification would you like to remove? ")
            for i in range(len(self.__notifications)):
                print(i + " : " + self.__notifications[i])
            self.deleteNotification(input())
        else:
            print(self.__notifications.pop(i) + " removed.")

class SettingNotificationException(Exception):
    def __str__(self):
        return "You cannot dirrectly change notificaitons, \nuse addNotification() or deleteNotification() \n to edit notifications"

class InvalidDateException(Exception):
    def __str__(self):
        return "Invalid Date"

class MissingInformationException(Exception):
    def __str__(self):
        return "This event does not have the informaiton you are looking for."
