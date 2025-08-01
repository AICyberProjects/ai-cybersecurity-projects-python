import os
import time
import pandas as pd

# --- Folder Structure ---
BASE_DIR = "chapter8_siem_log_analysis"
LOG_DIR = os.path.join(BASE_DIR, "logs")
QUERY_DIR = os.path.join(BASE_DIR, "detection_queries")
DASHBOARD_DIR = os.path.join(BASE_DIR, "dashboards")

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(QUERY_DIR, exist_ok=True)
os.makedirs(DASHBOARD_DIR, exist_ok=True)

# --- Step 1: Create Simulated Apache Access Log ---
def generate_apache_log():
    apache_log = """
192.168.1.5 - - [20/Jul/2025:14:10:01 -0700] "GET /login HTTP/1.1" 401 123
192.168.1.5 - - [20/Jul/2025:14:10:02 -0700] "GET /login HTTP/1.1" 401 123
192.168.1.5 - - [20/Jul/2025:14:10:03 -0700] "GET /login HTTP/1.1" 401 123
192.168.1.5 - - [20/Jul/2025:14:10:04 -0700] "GET /login HTTP/1.1" 401 123
192.168.1.5 - - [20/Jul/2025:14:10:05 -0700] "GET /admin HTTP/1.1" 401 123
192.168.2.9 - - [20/Jul/2025:14:15:01 -0700] "GET /home HTTP/1.1" 200 245
192.168.2.9 - - [20/Jul/2025:14:15:02 -0700] "GET /about HTTP/1.1" 200 198
    """.strip()

    with open(os.path.join(LOG_DIR, "apache_access.log"), "w") as f:
        f.write(apache_log)
    print("[✔] Apache access log created.")

# --- Step 2: Create Simulated Windows Event Log CSV ---
def generate_windows_events():
    data = {
        "TimeCreated": [
            "2025-07-20T14:00:01", "2025-07-20T14:01:05", "2025-07-20T14:02:12",
            "2025-07-20T14:04:19", "2025-07-20T14:05:00", "2025-07-20T14:06:30"
        ],
        "EventCode": [4625, 4625, 4625, 4625, 4625, 4624],
        "Account_Name": ["jdoe", "jdoe", "jdoe", "jdoe", "jdoe", "admin"],
        "Ip_Address": ["192.168.1.5"] * 6,
        "Message": [
            "Login failed", "Login failed", "Login failed",
            "Login failed", "Login failed", "Login successful"
        ]
    }

    df = pd.DataFrame(data)
    df.to_csv(os.path.join(LOG_DIR, "windows_events.csv"), index=False)
    print("[✔] Windows events CSV created.")

# --- Step 3: Save SPL Detection Queries ---
def save_spl_queries():
    queries = {
        "brute_force_search.spl": '''
sourcetype=access_combined uri_path="/login" OR uri_path="/admin"
| stats count by clientip, uri_path
| where count > 3
''',

        "port_scan_search.spl": '''
sourcetype=access_combined
| stats dc(uri_path) as unique_pages by clientip
| where unique_pages > 10
''',

        "failed_login_search.spl": '''
sourcetype=csv EventCode=4625
| stats count by Account_Name, Ip_Address
| where count > 4
'''
    }

    for filename, query in queries.items():
        with open(os.path.join(QUERY_DIR, filename), "w") as f:
            f.write(query.strip())
    print("SPL detection queries saved.")

# --- Step 4: Run All Setup Tasks ---
def setup_project():
    print("Setting up Chapter 8: SIEM Log Analysis Project...\n")
    generate_apache_log()
    generate_windows_events()
    save_spl_queries()
    print("Project folder is ready. Now open Splunk and ingest the logs manually.")

if __name__ == "__main__":
    setup_project()


