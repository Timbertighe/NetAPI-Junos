"""
OSPF information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Ospf
        Collect OSPF information from Juniper devices

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


import traceback as tb

import netconf


class Ospf:
    """
    Connect to a Junos device and collect information

    Supports being instantiated with the 'with' statement

    Attributes
    ----------
    host : str
        IP address or FQDN of the device to connect to
    user : str
        Username to connect with
    password : str
        Password to connect with

    Methods
    -------
    __init__(host, user, password)
        Class constructor
    __enter__()
        Called when the 'with' statement is used
    __exit__(exc_type, exc_value, traceback)
        Called when the 'with' statement is finished
    ospf()
        Get general OSPF information
    areas()
        Get OSPF area information
    neighbours()
        Get OSPF neighbour information
    interfaces()
        Get OSPF interface information
    """

    def __init__(self, host, user, password):
        """
        Class constructor

        Parameters
        ----------
        host : str
            IP address or FQDN of the device to connect to
        user : str
            Username to connect with
        password : str
            Password to connect with

        Raises
        ------
        None

        Returns
        -------
        None
        """

        # Authentication information
        self.host = host
        self.user = user
        self.password = password

        # Device information
        self.config = None
        self.neighbour_info = None
        self.interface_info = None

    def __enter__(self):
        """
        Called when the 'with' statement is used

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            The instantiated object
        """

        # Connect to device, collect facts, license, and config
        with netconf.Netconf(
            host=self.host,
            user=self.user,
            password=self.password
        ) as connection:
            # If there was a failure to connect, return
            if connection.dev is None:
                return

            # Collect OSPF information
            self.overview = connection.rpc_commands(
                'get-ospf-overview-information'
            )

            # Check if OSPF is running
            if (
                'output' in self.overview and
                'not running' in self.overview['output']
            ):
                self.supported = False
            else:
                self.supported = True

                # Get OSPF configuration
                self.config = connection.get_config(
                    filter=[
                        'protocols/ospf',
                    ]
                )

                # Get neighbour and interface information
                self.neighbour_info = connection.rpc_commands(
                    'get-ospf-neighbor-information'
                )

                self.interface_info = connection.rpc_commands(
                    'get-ospf-interface-information'
                )

        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """
        Called when the 'with' statement is finished

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        self
            None
        """

        # handle errors that were raised
        if exc_type:
            print(
                f"Exception of type {exc_type.__name__} occurred: {exc_value}"
            )
            if traceback:
                print("Traceback:")
                print(tb.format_tb(traceback))

    def ospf(self):
        """
        Get general OSPF information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        my_dict : dict
            Dictionary containing information
        """

        if self.supported is False:
            return {
                "id": "",
                "reference": ""
            }

        # Get reference bandwidth, if one is configured
        if 'reference-bandwidth' in (
            self.config['configuration']['protocols']['ospf']
        ):
            bw = (
                self.config
                ['configuration']
                ['protocols']
                ['ospf']
                ['reference-bandwidth']
            )

        # If not configured, use default
        else:
            bw = '100mbps'

        # Build dictionary of information
        my_dict = {
            "id": (
                self.overview
                ['ospf-overview-information']
                ['ospf-overview']
                ['ospf-router-id']
            ),
            "reference": bw
        }

        return my_dict

    def areas(self):
        """
        Collect OSPF area information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        my_dict : dict
            Dictionary containing information
        """

        if self.supported is False:
            return {
                "areas": "",
            }

        my_dict = {
            "areas": []
        }

        # Get the list of areas from config
        areas = (
            self.overview
            ['ospf-overview-information']
            ['ospf-overview']
            ['ospf-area-overview']
        )

        # Make it a list
        if type(areas) is not list:
            areas = [areas]

        # For each area, get the information
        for area in areas:
            entry = {}
            entry['id'] = area['ospf-area']
            entry['type'] = area['ospf-stub-type']
            entry['authentication'] = area['authentication-type']
            entry['neighbors'] = area['ospf-nbr-overview']['ospf-nbr-up-count']
            my_dict['areas'].append(entry)

        return my_dict

    def neighbours(self):
        """
        Collect OSPF neighbour information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        my_dict : dict
            Dictionary containing information
        """

        if self.supported is False:
            return {
                "neighbor": ""
            }

        my_dict = {
            "neighbor": []
        }

        # Get a list of neighbours
        neighbour_list = (
            self.neighbour_info
            ['ospf-neighbor-information']
            ['ospf-neighbor']
        )

        # Make it a list if it isn't already
        if type(neighbour_list) is not list:
            neighbour_list = [neighbour_list]

        for neighbour in neighbour_list:
            entry = {}
            entry['address'] = neighbour['neighbor-address']
            entry['interface'] = neighbour['interface-name']
            entry['state'] = neighbour['ospf-neighbor-state']
            entry['id'] = neighbour['neighbor-id']
            my_dict['neighbor'].append(entry)

        return my_dict

    def interfaces(self):
        """
        Collect OSPF interface information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        my_dict : dict
            Dictionary containing information
        """

        my_dict = {
            "interface": []
        }

        if self.supported is False:
            return my_dict

        int_list = (
            self.interface_info
            ['ospf-interface-information']
            ['ospf-interface']
        )
        for interface in int_list:
            entry = {}
            entry['name'] = interface['interface-name']
            entry['state'] = interface['ospf-interface-state']
            entry['area'] = interface['ospf-area']
            entry['neighbors'] = interface['neighbor-count']
            my_dict['interface'].append(entry)

        return my_dict


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
