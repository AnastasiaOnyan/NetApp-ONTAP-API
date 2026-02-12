"""
This script deletes a NetApp ONTAP volume using the REST API netapp_ontap python library.

Tested with:
- NetApp ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

Usage:
python3 delete_volume.py <IP> <login> <password> <svm_name> <volume_name>

Example:
python3 delete_volume.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01
"""

import sys
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume
from netapp_ontap.error import NetAppRestError


# CLI arguments
HOST = sys.argv[1]
USER = sys.argv[2]
PASSWORD = sys.argv[3]
SVM_NAME = sys.argv[4]
VOLUME_NAME = sys.argv[5]


def delete_volume():
    try:
        with HostConnection(
            host=HOST,
            username=USER,
            password=PASSWORD,
            verify=False
        ):
            # Find the volume by name and SVM
            vol = Volume.find(name=VOLUME_NAME, svm=SVM_NAME)

            if not vol:
                print(f"Volume {VOLUME_NAME} not found.")
                return None

            print(f"Deleting volume '{VOLUME_NAME}' from SVM '{SVM_NAME}'...")

            # Delete the volume
            vol.delete()

            print(f"Delete request successfully sent for volume {VOLUME_NAME}.")

    except NetAppRestError as e:
        print("ONTAP REST error:", e)


# Execute immediately
delete_volume()
