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


from typing import Optional, Union
from pydantic import BaseModel, Field, StrictFloat, StrictInt, StrictStr

class V1UpdateSatelliteTargetRequest(BaseModel):
    """
    V1UpdateSatelliteTargetRequest
    """
    target_id: StrictStr = Field(..., alias="targetId")
    tle_name: Optional[StrictStr] = Field(None, alias="tleName")
    tle_line1: StrictStr = Field(..., alias="tleLine1")
    tle_line2: StrictStr = Field(..., alias="tleLine2")
    linked_satellite_target_id: Optional[StrictStr] = Field(None, alias="linkedSatelliteTargetId", description="-| The OurSky Satellite Target. When this is specified OurSky will automatically choose the TLE to use based on which target has the newest TLE. The private target or the upstream target. Caution, setting this to null will unlink the target")
    mass: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="mass in kilograms. Caution, setting this to null well set the satellite target mass to null")
    coefficient_of_reflection: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="coefficientOfReflection", description="The Cr value used to calculate acceleration due to solar radiation pressure. Caution, setting this value to null will set the satellite target Cr value to null.")
    cross_section: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="crossSection", description="cross sectional area in meters^2. Caution, setting this value to null will set the crossSection to null")
    __properties = ["targetId", "tleName", "tleLine1", "tleLine2", "linkedSatelliteTargetId", "mass", "coefficientOfReflection", "crossSection"]

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
    def from_json(cls, json_str: str) -> V1UpdateSatelliteTargetRequest:
        """Create an instance of V1UpdateSatelliteTargetRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1UpdateSatelliteTargetRequest:
        """Create an instance of V1UpdateSatelliteTargetRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1UpdateSatelliteTargetRequest.parse_obj(obj)

        _obj = V1UpdateSatelliteTargetRequest.parse_obj({
            "target_id": obj.get("targetId"),
            "tle_name": obj.get("tleName"),
            "tle_line1": obj.get("tleLine1"),
            "tle_line2": obj.get("tleLine2"),
            "linked_satellite_target_id": obj.get("linkedSatelliteTargetId"),
            "mass": obj.get("mass"),
            "coefficient_of_reflection": obj.get("coefficientOfReflection"),
            "cross_section": obj.get("crossSection")
        })
        return _obj


