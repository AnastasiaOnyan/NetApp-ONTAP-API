"""
This script modifies an existing volume size using the NetApp ONTAP netapp_ontap Python client library.

Tested with:
- NetApp ONTAP AFF 9.14.1
- netapp_ontap Python client 9.17.1.0
- Python 3.10 

Usage:
python3 modify_vol_size.py <IP> <login> <password> <svm_name> <volume_name> <new_size>

Example:
python3 modify_vol_size.py 10.100.0.00 some_user "Disk@SomePassword" dc0_d000 dc0_d000_test_nfs_01 2GB
"""

import sys
from netapp_ontap import HostConnection
from netapp_ontap.resources import Volume
from netapp_ontap.error import NetAppRestError

"""CLI arguments. """
HOST = sys.argv[1]
USER = sys.argv[2]
PASSWORD = sys.argv[3]
SVM_NAME = sys.argv[4]
VOLUME_NAME = sys.argv[5]
# New size: "200GB" or "200" (bytes)
NEW_SIZE = sys.argv[6]


"""Connect to ONTAP and resize an existing volume."""
def resize_volume():
    try:
        with HostConnection(
            host=HOST,
            username=USER,
            password=PASSWORD,
            verify=False
        ):
            vol = Volume.find(name=VOLUME_NAME, svm=SVM_NAME)

            if not vol:
                print(f"Volume {VOLUME_NAME} not found.")
                return

            print(f"Current size: {vol.size}")

            vol.size = NEW_SIZE
            vol.patch()

            print(f"Successfully requested resize of {VOLUME_NAME} to {NEW_SIZE}.")

    except NetAppRestError as e:
        print("ONTAP REST error:", e)


resize_volume()
