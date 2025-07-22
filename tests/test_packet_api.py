import json
import pytest

flask = pytest.importorskip("flask")
from flask import Flask
from packet_api import packet_api


def test_packet_api_endpoints():
    app = Flask(__name__)
    app.register_blueprint(packet_api)
    client = app.test_client()

    # Post a packet
    resp = client.post('/api/packets', json={'id': 1, 'payload': 'abc'})
    assert resp.status_code == 200
    data = json.loads(resp.data.decode())
    assert data.get('status') == 'ok'
    assert data.get('count') == 1

    # Retrieve packets
    resp = client.get('/api/packets')
    assert resp.status_code == 200
    packets = json.loads(resp.data.decode())
    assert isinstance(packets, list)
    assert packets[0]['id'] == 1

