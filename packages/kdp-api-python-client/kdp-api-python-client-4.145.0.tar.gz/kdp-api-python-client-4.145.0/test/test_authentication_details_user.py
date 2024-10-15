# coding: utf-8

"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces. Please note that the Python client library follows Python's naming convention of snake casing for fields, even though they may appear in camel case in the API specification. <p><b>By default this api documentation targets the koverse production server at 'api.app.koverse.com' You can provide the hostname of your koverse instance to this documentation page via the 'host' query param.</p> <p><b>For example providing host - https://koverse-docs.saic.com/api?host=api.myHost.com, will update requests to target the provided host.</b></p> <p><b>Authentication request example with provided host - https://api.myHost.com/authentication</b></p>

    The version of the OpenAPI document: 4.145.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import unittest

from kdp_api.models.authentication_details_user import AuthenticationDetailsUser

class TestAuthenticationDetailsUser(unittest.TestCase):
    """AuthenticationDetailsUser unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional) -> AuthenticationDetailsUser:
        """Test AuthenticationDetailsUser
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # uncomment below to create an instance of `AuthenticationDetailsUser`
        """
        model = AuthenticationDetailsUser()
        if include_optional:
            return AuthenticationDetailsUser(
                avatar = '',
                change_email_token_expiration = '',
                created_at = '',
                deleted_at = '',
                display_name = '',
                email = '',
                first_name = '',
                github_id = '',
                google_id = '',
                id = '',
                last_name = '',
                linked_accounts = [
                    ''
                    ],
                microsoft_id = '',
                okta_id = '',
                stripe_customer_id = '',
                updated_at = '',
                verified = True,
                workspace_count = 1.337
            )
        else:
            return AuthenticationDetailsUser(
        )
        """

    def testAuthenticationDetailsUser(self):
        """Test AuthenticationDetailsUser"""
        # inst_req_only = self.make_instance(include_optional=False)
        # inst_req_and_optional = self.make_instance(include_optional=True)

if __name__ == '__main__':
    unittest.main()
