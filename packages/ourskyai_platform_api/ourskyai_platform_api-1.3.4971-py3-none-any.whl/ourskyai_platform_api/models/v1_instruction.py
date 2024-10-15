# coding: utf-8

"""
    OurSky Platform

    No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)

    The version of the OpenAPI document: 1.3.4971
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import List, Optional
from pydantic import BaseModel, conlist
from ourskyai_platform_api.models.v1_auto_focus_instruction import V1AutoFocusInstruction
from ourskyai_platform_api.models.v1_diagnostic_instruction import V1DiagnosticInstruction
from ourskyai_platform_api.models.v1_observation_instruction import V1ObservationInstruction

class V1Instruction(BaseModel):
    """
    Instruction  # noqa: E501
    """
    observation: Optional[V1ObservationInstruction] = None
    diagnostic: Optional[V1DiagnosticInstruction] = None
    search: Optional[conlist(V1ObservationInstruction)] = None
    autofocus: Optional[V1AutoFocusInstruction] = None
    __properties = ["observation", "diagnostic", "search", "autofocus"]

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
    def from_json(cls, json_str: str) -> V1Instruction:
        """Create an instance of V1Instruction from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of observation
        if self.observation:
            _dict['observation'] = self.observation.to_dict()
        # override the default output from pydantic by calling `to_dict()` of diagnostic
        if self.diagnostic:
            _dict['diagnostic'] = self.diagnostic.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in search (list)
        _items = []
        if self.search:
            for _item in self.search:
                if _item:
                    _items.append(_item.to_dict())
            _dict['search'] = _items
        # override the default output from pydantic by calling `to_dict()` of autofocus
        if self.autofocus:
            _dict['autofocus'] = self.autofocus.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> V1Instruction:
        """Create an instance of V1Instruction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return V1Instruction.parse_obj(obj)

        _obj = V1Instruction.parse_obj({
            "observation": V1ObservationInstruction.from_dict(obj.get("observation")) if obj.get("observation") is not None else None,
            "diagnostic": V1DiagnosticInstruction.from_dict(obj.get("diagnostic")) if obj.get("diagnostic") is not None else None,
            "search": [V1ObservationInstruction.from_dict(_item) for _item in obj.get("search")] if obj.get("search") is not None else None,
            "autofocus": V1AutoFocusInstruction.from_dict(obj.get("autofocus")) if obj.get("autofocus") is not None else None
        })
        return _obj


