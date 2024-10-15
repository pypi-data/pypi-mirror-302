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


from typing import List
from pydantic import BaseModel, Field, conlist
from ourskyai_astro_api.models.v1_node_with_location import V1NodeWithLocation

class V1GetNodes(BaseModel):
    """
    V1GetNodes
    """
    nodes: conlist(V1NodeWithLocation) = Field(...)
    __properties = ["nodes"]

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
    def from_json(cls, json_str: str) -> V1GetNodes:
        """Create an instance of V1GetNodes from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in nodes (list)
        _items = []
        if self.nodes:
            for _item in self.nodes:
                if _item:
                    _items.append(_item.to_dict())
            _dict['nodes'] = _items
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1GetNodes:
        """Create an instance of V1GetNodes from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1GetNodes.parse_obj(obj)

        _obj = V1GetNodes.parse_obj({
            "nodes": [V1NodeWithLocation.from_dict(_item) for _item in obj.get("nodes")] if obj.get("nodes") is not None else None
        })
        return _obj


