from flask import Blueprint, request, jsonify

packet_api = Blueprint('packet_api', __name__)

# In-memory storage for posted packet data
packet_store = []

@packet_api.route('/api/packets', methods=['POST'])
def ingest_packet():
    """Ingest packet data via JSON POST."""
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        return jsonify({'status': 'error', 'message': 'Invalid JSON payload'}), 400
    packet_store.append(data)
    return jsonify({'status': 'ok', 'count': len(packet_store)})

@packet_api.route('/api/packets', methods=['GET'])
def get_packets():
    """Return recently ingested packets."""
    limit = request.args.get('limit', default=10, type=int)
    return jsonify(packet_store[-limit:])
