#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Created with https://app.quicktype.io
#   name: cachet

json_schema = """
{
    "$ref": "#/definitions/Cachet",
    "definitions": {
        "Lxc": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "check": {
                    "type": "boolean"
                },
                "component_prefix": {
                    "type": "string"
                }
            },
            "required": [
                "check",
                "component_prefix"
            ],
            "title": "lxc"
        },
        "Endpoint": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "component": {
                    "type": "string"
                },
                "url": {
                    "type": "string"
                },
                "regex": {
                    "type": "string"
                }
            },
            "required": [
                "component",
                "regex",
                "url"
            ],
            "title": "endpoint"
        },
        "URL": {
            "type": "object",
            "additionalProperties": false,
            "properties": {
                "check": {
                    "type": "boolean"
                },
                "endpoints": {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/Endpoint"
                    }
                }
            },
            "required": [
                "check",
                "endpoints"
            ],
            "title": "url"
        },
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
                "lxc": {
                    "$ref": "#/definitions/Lxc"
                },
                "url": {
                    "$ref": "#/definitions/URL"
                }
            },
            "required": [
                "api_token",
                "api_url",
                "lxc",
                "url"
            ],
            "title": "cachet"
        }
    }
}
"""