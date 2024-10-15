# coding: utf-8

"""
    OurSky SDA

    The basic flow for a new organization is as follows: 1. View the available satellite targets with the [satellite targets](https://api.prod.oursky.ai/docs/sda#tag/satellite-targets/get/v1/satellite-targets) endpoint. Copy the id of the target you want to observe. 2. Create an organization target with the [organization target](https://api.prod.oursky.ai/docs/sda#tag/organization-targets/get/v1/organization-targets) endpoint. Use the id copied from above. 3. Create a webhook with the [webhook](https://api.prod.oursky.ai/docs/sda#tag/webhooks/post/v1/communications/webhook) endpoint to receive TDMs automatically (preferred) or use the [tdms](https://api.prod.oursky.ai/docs/sda#tag/tdms/get/v1/tdms) endpoint to poll for TDMs.  Check out our [examples](https://github.com/ourskyai/oursky-examples) repository to see usage in each language.

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel, Field, StrictStr
from ourskyai_sda_api.models.filter_type import FilterType
from ourskyai_sda_api.models.tracking_type import TrackingType

class V1CreateImageSetRequest(BaseModel):
    """
    V1CreateImageSetRequest
    """
    target_id: StrictStr = Field(..., alias="targetId")
    node_id: StrictStr = Field(..., alias="nodeId")
    observation_id: Optional[StrictStr] = Field(None, alias="observationId")
    tracking_type: Optional[TrackingType] = Field(None, alias="trackingType")
    filter_type: Optional[FilterType] = Field(None, alias="filterType")
    __properties = ["targetId", "nodeId", "observationId", "trackingType", "filterType"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> V1CreateImageSetRequest:
        """Create an instance of V1CreateImageSetRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1CreateImageSetRequest:
        """Create an instance of V1CreateImageSetRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1CreateImageSetRequest.parse_obj(obj)

        _obj = V1CreateImageSetRequest.parse_obj({
            "target_id": obj.get("targetId"),
            "node_id": obj.get("nodeId"),
            "observation_id": obj.get("observationId"),
            "tracking_type": obj.get("trackingType"),
            "filter_type": obj.get("filterType")
        })
        return _obj


