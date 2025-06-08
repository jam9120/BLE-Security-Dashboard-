import ast
import os

SCRIPT_PATH = os.path.join(os.path.dirname(__file__), os.pardir, 'Script')


def load_script_objects():
    with open(SCRIPT_PATH) as f:
        tree = ast.parse(f.read(), filename='Script')

    sample_vars = {}
    detect_node = None
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id.startswith('sample_'):
                    sample_vars[target.id] = ast.literal_eval(node.value)
        elif isinstance(node, ast.FunctionDef) and node.name == 'detect_anomalies':
            detect_node = node

    if detect_node is None:
        raise RuntimeError('detect_anomalies function not found in Script')

    mod = {}
    exec(compile(ast.Module([detect_node], []), 'Script', 'exec'), mod)
    detect_anomalies = mod['detect_anomalies']

    populated_ble_data = {
        'spoofing_sessions': sample_vars['sample_spoofing_sessions'],
        'jamming_sessions': sample_vars['sample_jamming_sessions'],
        'movement_sessions': sample_vars['sample_movement_sessions'],
        'network_anomaly_sessions': sample_vars['sample_network_anomaly_sessions'],
        'triangulation_sessions': sample_vars['sample_triangulation_sessions'],
        'rivian_vuln_sessions': sample_vars['sample_rivian_vuln_sessions'],
        'temporal_anomaly_sessions': sample_vars['sample_temporal_anomaly_sessions'],
    }
    populated_wifi_data = {
        'cross_protocol_sessions': sample_vars['sample_cross_protocol_sessions'],
        'sensor_fusion_sessions': sample_vars['sample_sensor_fusion_sessions'],
    }
    return detect_anomalies, populated_ble_data, populated_wifi_data


def test_detect_anomalies_count():
    detect_anomalies, ble_data, wifi_data = load_script_objects()
    anomalies = detect_anomalies(ble_data, wifi_data, network_threshold=0.5)
    assert len(anomalies) == 9

