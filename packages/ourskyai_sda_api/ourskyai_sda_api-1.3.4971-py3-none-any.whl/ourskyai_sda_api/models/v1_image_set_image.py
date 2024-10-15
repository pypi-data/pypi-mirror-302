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
from typing import List, Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr, conlist
from ourskyai_sda_api.models.fits_header import FitsHeader
from ourskyai_sda_api.models.v1_predicted_streak_location import V1PredictedStreakLocation

class V1ImageSetImage(BaseModel):
    """
    Image Set Image  # noqa: E501
    """
    id: StrictStr = Field(...)
    thumbnail_url: Optional[StrictStr] = Field(None, alias="thumbnailUrl")
    image_url: StrictStr = Field(..., alias="imageUrl")
    full_jpg_url: Optional[StrictStr] = Field(None, alias="fullJpgUrl")
    node_id: StrictStr = Field(..., alias="nodeId")
    target_id: Optional[StrictStr] = Field(None, alias="targetId")
    ra: Optional[Union[StrictFloat, StrictInt]] = None
    dec: Optional[Union[StrictFloat, StrictInt]] = None
    image_set_id: StrictStr = Field(..., alias="imageSetId")
    dark_calibrated: StrictBool = Field(..., alias="darkCalibrated")
    flat_calibrated: StrictBool = Field(..., alias="flatCalibrated")
    bias_calibrated: StrictBool = Field(..., alias="biasCalibrated")
    fwhm_average: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fwhmAverage")
    fwhm_std_dev: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fwhmStdDev")
    fwhm_angle: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="fwhmAngle")
    ra_offset: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="raOffset")
    dec_offset: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="decOffset")
    total_offset: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="totalOffset")
    total_offset_std_dev: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="totalOffsetStdDev")
    total_offset_rms: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="totalOffsetRMS")
    captured_at: datetime = Field(..., alias="capturedAt")
    created_at: datetime = Field(..., alias="createdAt")
    binning: Optional[StrictInt] = None
    exposure_length: Union[StrictFloat, StrictInt] = Field(..., alias="exposureLength")
    fits_headers: conlist(FitsHeader) = Field(..., alias="fitsHeaders")
    predicted_streak_location: Optional[V1PredictedStreakLocation] = Field(None, alias="predictedStreakLocation")
    __properties = ["id", "thumbnailUrl", "imageUrl", "fullJpgUrl", "nodeId", "targetId", "ra", "dec", "imageSetId", "darkCalibrated", "flatCalibrated", "biasCalibrated", "fwhmAverage", "fwhmStdDev", "fwhmAngle", "raOffset", "decOffset", "totalOffset", "totalOffsetStdDev", "totalOffsetRMS", "capturedAt", "createdAt", "binning", "exposureLength", "fitsHeaders", "predictedStreakLocation"]

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
    def from_json(cls, json_str: str) -> V1ImageSetImage:
        """Create an instance of V1ImageSetImage from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in fits_headers (list)
        _items = []
        if self.fits_headers:
            for _item in self.fits_headers:
                if _item:
                    _items.append(_item.to_dict())
            _dict['fitsHeaders'] = _items
        # override the default output from pydantic by calling `to_dict()` of predicted_streak_location
        if self.predicted_streak_location:
            _dict['predictedStreakLocation'] = self.predicted_streak_location.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1ImageSetImage:
        """Create an instance of V1ImageSetImage from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1ImageSetImage.parse_obj(obj)

        _obj = V1ImageSetImage.parse_obj({
            "id": obj.get("id"),
            "thumbnail_url": obj.get("thumbnailUrl"),
            "image_url": obj.get("imageUrl"),
            "full_jpg_url": obj.get("fullJpgUrl"),
            "node_id": obj.get("nodeId"),
            "target_id": obj.get("targetId"),
            "ra": obj.get("ra"),
            "dec": obj.get("dec"),
            "image_set_id": obj.get("imageSetId"),
            "dark_calibrated": obj.get("darkCalibrated"),
            "flat_calibrated": obj.get("flatCalibrated"),
            "bias_calibrated": obj.get("biasCalibrated"),
            "fwhm_average": obj.get("fwhmAverage"),
            "fwhm_std_dev": obj.get("fwhmStdDev"),
            "fwhm_angle": obj.get("fwhmAngle"),
            "ra_offset": obj.get("raOffset"),
            "dec_offset": obj.get("decOffset"),
            "total_offset": obj.get("totalOffset"),
            "total_offset_std_dev": obj.get("totalOffsetStdDev"),
            "total_offset_rms": obj.get("totalOffsetRMS"),
            "captured_at": obj.get("capturedAt"),
            "created_at": obj.get("createdAt"),
            "binning": obj.get("binning"),
            "exposure_length": obj.get("exposureLength"),
            "fits_headers": [FitsHeader.from_dict(_item) for _item in obj.get("fitsHeaders")] if obj.get("fitsHeaders") is not None else None,
            "predicted_streak_location": V1PredictedStreakLocation.from_dict(obj.get("predictedStreakLocation")) if obj.get("predictedStreakLocation") is not None else None
        })
        return _obj


