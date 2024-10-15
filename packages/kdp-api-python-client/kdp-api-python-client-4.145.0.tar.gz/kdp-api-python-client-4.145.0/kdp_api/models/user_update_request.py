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

from pydantic import BaseModel, ConfigDict, Field, SecretStr, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class UserUpdateRequest(BaseModel):
    """
    UserUpdateRequest
    """ # noqa: E501
    id: Optional[StrictStr] = Field(default=None, description="provide current or updated ID of the user")
    email: StrictStr = Field(description="provide current or updated email of the user")
    first_name: StrictStr = Field(description="the current or updated first name of the user", alias="firstName")
    last_name: StrictStr = Field(description="the current or updated last name of the user", alias="lastName")
    password: SecretStr = Field(description="the current or updated authentication password of the user")
    workspace_id: Optional[StrictStr] = Field(default=None, description="the current or updated workspaceId the user can access", alias="workspaceId")
    role: Optional[StrictStr] = Field(default=None, description="the current or updated workspace role for the user")
    __properties: ClassVar[List[str]] = ["id", "email", "firstName", "lastName", "password", "workspaceId", "role"]

    @field_validator('role')
    def role_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['member', 'admin']):
            raise ValueError("must be one of enum values ('member', 'admin')")
        return value

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
        """Create an instance of UserUpdateRequest from a JSON string"""
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
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of UserUpdateRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "email": obj.get("email"),
            "firstName": obj.get("firstName"),
            "lastName": obj.get("lastName"),
            "password": obj.get("password"),
            "workspaceId": obj.get("workspaceId"),
            "role": obj.get("role")
        })
        return _obj


