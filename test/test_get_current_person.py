# coding: utf-8

"""
    Scheduling (Alpha)

    No description provided (generated API client)  # noqa: E501

    OpenAPI spec version: v2024.14.0
    
    Generated API client
"""

from __future__ import absolute_import

import sys
import os
import unittest
from pprint import pprint

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client.configuration import Configuration
from src.client.api.api_client import ApiClient
from src.client.legacy_person_api import PersonApi

class TestCount(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.person_client = PersonApi(ApiClient(self.configuration))

    def tearDown(self):
        pass

    def testgetCurrentUser(self):
        """Test getCurrentUser"""
        person = self.person_client.get_current_person()
        pprint(person)


if __name__ == '__main__':
    unittest.main()
