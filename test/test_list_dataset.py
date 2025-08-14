# coding: utf-8
from __future__ import absolute_import

import sys
import os
import unittest
from pprint import pprint

# Add project root to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.client.configuration import Configuration
from src.client.api.api_client import ApiClient
from src.client.legacy_imported_dataset_api import ImportedDatasetApi

class TestCount(unittest.TestCase):
    """Count unit test stubs"""

    def setUp(self):
        self.configuration = Configuration()
        self.imported_dataset_client = ImportedDatasetApi(ApiClient(self.configuration))

    def tearDown(self):
        pass

    def testListDatasets(self):
        """Test list datasets"""
        datasets = self.imported_dataset_client.list_dataset_library(datasets_filter="all", ownership_filter="all", schematized=False, limit=100)
        pprint(datasets)


if __name__ == '__main__':
    unittest.main()
