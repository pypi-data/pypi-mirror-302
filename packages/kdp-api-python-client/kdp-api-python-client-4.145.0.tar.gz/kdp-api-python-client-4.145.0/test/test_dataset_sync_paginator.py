# coding: utf-8

"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces. Please note that the Python client library follows Python's naming convention of snake casing for fields, even though they may appear in camel case in the API specification. <p><b>By default this api documentation targets the koverse production server at 'api.app.koverse.com' You can provide the hostname of your koverse instance to this documentation page via the 'host' query param.</p> <p><b>For example providing host - https://koverse-docs.saic.com/api?host=api.myHost.com, will update requests to target the provided host.</b></p> <p><b>Authentication request example with provided host - https://api.myHost.com/authentication</b></p>

    The version of the OpenAPI document: 4.145.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from kdp_api.models.dataset_sync_paginator import DatasetSyncPaginator

class TestDatasetSyncPaginator(unittest.TestCase):
    """DatasetSyncPaginator unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> DatasetSyncPaginator:
        """Test DatasetSyncPaginator
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `DatasetSyncPaginator`
        """
        model = DatasetSyncPaginator()
        if include_optional:
            return DatasetSyncPaginator(
                total = 1,
                limit = 10,
                skip = 1.337,
                data = [
                    kdp_api.models.dataset_sync.dataset sync(
                        id = '', 
                        dataset_id = '', 
                        status = 'pending', 
                        type = 'read', 
                        key = '', 
                        created_by_user_id = '', 
                        is_origin_workspace = True, 
                        host = 'myKoverseWorkspaceName.api.myKoverseHostName.com', 
                        workspace_id = 'myWorkspace', 
                        workspace_unique_id = '', 
                        sync_id = '', 
                        sync_host = 'myReplicaWorkspaceName.api.myReplicaKoverseHostName.com', 
                        sync_dataset_id = '', 
                        sync_workspace_id = null, 
                        sync_workspace_unique_id = '', 
                        last_sync_at = datetime.datetime.strptime('2013-10-20 19:20:30.00', '%Y-%m-%d %H:%M:%S.%f'), )
                    ]
            )
        else:
            return DatasetSyncPaginator(
        )
        """

    def testDatasetSyncPaginator(self):
        """Test DatasetSyncPaginator"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
