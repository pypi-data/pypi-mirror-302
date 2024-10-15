# coding: utf-8

"""
    OurSky SDA

    The basic flow for a new organization is as follows: 1. View the available satellite targets with the [satellite targets](https://api.prod.oursky.ai/docs/sda#tag/satellite-targets/get/v1/satellite-targets) endpoint. Copy the id of the target you want to observe. 2. Create an organization target with the [organization target](https://api.prod.oursky.ai/docs/sda#tag/organization-targets/get/v1/organization-targets) endpoint. Use the id copied from above. 3. Create a webhook with the [webhook](https://api.prod.oursky.ai/docs/sda#tag/webhooks/post/v1/communications/webhook) endpoint to receive TDMs automatically (preferred) or use the [tdms](https://api.prod.oursky.ai/docs/sda#tag/tdms/get/v1/tdms) endpoint to poll for TDMs.  Check out our [examples](https://github.com/ourskyai/oursky-examples) repository to see usage in each language.

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class OrbitType(str, Enum):
    """
    OrbitType
    """

    """
    allowed enum values
    """
    GEOSTATIONARY = 'GEOSTATIONARY'
    GEOSYNCHRONOUS = 'GEOSYNCHRONOUS'
    MEO = 'MEO'
    LEO = 'LEO'
    GTO = 'GTO'
    SSO = 'SSO'
    TUNDRA = 'TUNDRA'
    MOLNIYA = 'MOLNIYA'
    EGO = 'EGO'
    ESO = 'ESO'
    GHO = 'GHO'
    HAO = 'HAO'
    HEO = 'HEO'
    IGO = 'IGO'
    LMO = 'LMO'
    MGO = 'MGO'
    NSO = 'NSO'
    UFO = 'UFO'

    @classmethod
    def from_json(cls, json_str: str) -> OrbitType:
        """Create an instance of OrbitType from a JSON string"""
        return OrbitType(json.loads(json_str))


