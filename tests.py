import unittest

from simulation import time

class TimeStampTests(unittest.TestCase):

    def test_day(self):
        t = time.Timestamp(1440)
        self.assertEqual(t.day(), 1)

    def test_hourOfDay(self):
        t = time.Timestamp(36 * time.HOUR)
        self.assertEqual(t.hourOfDay(), 12)

    def test_dayOfWeek(self):
        t = time.Timestamp(4 * time.DAY + 23 * time.HOUR)
        self.assertEqual(t.dayOfWeek(), 4)

    def test_today(self):
        t = time.Timestamp(65 * time.HOUR)
        self.assertEqual(t.today(), 2 * time.DAY)

if __name__ == "__main__":
    unittest.main()