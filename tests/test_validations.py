import unittest
from io import StringIO
import io
import sys
from interface import validations
from datetime import timedelta
import datetime


class TestValidations(unittest.TestCase):
    sys.stdout = io.StringIO()
    
    def test_make_datetime_from_string(self):
        string = validations.make_datetime_from_string('2019-11-19')
        self.assertEqual(datetime.datetime(2019, 11, 19, 0, 0), string)
        
    def test_valid_date_format(self):
        self.assertTrue(validations.date_correct_format('2020-12-20'))
        self.assertTrue(validations.date_correct_format('1998-12-20'))

    def test_invalid_date_format(self):
        self.assertFalse(validations.date_correct_format('2020-12-200'))
        self.assertFalse(validations.date_correct_format('2020-12-s'))

    def test_valid_date_valid_day(self):
        self.assertTrue(validations.date_valid_day('2020-12-20'))
        self.assertTrue(validations.date_valid_day('2020-11-30'))
        self.assertTrue(validations.date_valid_day('2020-02-29'))

    def test_invalid_date_valid_day(self):
        self.assertFalse(validations.date_valid_day('2020-12-32'))
        self.assertFalse(validations.date_valid_day('2021-04-31'))
        self.assertFalse(validations.date_valid_day('2020-09-31'))
        self.assertFalse(validations.date_valid_day('2021-02-30'))

    def test_valid_date(self):
        self.assertTrue(validations.date_within_30_days('2020-12-20'))

    def test_invalid_date(self):
        self.assertFalse(validations.date_within_30_days('2021-01-20'))
        self.assertFalse(validations.date_within_30_days('2019-01-20'))

    def test_correct_time_pattern(self):
        self.assertTrue(validations.time_correct_format('08:15'))
        self.assertTrue(validations.time_correct_format('20:00'))

    def test_incorrect_time_pattern(self):
        self.assertFalse(validations.time_correct_format('08:150'))
        self.assertFalse(validations.time_correct_format('20d:00'))

    def test_valid_timeslot(self):
        self.assertTrue(validations.time_valid_slot('08:30'))
        self.assertTrue(validations.time_valid_slot('10:00'))

    def test_invalid_timeslot(self):
        self.assertFalse(validations.time_valid_slot('08:15'))
        self.assertFalse(validations.time_valid_slot('10:05'))

    def test_description_added(self):
        self.assertTrue(validations.description_created('abc'))
        self.assertFalse(validations.description_created(''))

    def test_valid_nbr_format(self):
        self.assertTrue(validations.valid_number_format('30'))
        self.assertFalse(validations.valid_number_format('-1'))
        self.assertFalse(validations.valid_number_format('100'))

    def test_days_created(self):
        self.assertTrue(validations.days_created('30'))
        self.assertFalse(validations.days_created(''))

