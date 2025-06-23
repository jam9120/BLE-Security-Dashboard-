import yaml
import requests
import re
from bs4 import BeautifulSoup

# --- YAML Data Ingestion ---
BASE_URL = "https://bitbucket.org/bluetooth-SIG/public/raw/HEAD/assigned_numbers/"
FILES_TO_FETCH = {
    "company_identifiers": "company_identifiers.yaml",
    "service_uuids": "service_uuids.yaml",
    "protocol_identifiers": "protocol_identifiers.yaml",
}

# Using 'value' for OUI as per typical YAML structure for this, and string hex.
# Standard OUI format is 6 hex characters.
SAMPLE_COMPANY_IDENTIFIERS_YAML = """
- value: "0002B3" # Intel Corp.
  name: Intel Corp. (Sample)
- value: "BCF685" # Raspberry Pi Foundation
  name: Raspberry Pi Foundation (Sample)
- value: "001A7D" # Example OUI for Fictional Devices
  name: Fictional Devices Ltd (Sample)
- value: "001986" # Nordic Semiconductor ASA - One of their OUIs
  name: Nordic Semiconductor ASA (Sample)
"""

SAMPLE_SERVICE_UUIDS_YAML = """
- uuid: "1800" # Removed 0x prefix, will handle in parsing if needed, or assume strings
  name: Generic Access
- uuid: "1801"
  name: Generic Attribute
- uuid: "180F"
  name: Battery Service
- uuid: "180D"
  name: Heart Rate
- uuid: "180A"
  name: Device Information
"""

SAMPLE_PROTOCOL_IDENTIFIERS_YAML = """
- name: SDP
  uuid: "0x0001"
- name: UDP
  uuid: "0x0002"
- name: RFCOMM
  uuid: "0x0003"
"""

def fetch_assigned_numbers_data():
    parsed_data = {}
    data_loaded_from_fallback = False
    for key, filename in FILES_TO_FETCH.items():
        try:
            url = BASE_URL + filename
            print(f"Attempting to fetch {url}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            print(f"Successfully fetched {filename}. Parsing...")
            data = yaml.safe_load(response.content)
            if isinstance(data, dict) and len(data) == 1 and isinstance(list(data.values())[0], list):
                parsed_data[key] = list(data.values())[0]
            elif isinstance(data, list):
                 parsed_data[key] = data
            else:
                print(f"Warning: Unexpected YAML structure for {filename}. Using raw parsed data.")
                parsed_data[key] = data
            print(f"Successfully parsed {filename}.")
        except requests.exceptions.RequestException as e:
            print(f"Warning: Could not fetch {filename} due to: {e}. Using fallback sample for {key}.")
            data_loaded_from_fallback = True
            if key == "company_identifiers":
                parsed_data[key] = yaml.safe_load(SAMPLE_COMPANY_IDENTIFIERS_YAML)
            elif key == "service_uuids":
                parsed_data[key] = yaml.safe_load(SAMPLE_SERVICE_UUIDS_YAML)
            elif key == "protocol_identifiers":
                parsed_data[key] = yaml.safe_load(SAMPLE_PROTOCOL_IDENTIFIERS_YAML)
            else:
                parsed_data[key] = []
        except yaml.YAMLError as e:
            print(f"Warning: Could not parse YAML for {filename} (or its fallback) due to: {e}. Setting empty list for {key}.")
            data_loaded_from_fallback = True
            parsed_data[key] = []
        except Exception as e:
            print(f"An unexpected error occurred with {filename}: {e}. Using fallback for {key} if available.")
            data_loaded_from_fallback = True
            # Ensure fallback uses specific samples if available
            if key == "company_identifiers": parsed_data[key] = yaml.safe_load(SAMPLE_COMPANY_IDENTIFIERS_YAML)
            elif key == "service_uuids": parsed_data[key] = yaml.safe_load(SAMPLE_SERVICE_UUIDS_YAML)
            elif key == "protocol_identifiers": parsed_data[key] = yaml.safe_load(SAMPLE_PROTOCOL_IDENTIFIERS_YAML)
            else: parsed_data[key] = []

    if data_loaded_from_fallback:
        print("INFO: One or more YAML data files were loaded from fallback samples.")
    else:
        print("INFO: All YAML data successfully fetched and parsed from remote URLs.")
    return parsed_data

# --- HTML Data Ingestion (Security Notices) ---
SECURITY_NOTICES_URL = "https://www.bluetooth.com/learn-about-bluetooth/key-attributes/bluetooth-security/reporting-security/"
SAMPLE_SECURITY_NOTICES_HTML = """
<html><body>
<h2>Bluetooth® security notices</h2>
<div class="table-container"><table>
  <thead>
    <tr>
      <th>Vulnerability</th>
      <th>Original Publication Date</th>
      <th>Affected Specifications</th>
      <th>CVE Identifier</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><a href="/specifications/security-notice/example-notice-1/">Example Vulnerability 1 (EN-1)</a></td>
      <td>2023-01-15</td>
      <td>Core Specification v5.0 - v5.3, and devices implementing Battery Service (180F)</td>
      <td><a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2023-0001" target="_blank">CVE-2023-0001</a></td>
    </tr>
    <tr>
      <td><a href="/specifications/security-notice/example-notice-2/">Another Example (EN-2)</a></td>
      <td>2022-11-20</td>
      <td>Mesh Profile v1.0, v1.0.1, and Heart Rate Profile (180D)</td>
      <td><a href="https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2022-1234" target="_blank">CVE-2022-1234</a></td>
    </tr>
  </tbody>
</table></div>
</body></html>
"""

def fetch_sig_security_notices():
    notices = []
    html_content = ""
    using_fallback = False
    try:
        print(f"Attempting to fetch Bluetooth SIG Security Notices from {SECURITY_NOTICES_URL}...")
        response = requests.get(SECURITY_NOTICES_URL, timeout=15)
        response.raise_for_status()
        print("Successfully fetched security notices page.")
        html_content = response.text
    except requests.exceptions.RequestException as e:
        print(f"Warning: Could not fetch security notices page due to: {e}. Using fallback HTML sample.")
        html_content = SAMPLE_SECURITY_NOTICES_HTML
        using_fallback = True
    except Exception as e:
        print(f"An unexpected error occurred during fetching security notices: {e}. Using fallback HTML sample.")
        html_content = SAMPLE_SECURITY_NOTICES_HTML
        using_fallback = True

    if not html_content:
        print("Error: No HTML content to parse.")
        return []

    try:
        print("Parsing security notices HTML...")
        soup = BeautifulSoup(html_content, 'lxml')

        table_container = soup.find('div', class_='table-container')
        if not table_container:
            table_container = soup # Fallback to searching in whole soup

        table = table_container.find("table") if table_container else None

        if not table:
            msg = "Security notices table not found in HTML."
            if using_fallback: msg += " This occurred with SAMPLE HTML."
            print(f"Warning: {msg}")
            return []

        print("Found security notices table. Extracting data...")
        body = table.find('tbody')
        data_rows = body.find_all('tr') if body else []
        if not data_rows: # Fallback if no tbody, but table exists (e.g. rows directly in table)
            header = table.find('thead')
            all_rows_in_table = table.find_all('tr')
            if header:
                data_rows = [row for row in all_rows_in_table if row not in header.find_all('tr')]
            elif all_rows_in_table:
                 data_rows = all_rows_in_table[1:] # Assume first is header
            else:
                print("Warning: Table found, but no data rows identified.")
                return []

        for row_idx, row in enumerate(data_rows):
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 4:
                try:
                    vuln_cell = cells[0]
                    vuln_link_tag = vuln_cell.find('a')
                    vuln_title = vuln_link_tag.get_text(strip=True) if vuln_link_tag else vuln_cell.get_text(strip=True)
                    vuln_link_raw = vuln_link_tag['href'] if vuln_link_tag and vuln_link_tag.has_attr('href') else None
                    vuln_link = ("https://www.bluetooth.com" + vuln_link_raw) if vuln_link_raw and vuln_link_raw.startswith('/') else vuln_link_raw

                    date_str = cells[1].get_text(strip=True)
                    affected_specs = cells[2].get_text(strip=True)

                    cve_cell = cells[3]
                    cve_link_tag = cve_cell.find('a')
                    cve_id = cve_link_tag.get_text(strip=True) if cve_link_tag else cve_cell.get_text(strip=True)
                    cve_link = cve_link_tag['href'] if cve_link_tag and cve_link_tag.has_attr('href') else None

                    notices.append({
                        "title": vuln_title, "date": date_str, "link": vuln_link,
                        "affected_specs": affected_specs, "cve_id": cve_id, "cve_link": cve_link
                    })
                except Exception as cell_e:
                    print(f"Error parsing cells in row {row_idx} for security notices: {cell_e}. Row: {row.get_text(strip=True,separator='|')}")
            elif cells: # If row has cells but not enough
                 print(f"Warning: Row {row_idx} in security table does not have enough cells (expected >=4, got {len(cells)}). Content: {row.get_text(strip=True,separator='|')}")


        if notices: print(f"Successfully parsed {len(notices)} security notices.")
        else:
            msg = "Found table but could not parse any security notices."
            if using_fallback: msg += " This occurred with SAMPLE HTML."
            print(f"Warning: {msg}")

    except Exception as e:
        msg = f"An error occurred during HTML parsing of security notices: {e}"
        if using_fallback: msg += " This occurred while parsing the SAMPLE HTML."
        print(msg)
        return []
    return notices

# --- nRF Specific Security Advisories (Placeholder) ---
def fetch_nrf_security_advisories():
    """
    Returns a hardcoded list of sample nRF-specific security advisories.
    In a real-world scenario, this could fetch from a regularly updated CSV, JSON,
    or a dedicated API if available.
    """
    print("INFO: Using hardcoded sample data for nRF Security Advisories.")
    sample_advisories = [
        {
            "cve_id": "CVE-2023-12345", # Example, not a real CVE
            "product_series": "nRF52 Series",
            "summary": "A potential vulnerability in the Foobar peripheral allowing baz overflow.",
            "link": "https://www.nordicsemi.com/Products/Security/Advisory/NRFSEC-2023-001"
        },
        {
            "cve_id": "CVE-2023-67890",
            "product_series": "nRF53 Series", # For matching
            "summary": "Timing attack possible on the Qux crypto engine under specific conditions.",
            "link": "https://www.nordicsemi.com/Products/Security/Advisory/NRFSEC-2023-002"
        },
        {
            "cve_id": "CVE-2022-54321",
            "product_series": "nRF91 Series",
            "summary": "Modem firmware update required to address issue XYZ.",
            "link": "https://www.nordicsemi.com/Products/Security/Advisory/NRFSEC-2022-005"
        }
    ]
    return sample_advisories

if __name__ == '__main__':
    print("--- Testing data_ingestion.py ---")

    print("\n--- Testing fetch_assigned_numbers_data ---")
    assigned_numbers = fetch_assigned_numbers_data()
    if assigned_numbers.get("company_identifiers"):
        print("\nSample Company Identifiers (first 3 from fallback/loaded):")
        for item in assigned_numbers["company_identifiers"][:3]: # Print up to 3
            print(f"  Value: {item.get('value')}, Name: {item.get('name')}")
    else:
        print("\nNo Company Identifiers data loaded.")

    if assigned_numbers.get("service_uuids"):
        print("\nSample Service UUIDs (first 3 from fallback/loaded):")
        for item in assigned_numbers["service_uuids"][:3]: # Print up to 3
            print(f"  UUID: {item.get('uuid')}, Name: {item.get('name')}")
    else:
        print("\nNo Service UUIDs data loaded.")

    if assigned_numbers.get("protocol_identifiers"):
        print("\nSample Protocol Identifiers (first 3 from fallback/loaded):")
        for item in assigned_numbers["protocol_identifiers"][:3]: # Print up to 3
            print(f"  UUID: {item.get('uuid')}, Name: {item.get('name')}")
    else:
        print("\nNo Protocol Identifiers data loaded.")

    print("\n--- Testing fetch_sig_security_notices ---")
    security_notices = fetch_sig_security_notices()
    if security_notices:
        print("\nSample Security Notices (first 2):")
        for notice in security_notices[:2]:
            print(f"  Title: {notice.get('title')}")
            print(f"    Date: {notice.get('date')}")
            print(f"    Link: {notice.get('link')}")
            print(f"    Affected: {notice.get('affected_specs')}")
            print(f"    CVE: {notice.get('cve_id')} ({notice.get('cve_link')})")
    else:
        print("\nNo Security Notices data loaded or an error occurred.")

    print("\n--- Testing fetch_nrf_security_advisories ---")
    nrf_advisories = fetch_nrf_security_advisories()
    if nrf_advisories:
        print(f"\nLoaded {len(nrf_advisories)} nRF Security Advisories (sample data):")
        for advisory in nrf_advisories:
            print(f"  CVE: {advisory.get('cve_id')}, Product: {advisory.get('product_series')}, Summary: {advisory.get('summary')}")
    else:
        print("\nNo nRF Security Advisories loaded (this would be unexpected for sample data).")

    print("\n--- Testing complete ---")
