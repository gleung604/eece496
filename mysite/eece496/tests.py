"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

class ViewTest(TestCase):
    def test_index(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 301)

    def test_home(self):
        resp = self.client.get('/home/')
        self.assertEqual(resp.status_code, 200)

    def test_eece496(self):
        resp = self.client.get('/eece496/')
        self.assertEqual(resp.status_code, 301)
