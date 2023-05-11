"""
MAC address table information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    mac_table
        Collect MAC address table information from Juniper devices

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def mac_table():
    """
    Collect MAC address table information from Juniper devices
    Including MAC address, VLAN, and interface

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    mac : dict
        Dictionary containing template information
    """

    mac = {
        "entry": [
            {
                "mac": "00:00:00:00:00:00",
                "vlan": "Workstations",
                "interface": "ge-0/0/0"
            },
            {
                "mac": "00:00:00:00:00:01",
                "vlan": "Workstations",
                "interface": "ge-0/0/01"
            }
        ]
    }

    return mac


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
