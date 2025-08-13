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

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client.configuration import Configuration
from src.client.api.api_client import ApiClient
from src.client.plan_api import PlanApi

class TestCount(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.plan_client = PlanApi(ApiClient(self.configuration))

    def tearDown(self):
        pass

    def testCount(self):
        """Test Count"""
        count = self.plan_client.count_plans()
        print(count)


if __name__ == '__main__':
    unittest.main()
