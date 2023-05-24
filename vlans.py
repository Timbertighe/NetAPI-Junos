"""
VLAN information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

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


import traceback as tb

import netconf


class Vlan:
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
    example()
        An example method
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
            self.config = connection.get_config(
                filter=[
                    'vlans'
                ]
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

    def vlans(self):
        """
        An example method

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
            "vlans": []
        }

        # Collect VLAN information
        if 'vlans' in self.config:
            for vlan in self.config['configuration']['vlans']['vlan']:
                entry = {}
                entry['id'] = vlan['vlan-id']
                entry['name'] = vlan['name']

                if 'description' in vlan:
                    entry['description'] = vlan['description']
                else:
                    entry['description'] = ''

                if 'l3-interface' in vlan:
                    entry['irb'] = vlan['l3-interface']
                else:
                    entry['irb'] = None

                my_dict['vlans'].append(entry)

        return my_dict


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
