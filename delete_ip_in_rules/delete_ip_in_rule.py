"""
This script deletes a ONE specific client IP from an export policy rule using the REST API.

If an export rule contains only one client IP, the rule is alo deleted along with this IP.
If the export rule contains multiple client IPs, only the specified IP is removed and the rule remains.

Tested with:
- NetApp ONTAP AFF 9.14.1
- Python 3.10 

Usage:
python3 delete_ip_in_rule.py <IP> <login> <password> <svm_name> <export_policy_name> <client_ip_delete>

Example:
python3 delete_ip_in_rule.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy 10.100.10.01
"""

import sys
import requests
import urllib3

urllib3.disable_warnings()

CLUSTER = sys.argv[1]
USERNAME = sys.argv[2]
PASSWORD = sys.argv[3]
SVM = sys.argv[4]
POLICY_NAME = sys.argv[5]
IP_TO_REMOVE = sys.argv[6]

BASE = f"https://{CLUSTER}/api"
AUTH = (USERNAME, PASSWORD)

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-Dot-SVM-Name": SVM
}

# Get export policy ID.
# ONTAP does not work with policy names internally, only IDs.
policy_url = f"{BASE}/protocols/nfs/export-policies?name={POLICY_NAME}"
r = requests.get(policy_url, auth=AUTH, headers=HEADERS, verify=False)
r.raise_for_status()

records = r.json().get("records", [])
if not records:
    print(f"Export policy '{POLICY_NAME}' not found")
    sys.exit(1)

policy_id = records[0]["id"]
print(f"Found policy ID: {policy_id}")

# List and get export rules.
rules_url = f"{BASE}/protocols/nfs/export-policies/{policy_id}/rules"
r = requests.get(rules_url, auth=AUTH, headers=HEADERS, verify=False)
r.raise_for_status()

rules = r.json().get("records", [])

found = False

for rule in rules:
    rule_index = rule["index"]
    rule_url = f"{BASE}/protocols/nfs/export-policies/{policy_id}/rules/{rule_index}"

    # Get full rule
    r = requests.get(rule_url, auth=AUTH, headers=HEADERS, verify=False)
    r.raise_for_status()
    rule_data = r.json()

    clients = rule_data.get("clients", [])
    matches = [c["match"] for c in clients if "match" in c]

    if IP_TO_REMOVE not in matches:
        continue

    found = True
    remaining = [c for c in clients if c.get("match") != IP_TO_REMOVE]

    if not remaining:
        # Delete rule
        d = requests.delete(rule_url, auth=AUTH, headers=HEADERS, verify=False)
        if d.status_code in (200, 202, 204):
            print(f"Deleted rule {rule_index} (last IP removed)")
        else:
            print(f"Failed to delete rule {rule_index}: {d.text}")
    else:
        # Patch rule
        payload = {"clients": remaining}
        p = requests.patch(rule_url, json=payload, auth=AUTH, headers=HEADERS, verify=False)
        if p.status_code in (200, 202):
            print(f"Updated rule {rule_index}, removed {IP_TO_REMOVE}")
        else:
            print(f"Failed to update rule {rule_index}: {p.text}")

if not found:
    print(f"No matching IP found in export rules.")

print("Done.")
