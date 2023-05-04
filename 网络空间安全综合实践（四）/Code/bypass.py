#!/usr/bin/env python

“”"
Copyright © 2006-2021 sqlmap developers (https://sqlmap.org/)
See the file ‘LICENSE’ for copying permission
“”"

from lib.core.convert import encodeBase64
from lib.core.enums import PRIORITY

priority = PRIORITY.LOW

def dependencies():
    pass

def tamper(payload, **kwargs):
    if payload:
        payload = payload.replace(‘union select’,‘unnion all select’).replace(’ ‘,’%0a’)
    return payload
