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
from typing import Optional, Union
from pydantic import BaseModel, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from ourskyai_astro_api.models.calibration_master_type import CalibrationMasterType
from ourskyai_astro_api.models.filter_type import FilterType

class V1CreateCalibrationMasterRequest(BaseModel):
    """
    V1CreateCalibrationMasterRequest
    """
    node_id: StrictStr = Field(..., alias="nodeId")
    calibration_master_type: CalibrationMasterType = Field(..., alias="calibrationMasterType")
    filter_type: Optional[FilterType] = Field(None, alias="filterType")
    bin_xy: StrictInt = Field(..., alias="binXY")
    gain: Optional[StrictInt] = None
    readout_mode: Optional[StrictInt] = Field(None, alias="readoutMode")
    temperature: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="temperature in degrees celsius")
    exposure_time: Union[StrictFloat, StrictInt] = Field(..., alias="exposureTime")
    rotator_angle: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="rotatorAngle")
    offset: Optional[StrictInt] = None
    overwrite: Optional[StrictBool] = None
    captured_at: Optional[datetime] = Field(None, alias="capturedAt")
    __properties = ["nodeId", "calibrationMasterType", "filterType", "binXY", "gain", "readoutMode", "temperature", "exposureTime", "rotatorAngle", "offset", "overwrite", "capturedAt"]

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
    def from_json(cls, json_str: str) -> V1CreateCalibrationMasterRequest:
        """Create an instance of V1CreateCalibrationMasterRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1CreateCalibrationMasterRequest:
        """Create an instance of V1CreateCalibrationMasterRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1CreateCalibrationMasterRequest.parse_obj(obj)

        _obj = V1CreateCalibrationMasterRequest.parse_obj({
            "node_id": obj.get("nodeId"),
            "calibration_master_type": obj.get("calibrationMasterType"),
            "filter_type": obj.get("filterType"),
            "bin_xy": obj.get("binXY"),
            "gain": obj.get("gain"),
            "readout_mode": obj.get("readoutMode"),
            "temperature": obj.get("temperature"),
            "exposure_time": obj.get("exposureTime"),
            "rotator_angle": obj.get("rotatorAngle"),
            "offset": obj.get("offset"),
            "overwrite": obj.get("overwrite"),
            "captured_at": obj.get("capturedAt")
        })
        return _obj


