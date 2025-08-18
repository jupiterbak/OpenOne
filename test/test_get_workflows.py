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
from src.client.workflows_api import WorkflowsApi

class TestGetWorkflows(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.workflows_client = WorkflowsApi(ApiClient(self.configuration))

    def tearDown(self):
        pass

    def testGetWorkflows(self):
        """Test getWorkflows"""
        workflows = self.workflows_client.get_workflows(limit=1000)
        pprint(workflows)

    def testRunWorkflow(self):
        """Test runWorkflow"""
        workflow = self.workflows_client.run_workflow(workflow_id="01HMD8CEGMCKRZEY0NMPB7R7QE", compiler_version="6.21.6", execution_engine="amp")
        pprint(workflow)


if __name__ == '__main__':
    unittest.main()
