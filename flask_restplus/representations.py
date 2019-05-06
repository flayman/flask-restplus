# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

import importlib

from json import dumps

from flask import make_response, current_app

serializer = None


def output_json(data, code, headers=None):
    '''Makes a Flask response with a JSON encoded body'''

    global serializer

    settings = current_app.config.get('RESTPLUS_JSON', {})
    custom_serializer = current_app.config.get('RESTPLUS_JSON_SERIALIZER', None)

    # If the user wants to use a custom serializer, let it be
    if serializer is None and custom_serializer:
        try:
            serializer = importlib.import_module("{}.dumps".format(custom_serializer) if '.' not in custom_serializer
                                                 else custom_serializer)
        except ImportError:
            serializer = dumps
    elif serializer is None:
        serializer = dumps

    # If we're in debug mode, and the indent is not set, we set it to a
    # reasonable value here.  Note that this won't override any existing value
    # that was set.
    if current_app.debug:
        settings.setdefault('indent', 4)

    # always end the json dumps with a new line
    # see https://github.com/mitsuhiko/flask/pull/1262
    dumped = serializer(data, **settings) + "\n"

    resp = make_response(dumped, code)
    resp.headers.extend(headers or {})
    return resp
