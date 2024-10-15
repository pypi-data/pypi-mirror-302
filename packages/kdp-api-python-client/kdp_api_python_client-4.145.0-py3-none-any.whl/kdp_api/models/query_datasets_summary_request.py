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

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing import Optional, Set
from typing_extensions import Self

class QueryDatasetsSummaryRequest(BaseModel):
    """
    QueryDatasetsSummaryRequest
    """ # noqa: E501
    expression: Optional[StrictStr] = Field(default=None, description="The term that you want to search for")
    search_id: Optional[StrictStr] = Field(default=None, description="A uuid used for paging through search results.", alias="searchId")
    limit: Optional[StrictInt] = Field(default=None, description="The maximum number of datasets to return for the query, providing -1 returns all datasets that contain matching records")
    offset: Optional[StrictInt] = Field(default=None, description="The number of datasets from the beginning where the current results will start, used for paging results")
    credentials_subset: Optional[List[StrictStr]] = Field(default=None, description="A list of credentials that can be provided to return records of a more limited subset than that of the authenticated caller", alias="credentialsSubset")
    __properties: ClassVar[List[str]] = ["expression", "searchId", "limit", "offset", "credentialsSubset"]

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
        """Create an instance of QueryDatasetsSummaryRequest from a JSON string"""
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
        """Create an instance of QueryDatasetsSummaryRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "expression": obj.get("expression"),
            "searchId": obj.get("searchId"),
            "limit": obj.get("limit"),
            "offset": obj.get("offset"),
            "credentialsSubset": obj.get("credentialsSubset")
        })
        return _obj


