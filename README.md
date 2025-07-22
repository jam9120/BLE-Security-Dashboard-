# BLE Security Analytics Dashboard

A forensic dashboard for visualizing and reporting Bluetooth Low Energy (BLE), Wi-Fi, and RF anomaly sessions. Built for professional incident response, surveillance investigation, and legal reporting.

## Summary

The dashboard aggregates BLE, Wi-Fi, and other RF session data to surface spoofing,
jamming, and cross-protocol attacks. It provides interactive charts for analysis
and exportable reports suitable for legal or investigative use.

---

## **Key Features**
- Overlay of all BLE/Wi-Fi session logs: no sampling, full evidence
- Interactive visualizations: spoofing, jamming, triangulation, cross-protocol correlation, and more
- Legal/forensic export-ready for court, law enforcement, or expert review
- Easily deployable locally or on cloud platforms (Render, Google Cloud Run, Replit, etc.)

- RSSI screenshot training pipeline in `rssi-resnet-detector` for anomaly classification
---

## **Current Status**
- The application currently uses `ble_dashboard.py` as the main entry point.
- Data ingestion (`data_ingestion.py`) relies on fallback sample data for Bluetooth SIG assigned numbers and security notices. This is due to ongoing issues accessing the live external data sources (returning 404/403 errors). This ensures the dashboard remains operational and can display sample insights.

---

## **Requirements**
- Python 3.8+
- See `Requirements` for dependencies

---

## **Quick Start (Local)**
```bash
pip install -r Requirements
python ble_dashboard.py
```
## RSSI ResNet Detector
See `rssi-resnet-detector/README.md` for training a ResNet model on RSSI screenshots.


---

## **Deployment with Gunicorn**
To run the application with Gunicorn (a production WSGI server), use the following command:
```bash
gunicorn ble_dashboard:server -b 0.0.0.0:8050
```
Ensure Gunicorn is installed (it's listed in the `Requirements` file). The `server` object is made available in `ble_dashboard.py` for Gunicorn.

---

## Sensor Packet API

Sensors can stream packets directly to the dashboard via a simple REST API.

- `POST /api/packets` – submit a JSON packet payload.
- `GET /api/packets?limit=10` – retrieve the most recent packets.

Packets are currently kept in memory.

---

## Security

This project uses [GitHub CodeQL](https://codeql.github.com/) for automated code scanning.
All pushes and pull requests are analyzed for security vulnerabilities and code quality issues.
View results in the GitHub repo Security tab.

---

## Roadmap

The overall development direction is documented in [ROADMAP.md](ROADMAP.md). It outlines upcoming work such as sensor integration, machine learning models and deployment improvements.

---

## About

Maintained by [jam9120](https://github.com/jam9120).

jam9120 is a security researcher focused on Bluetooth Low Energy and wireless
anomaly analytics. This dashboard grew out of work building forensic tools for
incident responders. Contributions and feedback are welcome.
