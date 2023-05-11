"""
LLDP information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    lldp
        Collects LLDP information about connected devices

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def interfaces():
    """
    Collects LLDP information about connected devices
    Includes local interface, MAC, system, port name, IP address, vendor,
        description, model, and serial number

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    lldp : dict
        Dictionary containing LLDP information
    """

    lldp = {
        "interfaces": [
            {
                "name": "ge-0/0/0",
                "mac": "18:66:da:3f:f2:aa",
                "system": "WAP-1",
                "port_name": "ETH0",
                "ip": "10.1.1.1",
                "vendor": "Mist Systems.",
                "description": "Mist Systems 802.11ax Access Point.",
                "model": "AP43-WW",
                "serial": "Axxxxxxx"
            },
            {
                "name": "ge-0/0/1",
                "mac": "18:66:da:3f:f2:ab",
                "system": "WAP-2",
                "port_name": "ETH0",
                "ip": "10.1.1.2",
                "vendor": "Mist Systems.",
                "description": "Mist Systems 802.11ax Access Point.",
                "model": "AP43-WW",
                "serial": "Axxxxxxx"
            }
        ]
    }

    return lldp


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
