"""
VLAN information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    vlans
        Collect VLAN information from Juniper devices

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def vlans():
    """
    Collect VLAN information from Juniper devices
    Including VLAN ID, Name, description, irb

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    vlans : dict
        Dictionary containing VLAN information
    """

    vlans = {
        "vlans": [
            {
                "id": 25,
                "name": "Internet",
                "description": "Internet access for the public",
                "irb": "irb.25"
            },
            {
                "id": 30,
                "name": "Servers",
                "description": "Servers",
                "irb": "irb.30"
            }
        ]
    }

    return vlans


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
