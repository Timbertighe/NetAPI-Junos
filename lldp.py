"""
LLDP information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Lldp
        Connect to a Junos device and collect LLDP information

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


import traceback as tb

import netconf


class Lldp:
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
    interfaces()
        Collects LLDP information about connected devices
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
        self.lldp_interface = None

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

        # Connect to device, collect LLDP information
        with netconf.Netconf(
            host=self.host,
            user=self.user,
            password=self.password
        ) as connection:
            # If there was a failure to connect, return
            if connection.dev is None:
                return

            # Collect LLDP information
            try:
                self.lldp_interface = connection.rpc_commands(
                    'get-lldp-neighbor-detail-information',
                )

            # Some junos versions do not support the 'detail' keyword
            except Exception:
                print("Old junos version, using non-detailed LLDP")
                self.lldp_interface = connection.rpc_commands(
                    'get-lldp-neighbors-information'
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

    def interfaces(self):
        """
        Collect detailed LLDP information from Juniper devices

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

        print('DEBUG #1')

        my_dict = {
            "interfaces": []
        }

        print(self.lldp_interface)

        lldp_ints = (
            self.lldp_interface
            ['lldp-neighbors-information']
            ['lldp-neighbor-information']
        )

        print(lldp_ints)

        if type(lldp_ints) is not list:
            lldp_ints = [lldp_ints]

        print('DEBUG #2')

        # Iterate through each interface
        for interface in lldp_ints:
            # Creating an empty dictionary, as not all these keys
            #   will be present
            entry = {
                'name': '',
                'mac': '',
                'system': '',
                'ip': '',
                'vendor': '',
                'description': '',
                'model': '',
                'serial': ''
            }

            if 'lldp-local-interface' in interface:
                entry['name'] = interface['lldp-local-interface']

            if 'lldp-remote-chassis-id' in interface:
                entry['mac'] = interface['lldp-remote-chassis-id']

            if 'lldp-remote-system-name' in interface:
                entry['system'] = interface['lldp-remote-system-name']

            if 'lldp-remote-management-address' in interface:
                entry['ip'] = interface['lldp-remote-management-address']

            if 'lldp-remote-inventory-manufacturer-name' in interface:
                entry['vendor'] = (
                    interface['lldp-remote-inventory-manufacturer-name']
                )

            if 'lldp-remote-port-description' in interface:
                entry['description'] = (
                    interface['lldp-remote-port-description']
                )

            if 'lldp-system-description' in interface:
                entry['model'] = (
                    interface
                    ['lldp-system-description']
                    ['lldp-remote-system-description']
                )

            if 'lldp-remote-inventory-serial-number' in interface:
                entry['serial'] = (
                    interface['lldp-remote-inventory-serial-number']
                )

            my_dict['interfaces'].append(entry)

        return my_dict


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
