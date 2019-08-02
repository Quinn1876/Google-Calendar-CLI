import unittest
import googleAPI
from googleAPI import Event
import datetime

class TestEventMethods(unittest.TestCase):
    def setUp(self):
        startDate = datetime.datetime(year=2019, month=5, day=10, hour=16, minute=30)
        endDate = datetime.datetime(year=2019, month=5, day=10, hour=18, minute=30)
        self.event = Event("TestEvent", startDate, endDate)

    def test_Event_default_callable(self):
        testPayload = self.event()
        self.assertEqual(testPayload['summary'], "TestEvent", "incorrect name")
        self.assertEqual(testPayload['start']['dateTime'], "2019-05-10T16:30:00-04:00")
        self.assertEqual(testPayload['end']['dateTime'], "2019-05-10T18:30:00-04:00")

    def test_Event_location_callable(self):
        self.event.location = "Toronto"
        p = self.event()
        self.assertEqual(p['location'], "Toronto")

    def test_Event_description_callable(self):
        self.event.description = "test desc"
        p = self.event()
        self.assertEqual(p['description'], "test desc")

    def test_Event_notification_callable(self):
        self.event.addNotification('email', minutes=10)
        p = self.event()
        self.assertEqual(p['reminders']['overrides'][0]['method'], "email")
        self.assertEqual(p['reminders']['overrides'][0]['minutes'], 10)

    def test_Event_changeDate(self):
        self.event.startDate = datetime.datetime.now()
        self.event.endDate = datetime.datetime.now()
        self.assertIsInstance(self.event.startDate, datetime.datetime)
        self.assertIsInstance(self.event.endDate, datetime.datetime)

if __name__ == "__main__":
    unittest.main()
