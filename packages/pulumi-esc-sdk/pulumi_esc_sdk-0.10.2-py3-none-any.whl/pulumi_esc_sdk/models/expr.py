# coding: utf-8

# Copyright 2024, Pulumi Corporation.  All rights reserved.

"""
    ESC (Environments, Secrets, Config) API

    Pulumi ESC allows you to compose and manage hierarchical collections of configuration and secrets and consume them in various ways.

    The version of the OpenAPI document: 0.1.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List, Optional
from pulumi_esc_sdk.models.access import Access
from pulumi_esc_sdk.models.interpolation import Interpolation
from pulumi_esc_sdk.models.property_accessor import PropertyAccessor
from pulumi_esc_sdk.models.range import Range
from typing import Optional, Set
from typing_extensions import Self

class Expr(BaseModel):
    """
    Expr
    """ # noqa: E501
    range: Optional[Range] = None
    base: Optional[Expr] = None
    var_schema: Optional[Any] = Field(default=None, alias="schema")
    key_ranges: Optional[Dict[str, Range]] = Field(default=None, alias="keyRanges")
    literal: Optional[Any] = None
    interpolate: Optional[List[Interpolation]] = None
    symbol: Optional[List[PropertyAccessor]] = None
    access: Optional[List[Access]] = None
    list: Optional[List[Expr]] = None
    object: Optional[Dict[str, Expr]] = None
    builtin: Optional[ExprBuiltin] = None
    __properties: ClassVar[List[str]] = ["range", "base", "schema", "keyRanges", "literal", "interpolate", "symbol", "access", "list", "object", "builtin"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of Expr from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of range
        if self.range:
            _dict['range'] = self.range.to_dict()
        # override the default output from pydantic by calling `to_dict()` of base
        if self.base:
            _dict['base'] = self.base.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in key_ranges (dict)
        _field_dict = {}
        if self.key_ranges:
            for _key in self.key_ranges:
                if self.key_ranges[_key]:
                    _field_dict[_key] = self.key_ranges[_key].to_dict()
            _dict['keyRanges'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each item in interpolate (list)
        _items = []
        if self.interpolate:
            for _item in self.interpolate:
                if _item:
                    _items.append(_item.to_dict())
            _dict['interpolate'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in symbol (list)
        _items = []
        if self.symbol:
            for _item in self.symbol:
                if _item:
                    _items.append(_item.to_dict())
            _dict['symbol'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in access (list)
        _items = []
        if self.access:
            for _item in self.access:
                if _item:
                    _items.append(_item.to_dict())
            _dict['access'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in list (list)
        _items = []
        if self.list:
            for _item in self.list:
                if _item:
                    _items.append(_item.to_dict())
            _dict['list'] = _items
        # override the default output from pydantic by calling `to_dict()` of each value in object (dict)
        _field_dict = {}
        if self.object:
            for _key in self.object:
                if self.object[_key]:
                    _field_dict[_key] = self.object[_key].to_dict()
            _dict['object'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of builtin
        if self.builtin:
            _dict['builtin'] = self.builtin.to_dict()
        # set to None if var_schema (nullable) is None
        # and model_fields_set contains the field
        if self.var_schema is None and "var_schema" in self.model_fields_set:
            _dict['schema'] = None

        # set to None if literal (nullable) is None
        # and model_fields_set contains the field
        if self.literal is None and "literal" in self.model_fields_set:
            _dict['literal'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Expr from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "range": Range.from_dict(obj["range"]) if obj.get("range") is not None else None,
            "base": Expr.from_dict(obj["base"]) if obj.get("base") is not None else None,
            "schema": obj.get("schema"),
            "keyRanges": dict(
                (_k, Range.from_dict(_v))
                for _k, _v in obj["keyRanges"].items()
            )
            if obj.get("keyRanges") is not None
            else None,
            "literal": obj.get("literal"),
            "interpolate": [Interpolation.from_dict(_item) for _item in obj["interpolate"]] if obj.get("interpolate") is not None else None,
            "symbol": [PropertyAccessor.from_dict(_item) for _item in obj["symbol"]] if obj.get("symbol") is not None else None,
            "access": [Access.from_dict(_item) for _item in obj["access"]] if obj.get("access") is not None else None,
            "list": [Expr.from_dict(_item) for _item in obj["list"]] if obj.get("list") is not None else None,
            "object": dict(
                (_k, Expr.from_dict(_v))
                for _k, _v in obj["object"].items()
            )
            if obj.get("object") is not None
            else None,
            "builtin": ExprBuiltin.from_dict(obj["builtin"]) if obj.get("builtin") is not None else None
        })
        return _obj

from pulumi_esc_sdk.models.expr_builtin import ExprBuiltin
# TODO: Rewrite to not use raise_errors
Expr.model_rebuild(raise_errors=False)

