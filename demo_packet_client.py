import requests
import json

# Simple demo to post a packet and fetch packets from the running dashboard
BASE_URL = 'http://localhost:8050'

sample_packet = {
    'id': 1,
    'payload': 'demo',
}

post_resp = requests.post(f'{BASE_URL}/api/packets', json=sample_packet)
print('POST status:', post_resp.status_code)
print('POST response:', post_resp.json())

get_resp = requests.get(f'{BASE_URL}/api/packets')
print('GET status:', get_resp.status_code)
print('Packets:', json.dumps(get_resp.json(), indent=2))
