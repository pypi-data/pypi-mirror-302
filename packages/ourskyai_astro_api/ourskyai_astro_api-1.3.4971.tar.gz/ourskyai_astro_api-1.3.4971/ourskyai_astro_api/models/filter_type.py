# coding: utf-8

"""
    OurSky Astro

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


import json
import pprint
import re  # noqa: F401
from aenum import Enum, no_arg





class FilterType(str, Enum):
    """
    FilterType
    """

    """
    allowed enum values
    """
    NONE = 'NONE'
    RED = 'RED'
    BLUE = 'BLUE'
    GREEN = 'GREEN'
    UV = 'UV'
    IR = 'IR'
    LUMINANCE = 'LUMINANCE'
    ENHANCED_LUMINANCE = 'ENHANCED_LUMINANCE'
    H_ALPHA = 'H_ALPHA'
    H_BETA = 'H_BETA'
    S_II = 'S_II'
    O_III = 'O_III'
    DUAL_BAND = 'DUAL_BAND'
    PHOTO_JOHNSON_U = 'PHOTO_JOHNSON_U'
    PHOTO_JOHNSON_B = 'PHOTO_JOHNSON_B'
    PHOTO_JOHNSON_V = 'PHOTO_JOHNSON_V'
    PHOTO_COUSINS_R = 'PHOTO_COUSINS_R'
    PHOTO_COUSINS_I = 'PHOTO_COUSINS_I'

    @classmethod
    def from_json(cls, json_str: str) -> FilterType:
        """Create an instance of FilterType from a JSON string"""
        return FilterType(json.loads(json_str))


