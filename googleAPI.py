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
        pass



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
        payload = {'summary' : self.__name}
        try:
            payload['location'] = self.location


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
        self.__location = newNotifcations


class InvalidDateException(Exception):
    def __str__(self):
        return "Invalid Date"

class MissingInformationException(Exception):
    def __str__(self):
        return "This event does not have the informaiton you are looking for."
