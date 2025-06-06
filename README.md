# BLE Security Analytics Dashboard

A forensic dashboard for visualizing and reporting Bluetooth Low Energy (BLE), Wi-Fi, and RF anomaly sessions. Built for professional incident response, surveillance investigation, and legal reporting.

---

## **Key Features**
- Overlay of all BLE/Wi-Fi session logs: no sampling, full evidence
- Interactive visualizations: spoofing, jamming, triangulation, cross-protocol correlation, and more
- Legal/forensic export-ready for court, law enforcement, or expert review
- Easily deployable locally or on cloud platforms (Render, Google Cloud Run, Replit, etc.)

---

## **Requirements**
- Python 3.8+
- See `Requirements` for dependencies

---

## **Quick Start (Local)**
```bash
pip install -r Requirements
python app.py
```

---

## **Live Demo on Render**
1. Commit the provided `render.yaml` and `app.py` to your repository.
2. Push to GitHub and create a new web service on [Render](https://render.com/).
3. Render will automatically install the requirements and start the app using `gunicorn`.
4. Access the dashboard via the URL provided by Render.

---

## Security

This project uses [GitHub CodeQL](https://codeql.github.com/) for automated code scanning.
All pushes and pull requests are analyzed for security vulnerabilities and code quality issues.
View results in the GitHub repo Security tab.
