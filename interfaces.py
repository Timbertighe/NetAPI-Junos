"""
Interface information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Interfaces
        Connect to a Junos device and collect interface information

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


import traceback as tb

import netconf


class Interfaces:
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
        Collect interface information from Juniper devices
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
        self.interface_list = None
        self.poe = None

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

        # Connect to device, collect interface information
        with netconf.Netconf(
            host=self.host,
            user=self.user,
            password=self.password
        ) as connection:
            # If there was a failire to connect, return
            if connection.dev is None:
                return

            # Collect interface information
            self.interface_list = connection.rpc_commands(
                'get-interface-information'
            )

            # Not all devices support PoE
            #   Check the model number to see if it's a PoE device
            model = connection.dev.facts["model"]

            if 'P' in model:
                self.poe = connection.rpc_commands(
                    'get-poe-interface-information'
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
        Collect interface information from Juniper devices

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        int_list : dict
            Dictionary containing information
        """

        int_list = {
            "interfaces": []
        }

        for item in (
            self.interface_list['interface-information']['physical-interface']
        ):
            # Skip internal interfaces
            if item['name'] == 'gr-0/0/0':
                continue
            if item['name'] == 'ip-0/0/0':
                continue
            if item['name'] == 'lsq-0/0/0':
                continue
            if item['name'] == 'lt-0/0/0':
                continue
            if item['name'] == 'mt-0/0/0':
                continue
            if item['name'] == 'sp-0/0/0':
                continue
            if item['name'] == 'dl0':
                continue
            if item['name'] == 'esi':
                continue
            if item['name'] == 'fti0':
                continue
            if item['name'] == 'gre':
                continue
            if item['name'] == 'ipip':
                continue
            if item['name'] == 'jsrv':
                continue
            if item['name'] == 'lsi':
                continue
            if item['name'] == 'mtun':
                continue
            if item['name'] == 'pimd':
                continue
            if item['name'] == 'pime':
                continue
            if item['name'] == 'pp0':
                continue
            if item['name'] == 'ppd0':
                continue
            if item['name'] == 'ppe0':
                continue
            if item['name'] == 'rbeb':
                continue
            if item['name'] == 'tap':
                continue
            if item['name'] == 'vtep':
                continue
            if item['name'] == 'pfe-0/0/0':
                continue
            if item['name'] == 'pfh-0/0/0':
                continue
            if item['name'] == 'bme0':
                continue
            if item['name'] == 'cbp0':
                continue
            if item['name'] == 'pip0':
                continue

            entry = {}
            entry['name'] = item['name']

            # Get the MAC address if one exists
            if 'current-physical-address' in item:
                if '#text' in item['current-physical-address']:
                    entry['mac'] = item['current-physical-address']['#text']
                else:
                    entry['mac'] = item['current-physical-address']
            else:
                entry['mac'] = ''

            # Get the interface speed if one exists
            if 'speed' in item:
                entry['speed'] = item['speed']
            else:
                entry['speed'] = ''

            # Get the description if one exists
            if 'description' in item:
                entry['description'] = item['description']
            else:
                entry['description'] = ''

            # Get the address family (not configured on LAG interfaces)
            if 'address-family' in item:
                entry['family'] = item['address-family']['address-family-name']
            else:
                entry['family'] = ''

            # Get an IP address if one exists
            if entry['family'] == 'inet':
                mask = item['address-family']['ifa-destination']
                mask = mask.split('/')[1]
                ip_address = item['address-family']['ifa-local']
                entry['address'] = f"{ip_address}"/"{mask}"
            else:
                entry['address'] = ''

            # Get counters if they exist
            entry['counters'] = {}
            if 'traffic-statistics' in item:
                stats = item['traffic-statistics']
                if 'input-bps' in stats:
                    entry['counters']['bps_in'] = stats['input-bps']
                else:
                    entry['counters']['bps_in'] = 0

                if 'output-bps' in stats:
                    entry['counters']['bps_out'] = stats['output-bps']
                else:
                    entry['counters']['bps_out'] = 0

                if 'input-pps' in stats:
                    entry['counters']['pps_in'] = stats['input-pps']
                else:
                    entry['counters']['pps_in'] = 0

                if 'output-pps' in stats:
                    entry['counters']['pps_out'] = stats['output-pps']
                else:
                    entry['counters']['pps_out'] = 0

            # Get subinterface information if it exists
            entry['subinterfaces'] = []
            if 'logical-interface' in item:
                # If there is only one subinterface, it is not a list
                sub_interfaces = item['logical-interface']
                if type(sub_interfaces) is not list:
                    sub_interfaces = [sub_interfaces]

                for sub_interface in sub_interfaces:
                    sub = {}
                    sub['subinterface'] = sub_interface['name']
                    if 'address-family' in sub_interface:
                        sub_list = sub_interface['address-family']

                        # Sometimes there is only one address family,
                        #   sometimes there are many
                        # If there is only one address family, it is not a list
                        if type(sub_list) is not list:
                            sub_list = [sub_list]

                        # Create a list of address families
                        sub['family'] = []

                        # Iterate over the address families
                        for interface in sub_list:
                            int_entry = {}
                            int_entry['family'] = (
                                interface['address-family-name']
                            )

                            # Get a description if one exists
                            if 'description' in interface:
                                int_entry['description'] = (
                                    interface['description']
                                )
                            else:
                                int_entry['description'] = ''

                            # Get an IP address if one exists
                            if (
                                'family' in interface and
                                interface['family'] == 'inet'
                            ):
                                if 'ifa-destination' in interface(
                                    ['address-family']
                                ):
                                    mask = (
                                        interface
                                        ['address-family']
                                        ['ifa-destination']
                                    )
                                    mask = mask.split('/')[1]
                                    ip_address = (
                                        interface
                                        ['address-family']
                                        ['ifa-local']
                                    )
                                    int_entry['address'] = (
                                        f"{ip_address}"/"{mask}"
                                    )
                                else:
                                    int_entry['address'] = ''
                            else:
                                int_entry['address'] = ''

                            sub['family'].append(int_entry)

                    else:
                        sub['family'] = ''

                    # Put it all together
                    entry['subinterfaces'].append(sub)

            # Check for PoE
            if self.poe is not None:
                for poe in self.poe['poe']['interface-information']:
                    # Set empty values
                    entry['poe'] = {}
                    entry['poe']['admin'] = False
                    entry['poe']['operational'] = False
                    entry['poe']['max_power'] = False
                    entry['poe']['power_used'] = False

                    # Check for real values
                    if poe['interface-name'] == entry['name']:
                        # Convert to boolean
                        if poe['interface-enabled'] == 'Enabled':
                            entry['poe']['admin'] = True
                        else:
                            entry['poe']['admin'] = False

                        # Convert to boolean
                        if poe['interface-status'] == 'on':
                            entry['poe']['operational'] = True
                        else:
                            entry['poe']['operational'] = False

                        entry['poe']['max_power'] = (
                            poe['interface-power-limit']
                        )
                        entry['poe']['power_used'] = poe['interface-power']
                        continue

            # Put it all together
            int_list['interfaces'].append(entry)

        return int_list


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
