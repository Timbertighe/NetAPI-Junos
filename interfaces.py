"""
Interface information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    interfaces
        Collect interface information from Juniper devices
        Includes PoE details

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def interfaces():
    """
    Collect interface information from Juniper devices
    Name, MAC, Description, Family, Address, Native VLAN, Speed,
        Counters, Subinterfaces
    PoE: Admin, Operational, Max Power, Power Used

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    int : dict
        Dictionary containing interface information
    """

    int = {
        "interfaces": [
            {
                "name": "ge-0/0/0",
                "mac": "4c:6d:58:39:69:a3",
                "description": "Workstations",
                "family": "",
                "address": "",
                "native_vlan": 1,
                "speed": 1000,
                "counters": {
                    "bps_in": 550800,
                    "bps_out": 682184,
                    "bytes_in": 4755699005,
                    "bytes_out": 629507153,
                    "pps_in": 51088,
                    "pps_out": 74936,
                    "packets_in": 3979923,
                    "packets_out": 2173825
                },
                "subinterfaces": [
                    {
                        "subinterface": "unit 0",
                        "family": "ethernet",
                        "address": "204",
                        "description": "Workstation"
                    }
                ],
                "poe": {
                    "admin": True,
                    "operational": True,
                    "max_power": 30,
                    "power_used": 20
                }
            },
            {
                "name": "ge-0/0/1",
                "mac": "4c:6d:58:39:69:a4",
                "description": "Workstations",
                "family": "",
                "address": "",
                "native_vlan": 1,
                "speed": 1000,
                "counters": {
                    "bps_in": 550800,
                    "bps_out": 682184,
                    "bytes_in": 4755699005,
                    "bytes_out": 629507153,
                    "pps_in": 51088,
                    "pps_out": 74936,
                    "packets_in": 3979923,
                    "packets_out": 2173825
                },
                "subinterfaces": [
                    {
                        "subinterface": "unit 0",
                        "family": "ethernet",
                        "address": "204",
                        "description": "Workstation"
                    }
                ],
                "poe": {
                    "admin": True,
                    "operational": True,
                    "max_power": 30,
                    "power_used": 20
                }
            }
        ]
    }

    return int


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
