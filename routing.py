"""
Routing table information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

Functions

    routing_table
        Collect routing table information

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""


def routing_table():
    """
    Collect routing table information
    Includes routes, and next-hop information

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    routes : dict
        Dictionary containing template information
    """

    routes = {
        "entry": [
            {
                "route": "10.10.10.0/24",
                "next_hop": [
                    {
                        "hop": "172.16.1.1",
                        "protocol": "static/5",
                        "interface": "ge-0/0/0.0",
                        "metric": "0",
                        "active": True
                    }
                ]
            },
            {
                "route": "0.0.0.0/0",
                "next_hop": [
                    {
                        "hop": "172.16.1.2",
                        "protocol": "static/5",
                        "interface": "irb.10",
                        "metric": "100",
                        "active": True
                    }
                ]
            }
        ]
    }

    return routes


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
