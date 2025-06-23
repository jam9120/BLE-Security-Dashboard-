# Project Roadmap

This document outlines upcoming milestones for expanding the BLE Security Analytics Dashboard into a full AI-powered sensor detecting platform.

## Milestones

1. **Repository Organization**
   - Maintain `main` for releases and create a `dev` branch for active development.
   - Feature branches will be used for major work (e.g., `data-ingestion`, `ml-models`, `dashboard-ui`).

2. **Data Ingestion**
   - Integrate live BLE and Wi-Fi captures.
   - Normalize sensor streams and store them in a database (SQLite locally, PostgreSQL in the cloud).

3. **Machine Learning**
   - Replace rule based thresholds with trainable models using scikit-learn or PyTorch.
   - Support periodic model updates with new captures.

4. **Dashboard Enhancements**
   - Add pages for sensor management and model status.
   - Provide filtering options and real-time updates as new data arrives.

5. **Sensor Integration**
   - Build connectors for common BLE sniffers and Wi-Fi adapters.
   - Expose a small API so sensors can stream packets directly to the app.

6. **Security & Forensics**
   - Continue static analysis with CodeQL and add Python security linters.
   - Document chain-of-custody steps for exported reports.

7. **Deployment**
   - Supply Docker and Compose files for simplified setup.
   - Document options for deploying to container platforms or serverless services.

8. **Community & Contributions**
   - Label good first issues and describe how to submit new sensor integrations or models.

