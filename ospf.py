"""
OSPF information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    ospf
        Collect OSPF information
    areas
        Collect OSPF area information
    neighbours
        Collect OSPF neighbour information
    interfaces
        Collect OSPF interface information

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def ospf():
    """
    Collect OSPF information
    Includes router ID, and reference bandwidth

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    ospf : dict
        Dictionary containing OSPF information
    """

    ospf = {
        "id": "10.250.1.1",
        "reference": "100g"
    }

    return ospf


def areas():
    """
    Collect OSPF area information
    Includes area ID, area type, authentication, and neighbours

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    areas : dict
        Dictionary containing OSPF area information
    """

    areas = {
        "areas": [
            {
                "id": "0.0.0.10",
                "type": "stub",
                "authentication": "none",
                "neighbors": 2
            },
            {
                "id": "0.0.0.0",
                "type": "normal",
                "authentication": "none",
                "neighbors": 4
            }
        ]
    }

    return areas


def neighbours():
    """
    Collect OSPF neighbour information
    Includes neighbour IP, state, interface, router ID, and area

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    neighbour : dict
        Dictionary containing OSPF neighbour information
    """

    neighbour = {
        "neighbor": [
            {
                "address": "172.16.1.1",
                "interface": "ge-0/0/0.0",
                "state": "full",
                "id": "10.250.1.1",
                "area": "0.0.0.10"
            },
            {
                "address": "172.16.2.2",
                "interface": "ge-0/0/1.0",
                "state": "full",
                "id": "10.250.2.1",
                "area": "0.0.0.0"
            }
        ]
    }

    return neighbour


def interfaces():
    """
    Collect OSPF interface information
    Includes interface name, state, area, neighbour count, mtu, cost, type,
        mask, authentication, and passive interface

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    interface : dict
        Dictionary containing OSPF interface information
    """

    interface = {
        "interface": [
            {
                "name": "ge-0/0/0.0",
                "state": "DROther",
                "area": "0.0.0.10",
                "neighbors": 0,
                "mtu": 1500,
                "cost": 10,
                "type": "broadcast",
                "mask": "255.255.255.0",
                "authentication": "none",
                "passive": False
            }
        ]
    }

    return interface


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
