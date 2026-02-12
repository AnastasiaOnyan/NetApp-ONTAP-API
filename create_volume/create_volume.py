"""
This script performs the following tasks on an NetApp ONTAP AFF cluster:
- Creates a new NFS volume with thick provisioning.
- Configures NFS export policy and rules for client IPs.
- Attaches the 'none' snapshot policy.
- Sets the snapshot reserve to 0% to avoid pre-allocating space for snapshots.
- Disables storage efficiency deduplication and compression.
- Hide .snapshot directory from clients.

Tested with:
- NetApp ONTAP 9.14.1
- Python 3.10 

Usage:
python3 create_volume.py <cluster_ip> <username> <password> <svm_name> <aggregate> <volume_name> <size_gb> <client_ips>

Example:
python3 create_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_10_SAS_1 dc0_d000_test_nfs_01 10 10.100.10.01 10.100.10.02
"""

import requests
import base64
import urllib3
import argparse
import time

"""Disable SSL warnings for self-signed certificates"""
urllib3.disable_warnings()

"""Parse arguments from bash command line. 
Use python3 create_volume.py --help to see which arguments must be given via Linux CLI."""
parser = argparse.ArgumentParser()

args_list = [
    ("cluster", "Cluster management IP"),
    ("username", "ONTAP username"),
    ("password", "ONTAP password"),
    ("svm_name", "An existing svm_name: dc5_d120"),
    ("aggregate", "An existing aggregate name: dc5_d120_01_SSD_1"),
    ("volume_name", "Volume name from a client: dc5_d120_smthng_nfs_01"),
    ("size_gb", "Volume size: 100"),
]

for arg, help_text in args_list:
    parser.add_argument(arg, help=help_text)
parser.add_argument("client_ips", nargs="+", help="Pass one or more client IP addresses, separated by spaces")
args = parser.parse_args()

CLUSTER = args.cluster
USERNAME = args.username
PASSWORD = args.password
SVM_NAME = args.svm_name
AGGR_NAME = args.aggregate
VOLUME_NAME = args.volume_name
SIZE_GB = int(args.size_gb)
# A list of client IPs allowed to access via NFS: ["00.0.000.00", "00.0.000.00"].
CLIENT_IPS = args.client_ips


"""Authentication and headers. base64 is encoding text into a Base64 string for HTTP headers 
(admin:NetApp123! --> YWRtaW46TmV0QXBwMTIzIQ==)."""
auth = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
headers = {
    # Adds base64 string to the request headers ("Authorization": "Basic YWRtaW46TmV0QXBwMTIzIQ==").
    "Authorization": f"Basic {auth}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    # Run API request inside the given svm.
    "X-Dot-SVM-Name": SVM_NAME
}

"""Create or get export policy."""
policy_name = f"{VOLUME_NAME}_policy"
policy_url = f"https://{CLUSTER}/api/protocols/nfs/export-policies"

resp = requests.post(policy_url, headers=headers, json={"name": policy_name}, verify=False)
if resp.status_code == 409:
    # Policy already exists so it skips creation
    print(f"Policy '{policy_name}' already exists. Using existing policy.")
elif resp.status_code not in (200, 201, 202):
    raise Exception(f"Failed to create export policy: {resp.text}")
else:
    print(f"✔️ Export policy '{policy_name}' created.")

"""Get policy UUID."""
resp = requests.get(f"{policy_url}?name={policy_name}", headers=headers, verify=False).json()
# Numeric internal ID for policy_id (instead of UUID).
records = resp.get("records", [])
if not records or "id" not in records[0]:
    raise Exception(f"Policy ID not returned by ONTAP. Response: {resp}")
# Policy_id is used to add rules and attach the volume.
policy_id = records[0]["id"]

"""Create export rules."""
rule_url = f"{policy_url}/{policy_id}/rules"
existing_rules = requests.get(rule_url, headers=headers, verify=False).json()
existing_ips = [
    r.get("clients", [{}])[0].get("match")
    for r in existing_rules.get("records", [])
    if "clients" in r and r["clients"]
]

for ip in CLIENT_IPS:
    if ip in existing_ips:
        continue

    rule_payload = {
        "clients": [{"match": ip}],
        "protocols": ["nfs"],
        "ro_rule": ["any"],
        "rw_rule": ["any"],
        "superuser": ["any"]
    }

    rule_resp = requests.post(rule_url, headers=headers, json=rule_payload, verify=False)
    if rule_resp.status_code not in (200, 201, 202):
        print(f"Failed to add rule for {ip}: {rule_resp.text}")
    else:
        print(f"Added export rule for {ip}")


"""Create volume."""
volume_url = f"https://{CLUSTER}/api/storage/volumes"
volume_payload = {
    "name": VOLUME_NAME,
    "aggregates": [{"name": AGGR_NAME}],
    # size in GB
    "size": SIZE_GB * 1024**3,
    # thick provisioning
    "guarantee": {"type": "volume"},
    "nas": {
        "path": f"/{VOLUME_NAME}",
        "export_policy": {"id": policy_id},
        "security_style": "unix"
    }
}

# Create volume (may be asynchronous).
vol_resp = requests.post(volume_url, headers=headers, json=volume_payload, verify=False)
print(f"Volume create response: {vol_resp.status_code} {vol_resp.json()}")
vol_resp_json = vol_resp.json()


if vol_resp.status_code == 202 and "job" in vol_resp_json:
    job_uuid = vol_resp_json["job"]["uuid"]
    job_url = f"https://{CLUSTER}/api/cluster/jobs/{job_uuid}"

    # ONTAP started a background job - wait for completion.
    while True:
        job_status = requests.get(job_url, headers=headers, verify=False).json()
        state = job_status.get("state")
        if state in ("success", "failure", "canceled"):
            break
        time.sleep(5)

    if state != "success":
        raise Exception(f"Volume creation job failed: {job_status}")
    print("Volume creation job completed.")
else:
    # Volume was created immediately.
    print("Volume created immediately (no job).")

# Get volume UUID by name.
vol_lookup = requests.get(f"{volume_url}?name={VOLUME_NAME}", headers=headers, verify=False).json()
vol_records = vol_lookup.get("records", [])
if not vol_records:
    raise Exception(f"Volume {VOLUME_NAME} not found after creation.")

vol_uuid = vol_records[0]["uuid"]

# Add polling for volume to be fully ready here.
while True:
    vol_status = requests.get(f"{volume_url}/{vol_uuid}", headers=headers, verify=False).json()
    vol_state = vol_status.get("state", "")
    if vol_state == "online":
        break
    time.sleep(5)
print("Volume is online and ready for efficiency changes.")


"""Attach the 'none' snapshot policy to the volume."""
snap_payload = {
    "snapshot_policy": {
        "name": "none"
    }
}

"""PATCH operations in ONTAP may run asynchronously (202 Accepted). Treat 200/201/202 as success."""
snap_resp = requests.patch(
    f"{volume_url}/{vol_uuid}",
    headers=headers,
    json=snap_payload,
    verify=False
)
if snap_resp.status_code not in (200, 201, 202):
    print(f"Failed to attach 'none' snapshot policy: {snap_resp.text}")
else:
    print(f"'none' snapshot policy attached. No snapshots will be taken for {VOLUME_NAME}")


final_payload = {

    # Snapshot copies (local) settings.
    "space": {
        "snapshot": {
            "reserve_percent": 0
        }
    },

    # Hide .snapshot directory from clients.
    "snapshot_directory_access_enabled": False,

    # Disable storage efficiency features.
    "efficiency": {
        "dedupe": "none",
        "cross_volume_dedupe": "none",
        "compression": "none"
    }
}

final_resp = requests.patch(
    f"https://{CLUSTER}/api/storage/volumes/{vol_uuid}",
    headers=headers,
    json=final_payload,
    verify=False
)

if final_resp.status_code in (200, 201, 202):
    print(f"Final volume settings applied successfully to {VOLUME_NAME}")
else:
    print(f"Failed to apply final volume settings: {final_resp.status_code} {final_resp.text}")
