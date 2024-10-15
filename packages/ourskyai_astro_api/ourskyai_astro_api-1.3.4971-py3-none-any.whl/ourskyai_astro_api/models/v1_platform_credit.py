# coding: utf-8

"""
    OurSky Astro

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, StrictInt, StrictStr
from ourskyai_astro_api.models.v1_platform_credit_source import V1PlatformCreditSource
from ourskyai_astro_api.models.v1_platform_credit_type import V1PlatformCreditType
from ourskyai_astro_api.models.v1_platform_credit_unit import V1PlatformCreditUnit

class V1PlatformCredit(BaseModel):
    """
    Platform Credit  # noqa: E501
    """
    id: StrictStr = Field(...)
    organization: Optional[StrictStr] = None
    type: V1PlatformCreditType = Field(...)
    unit: V1PlatformCreditUnit = Field(...)
    source: V1PlatformCreditSource = Field(...)
    amount: StrictInt = Field(...)
    created_by: StrictStr = Field(..., alias="createdBy")
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: datetime = Field(..., alias="updatedAt")
    __properties = ["id", "organization", "type", "unit", "source", "amount", "createdBy", "createdAt", "updatedAt"]

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
    def from_json(cls, json_str: str) -> V1PlatformCredit:
        """Create an instance of V1PlatformCredit from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1PlatformCredit:
        """Create an instance of V1PlatformCredit from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1PlatformCredit.parse_obj(obj)

        _obj = V1PlatformCredit.parse_obj({
            "id": obj.get("id"),
            "organization": obj.get("organization"),
            "type": obj.get("type"),
            "unit": obj.get("unit"),
            "source": obj.get("source"),
            "amount": obj.get("amount"),
            "created_by": obj.get("createdBy"),
            "created_at": obj.get("createdAt"),
            "updated_at": obj.get("updatedAt")
        })
        return _obj


