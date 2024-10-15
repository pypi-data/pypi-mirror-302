# coding: utf-8

"""
    Koverse Data Platform (KDP) API

    The KDP API is a REST API that can be used to create, access, and update data in KDP Workspaces. Please note that the Python client library follows Python's naming convention of snake casing for fields, even though they may appear in camel case in the API specification. <p><b>By default this api documentation targets the koverse production server at 'api.app.koverse.com' You can provide the hostname of your koverse instance to this documentation page via the 'host' query param.</p> <p><b>For example providing host - https://koverse-docs.saic.com/api?host=api.myHost.com, will update requests to target the provided host.</b></p> <p><b>Authentication request example with provided host - https://api.myHost.com/authentication</b></p>

    The version of the OpenAPI document: 4.145.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing import Optional, Set
from typing_extensions import Self

class KeycloakProviderConfiguration(BaseModel):
    """
    KeycloakProviderConfiguration
    """ # noqa: E501
    key: StrictStr = Field(description="Key for keycloak configuration")
    secret: StrictStr = Field(description="Secret for keycloak configuration")
    authorize_url: Optional[StrictStr] = Field(default=None, description="Url for keycloak authentication", alias="authorizeUrl")
    access_url: Optional[StrictStr] = Field(default=None, description="Url for keycloak token", alias="accessUrl")
    profile_url: Optional[Any] = Field(default=None, description="Url for keycloak user information", alias="profileUrl")
    scope: Optional[List[StrictStr]] = Field(default=None, description="Scope of the SSO configuration")
    nonce: Optional[StrictBool] = Field(default=None, description="When enabled provides a random value generated by your app that enables replay protection.")
    state: Optional[StrictStr] = Field(default=None, description="Keycloak configuration state")
    oauth: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="OAuth version")
    __properties: ClassVar[List[str]] = ["key", "secret", "authorizeUrl", "accessUrl", "profileUrl", "scope", "nonce", "state", "oauth"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of KeycloakProviderConfiguration from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # set to None if profile_url (nullable) is None
        # and model_fields_set contains the field
        if self.profile_url is None and "profile_url" in self.model_fields_set:
            _dict['profileUrl'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of KeycloakProviderConfiguration from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "key": obj.get("key"),
            "secret": obj.get("secret"),
            "authorizeUrl": obj.get("authorizeUrl"),
            "accessUrl": obj.get("accessUrl"),
            "profileUrl": obj.get("profileUrl"),
            "scope": obj.get("scope"),
            "nonce": obj.get("nonce"),
            "state": obj.get("state"),
            "oauth": obj.get("oauth")
        })
        return _obj


