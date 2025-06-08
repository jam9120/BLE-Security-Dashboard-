import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from data_ingestion import fetch_assigned_numbers_data, fetch_sig_security_notices, fetch_nrf_security_advisories

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server # Expose server for Gunicorn

# Fetch data
assigned_numbers = fetch_assigned_numbers_data()
sig_notices = fetch_sig_security_notices()
nrf_advisories = fetch_nrf_security_advisories()

# App layout
app.layout = dbc.Container([
    dbc.Row(dbc.Col(html.H1("BLE Security Analytics Dashboard"), width=12)),

    dbc.Row([
        dbc.Col([
            html.H3("Data Ingestion Summary"),
            html.P(f"Company Identifiers: {len(assigned_numbers.get('company_identifiers', []))}"),
            html.P(f"Service UUIDs: {len(assigned_numbers.get('service_uuids', []))}"),
            html.P(f"Protocol Identifiers: {len(assigned_numbers.get('protocol_identifiers', []))}"),
            html.P(f"Bluetooth SIG Security Notices: {len(sig_notices)}"),
            html.P(f"nRF Security Advisories: {len(nrf_advisories)}"),
        ], width=12)
    ]),

    # Placeholder for future visualizations and tables
    dbc.Row([
        dbc.Col([
            html.H4("SIG Security Notices"),
            # Displaying titles of SIG notices as an example
            html.Ul([html.Li(notice.get('title')) for notice in sig_notices[:5]]) # Display first 5
        ], md=6),
        dbc.Col([
            html.H4("nRF Advisories"),
            # Displaying summaries of nRF advisories
            html.Ul([html.Li(f"{advisory.get('cve_id')}: {advisory.get('summary')}") for advisory in nrf_advisories[:5]]) # Display first 5
        ], md=6)
    ])
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
