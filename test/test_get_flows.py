# coding: utf-8

"""
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
from src.client.legacy_flow_api import FlowApi

class TestCount(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.flow_client = FlowApi(ApiClient(self.configuration))

    def tearDown(self):
        pass

    def testGetFlows(self):
        """Test getFlows"""
        flows = self.flow_client.list_flows()
        pprint(flows)


if __name__ == '__main__':
    unittest.main()
