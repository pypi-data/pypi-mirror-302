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

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, Field, StrictStr, conlist
from ourskyai_sda_api.models.v1_observation_sequence_result_image_sets_inner import V1ObservationSequenceResultImageSetsInner

class V1ObservationSequenceResult(BaseModel):
    """
    Observation Sequence Result  # noqa: E501
    """
    id: StrictStr = Field(...)
    target_id: StrictStr = Field(..., alias="targetId")
    norad_id: Optional[StrictStr] = Field(None, alias="noradId")
    generated_tle_line1: Optional[StrictStr] = Field(None, alias="generatedTleLine1", description="Resulting line 1 of TLE generated from Batch Least Squares fit of orbit from recently extracted streaks")
    generated_tle_line2: Optional[StrictStr] = Field(None, alias="generatedTleLine2", description="Resulting line 2 of TLE generated from Batch Least Squares fit of orbit from recently extracted streaks")
    image_sets: conlist(V1ObservationSequenceResultImageSetsInner) = Field(..., alias="imageSets")
    created_at: datetime = Field(..., alias="createdAt")
    created_by: StrictStr = Field(..., alias="createdBy")
    __properties = ["id", "targetId", "noradId", "generatedTleLine1", "generatedTleLine2", "imageSets", "createdAt", "createdBy"]

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
    def from_json(cls, json_str: str) -> V1ObservationSequenceResult:
        """Create an instance of V1ObservationSequenceResult from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in image_sets (list)
        _items = []
        if self.image_sets:
            for _item in self.image_sets:
                if _item:
                    _items.append(_item.to_dict())
            _dict['imageSets'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1ObservationSequenceResult:
        """Create an instance of V1ObservationSequenceResult from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1ObservationSequenceResult.parse_obj(obj)

        _obj = V1ObservationSequenceResult.parse_obj({
            "id": obj.get("id"),
            "target_id": obj.get("targetId"),
            "norad_id": obj.get("noradId"),
            "generated_tle_line1": obj.get("generatedTleLine1"),
            "generated_tle_line2": obj.get("generatedTleLine2"),
            "image_sets": [V1ObservationSequenceResultImageSetsInner.from_dict(_item) for _item in obj.get("imageSets")] if obj.get("imageSets") is not None else None,
            "created_at": obj.get("createdAt"),
            "created_by": obj.get("createdBy")
        })
        return _obj


