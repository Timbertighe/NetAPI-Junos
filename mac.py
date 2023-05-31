"""
MAC address table information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Mac
        Collect MAC address table information from Juniper devices

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


import traceback as tb

import netconf


class Mac:
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
    mac()
        Collect MAC address table information from Juniper devices
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
        self.mac_table = None

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

            # Collect MAC address table information
            self.mac_table = connection.rpc_commands(
                'get-ethernet-switching-table-information'
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

    def mac(self):
        """
        Collect MAC address table information from Juniper devices

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
            "entry": []
        }

        # Handle newer and older versions of Junos
        #   Newer versions have a different structure
        if 'l2ng-l2ald-rtb-macdb' in self.mac_table:

            # Get the MAC address table, if one exists
            #   Routers don't have MAC address table entries, only ARP
            if self.mac_table['l2ng-l2ald-rtb-macdb'] is not None:
                mac_table = (
                    self.mac_table
                    ['l2ng-l2ald-rtb-macdb']
                    ['l2ng-l2ald-mac-entry-vlan']
                    ['l2ng-mac-entry']
                )

                # Loop through the MAC address table and add to the dictionary
                for address in mac_table:
                    entry = {}
                    entry['mac'] = address['l2ng-l2-mac-address']
                    entry['vlan'] = address['l2ng-l2-mac-vlan-name']
                    entry['interface'] = (
                        address['l2ng-l2-mac-logical-interface']
                    )
                    my_dict['entry'].append(entry)

        # Older versions have a different structure
        elif 'ethernet-switching-table-information' in self.mac_table:
            mac_table = (
                self.mac_table
                ['ethernet-switching-table-information']
                ['ethernet-switching-table']
                ['mac-table-entry']
            )

            # Loop through the MAC address table and add to the dictionary
            for address in mac_table:
                entry = {}
                entry['mac'] = address['mac-address']
                entry['vlan'] = address['mac-vlan']
                entry['interface'] = (
                    address['mac-interfaces-list']['mac-interfaces']
                )
                my_dict['entry'].append(entry)

        return my_dict


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
