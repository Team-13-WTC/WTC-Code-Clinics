import unittest
from io import StringIO
import io
import sys
from interface import run_clinic
from argparse import Namespace

class TestRunClinic(unittest.TestCase):
    sys.stdout = io.StringIO()
    def test_step1_test_operation_call_book(self):
        self.assertEqual(1,run_clinic.only_one_operation(Namespace(book=True, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step1_test_operation_call_cancel(self):
        self.assertEqual(3,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=True, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))
    
    def test_step1_test_operation_call_delete(self):
        self.assertEqual(2,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=True, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step1_test_operation_call_retrieve(self):
        self.assertEqual(4,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=True, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))
        
    def test_step1_test_operation_call_volunteer(self):
        self.assertEqual(0,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=True, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step1_test_operation_call_help(self):
        self.assertEqual(5,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = True, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step1_test_operation_call_personal(self):
        self.assertEqual(11,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=True, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step1_test_operation_call_update(self):
        self.assertEqual(12,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = True, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))

    def test_step2_test_no_operation(self):
        self.assertEqual(None,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))
       
    def test_step2_test_too_many_operation(self):
        self.assertEqual(None,run_clinic.only_one_operation(Namespace(book=False, 
        cancel=False, date=None, delete=False, description=None, id=None, personal=False, retrieve=False, time=None, volunteer=False, help = False, update = False, days = False, hv= False, hb= False, hr= False, hc= False, hd= False, hp= False, hu= False)))
