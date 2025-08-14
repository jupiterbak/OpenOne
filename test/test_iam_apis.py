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
import pprint

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client.configuration import Configuration
from src.client.api.api_client import ApiClient
from src.client.person_api import PersonApi
from src.client.workspace_api import WorkspaceApi

class TestIAMApis(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.iam_client = PersonApi(ApiClient(self.configuration))
        self.workspace_client = WorkspaceApi(ApiClient(self.configuration))
    def tearDown(self):
        pass

    def testWorkspace(self):
        """Test Count"""
        workspace = self.workspace_client.read_current_workspace()
        pprint.pprint(workspace)


if __name__ == '__main__':
    unittest.main()
