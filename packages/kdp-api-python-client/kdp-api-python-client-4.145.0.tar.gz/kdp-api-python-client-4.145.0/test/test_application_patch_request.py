# coding: utf-8

"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces. Please note that the Python client library follows Python's naming convention of snake casing for fields, even though they may appear in camel case in the API specification. <p><b>By default this api documentation targets the koverse production server at 'api.app.koverse.com' You can provide the hostname of your koverse instance to this documentation page via the 'host' query param.</p> <p><b>For example providing host - https://koverse-docs.saic.com/api?host=api.myHost.com, will update requests to target the provided host.</b></p> <p><b>Authentication request example with provided host - https://api.myHost.com/authentication</b></p>

    The version of the OpenAPI document: 4.145.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from kdp_api.models.application_patch_request import ApplicationPatchRequest

class TestApplicationPatchRequest(unittest.TestCase):
    """ApplicationPatchRequest unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> ApplicationPatchRequest:
        """Test ApplicationPatchRequest
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `ApplicationPatchRequest`
        """
        model = ApplicationPatchRequest()
        if include_optional:
            return ApplicationPatchRequest(
                name = '',
                url = '',
                redirect_url = '',
                workspace_id = '',
                client_id = '',
                client_secret = '',
                visible = True,
                description = '',
                type = 'mls',
                allowed_users = [
                    ''
                    ],
                required_dataset_access = [
                    kdp_api.models.application_create_request_required_dataset_access_inner.application_create_request_requiredDatasetAccess_inner(
                        action = 'read', 
                        dataset_id = '', )
                    ],
                reset_secret = True
            )
        else:
            return ApplicationPatchRequest(
        )
        """

    def testApplicationPatchRequest(self):
        """Test ApplicationPatchRequest"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
