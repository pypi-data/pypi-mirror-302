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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr, field_validator
from typing import Any, ClassVar, Dict, List, Optional, Union
from kdp_api.models.workspace_subscription_subscription_item_ids import WorkspaceSubscriptionSubscriptionItemIds
from typing import Optional, Set
from typing_extensions import Self

class WorkspaceSubscription(BaseModel):
    """
    subscription for workspace
    """ # noqa: E501
    current_period_start: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="current period start date", alias="currentPeriodStart")
    current_period_end: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="current period end date", alias="currentPeriodEnd")
    cancel_at_period_end: Optional[StrictBool] = Field(default=None, description="cancel subscription at period end flag", alias="cancelAtPeriodEnd")
    status: Optional[StrictStr] = Field(default=None, description="subscription status")
    trial_start: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="trial start date", alias="trialStart")
    trial_end: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="trial end date", alias="trialEnd")
    concurrency: Optional[Union[StrictFloat, StrictInt]] = None
    subscription_item_ids: Optional[WorkspaceSubscriptionSubscriptionItemIds] = Field(default=None, alias="subscriptionItemIds")
    __properties: ClassVar[List[str]] = ["currentPeriodStart", "currentPeriodEnd", "cancelAtPeriodEnd", "status", "trialStart", "trialEnd", "concurrency", "subscriptionItemIds"]

    @field_validator('status')
    def status_validate_enum(cls, value):
        """Validates the enum"""
        if value is None:
            return value

        if value not in set(['incomplete', 'incomplete_expired', 'trialing', 'active', 'past_due', 'canceled', 'unpaid']):
            raise ValueError("must be one of enum values ('incomplete', 'incomplete_expired', 'trialing', 'active', 'past_due', 'canceled', 'unpaid')")
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
        """Create an instance of WorkspaceSubscription from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of subscription_item_ids
        if self.subscription_item_ids:
            _dict['subscriptionItemIds'] = self.subscription_item_ids.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of WorkspaceSubscription from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "currentPeriodStart": obj.get("currentPeriodStart"),
            "currentPeriodEnd": obj.get("currentPeriodEnd"),
            "cancelAtPeriodEnd": obj.get("cancelAtPeriodEnd"),
            "status": obj.get("status"),
            "trialStart": obj.get("trialStart"),
            "trialEnd": obj.get("trialEnd"),
            "concurrency": obj.get("concurrency"),
            "subscriptionItemIds": WorkspaceSubscriptionSubscriptionItemIds.from_dict(obj["subscriptionItemIds"]) if obj.get("subscriptionItemIds") is not None else None
        })
        return _obj


