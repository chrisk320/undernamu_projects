# coding: utf-8

"""
    LINE Messaging API

    This document describes LINE Messaging API.  # noqa: E501

    The version of the OpenAPI document: 0.0.1
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic.v1 import Field, conlist
from linebot.v3.messaging.models.demographic_filter import DemographicFilter
from linebot.v3.messaging.models.gender_demographic import GenderDemographic

class GenderDemographicFilter(DemographicFilter):
    """
    GenderDemographicFilter
    """
    one_of: Optional[conlist(GenderDemographic)] = Field(None, alias="oneOf")
    type: str = "gender"

    __properties = ["type", "oneOf"]

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
    def from_json(cls, json_str: str) -> GenderDemographicFilter:
        """Create an instance of GenderDemographicFilter from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GenderDemographicFilter:
        """Create an instance of GenderDemographicFilter from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GenderDemographicFilter.parse_obj(obj)

        _obj = GenderDemographicFilter.parse_obj({
            "type": obj.get("type"),
            "one_of": obj.get("oneOf")
        })
        return _obj

