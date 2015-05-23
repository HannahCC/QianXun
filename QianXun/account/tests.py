# -*- coding: UTF-8 -*-
from django.test import TestCase

from account.models import Customer
from QianXun.account.db import customer





# Create your tests here.
class TestCustomer(TestCase):
    def create_customer(self):
        cus = Customer(user_name='13378569875', user_type=1,
                       nick_name='9n久', password='123abc',
                       client_id='adre-fdsf-fewf-543-fds', version='1.0.1')
        new_cus = customer.save_customer(cus)
        self.assertEqual(1, new_cus.id, 'id is not 1')

    def update_customer(self):
        cus = Customer(id='1', user_name='13378569875', user_type=2,
                       nick_name='9n久', password='123abc',
                       client_id='adre-fdsf-fewf-543-fds', version='1.0.1')
        new_cus = customer.update(cus)
        self.assertEqual(1, new_cus.id, 'id is not 1')