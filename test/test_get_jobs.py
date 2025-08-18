# coding: utf-8

"""
   
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
from src.client.legacy_job_group_api import JobGroupApi

class TestGetJobs(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.jobs_client = JobGroupApi(ApiClient(self.configuration))
    def tearDown(self):
        pass

    def testGetJobGroup(self):
        """Test getJobGroup"""
        job_group = self.jobs_client.get_job_group(id="151042")
        pprint.pprint(job_group)


if __name__ == '__main__':
    unittest.main()
