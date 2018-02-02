#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: cachet

json_schema = """
{
    "$ref": "#/definitions/Cachet",
    "definitions": {
        "Cachet": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "api_token": {
                    "type": "string"
                },
                "api_url": {
                    "type": "string"
                },
                "lxc_check": {
                    "type": "boolean"
                },
                "lxc_component_prefix": {
                    "type": "string"
                }
            },
            "required": [
                "api_token",
                "api_url",
                "lxc_check",
                "lxc_component_prefix"
            ],
            "title": "cachet"
        }
    }
}
"""