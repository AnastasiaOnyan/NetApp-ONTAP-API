"""
This script deletes an NFS export policy using the NetApp ONTAP REST API
via the netapp_ontap Python client library.

!!! AN IMPORTANT NOTE !!!
All volumes (and qtrees) that reference this export policy must be reassigned
to another export policy or deleted before the policy deletion is attempted.
There should be no export rules left which assigned to this policy.

Tested with:
- NetApp ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

Usage:
python3 delete_exp_policy.py <IP> <login> <password> <svm_name> <export_policy_name>

Example:
python3 delete_exp_policy.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01_policy
"""

import sys
from netapp_ontap import HostConnection
from netapp_ontap.resources import ExportPolicy
from netapp_ontap.error import NetAppRestError


# CLI arguments
HOST = sys.argv[1]
USER = sys.argv[2]
PASSWORD = sys.argv[3]
SVM_NAME = sys.argv[4]
EXPORT_POLICY_NAME = sys.argv[5]


def delete_export_policy():
    try:
        # Establishing connection to ONTAP.
        with HostConnection(
            host=HOST,
            username=USER,
            password=PASSWORD,
            # TLS cert verification is disabled.
            verify=False
        ):
            # Find export policy by name and SVM
            # GET /api/protocols/nfs/export-policies?name=<policy>&svm.name=<svm>
            policy = ExportPolicy.find(
                name=EXPORT_POLICY_NAME,
                svm=SVM_NAME
            )

            if not policy:
                print(f"Export policy '{EXPORT_POLICY_NAME}' not found.")
                return None

            print(
                f"Deleting export policy '{EXPORT_POLICY_NAME}' "
                f"from SVM '{SVM_NAME}'..."
            )

            # Delete export policy
            # DELETE /api/protocols/nfs/export-policies/{uuid}
            policy.delete()

            print(
                f"Delete request successfully sent for export policy "
                f"'{EXPORT_POLICY_NAME}'."
            )

    except NetAppRestError as e:
        print("ONTAP REST error:", e)


# Execute immediately
delete_export_policy()
