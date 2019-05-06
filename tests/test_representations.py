import flask_restplus.representations as rep

from json import dumps, loads
from ujson import dumps as udumps, loads as uloads

from flask import current_app


def test_representations(api):
    payload = {
        'id': 1,
        'name': 'toto',
        'address': 'test',
    }
    r = rep.output_json(payload, 200)
    assert loads(r.get_data(True)) == loads(dumps(payload))
    # now reset serializer
    rep.serializer = None
    # then enforce a custom serializer
    current_app.config['RESTPLUS_JSON_SERIALIZER'] = 'ujson'
    r2 = rep.output_json(payload, 200)
    assert uloads(r2.get_data(True)) == uloads(udumps(payload))
