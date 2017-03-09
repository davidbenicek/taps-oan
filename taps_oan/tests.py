from django.test import TestCase

import unittest

class PageAccessTests(TestCase):

    def page_loads(self):

        request = 'placeholder'

        response = index(request)

        self.assertEqual(response.status_code, 200)