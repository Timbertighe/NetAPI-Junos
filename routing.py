"""
Routing table information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Routing
        Collect routing information from Juniper devices

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


import traceback as tb

import netconf


class Routing:
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
    routing_table()
        Collect routing table information
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
        self.routing = None

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

            # Collect routing table information
            self.routing = connection.rpc_commands(
                'get-route-information'
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

    def routing_table(self):
        """
        Collect routing table information

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

        # Only supports the IPv4 Unicast table for now
        ipv4_table = None

        # This may be a list or a dictionary
        #   If it's a dictionary, convert it to a list
        table_list = self.routing['route-information']['route-table']
        if type(table_list) != list:
            table_list = [table_list]

        for table in table_list:
            if table['table-name'] == 'inet.0':
                ipv4_table = table['rt']
                break

        # Loop through the routes in the table
        for route in ipv4_table:

            destination = route['rt-destination']

            # Sometimes there is more than one entry (more than one protocol)
            route_entry = route['rt-entry']
            if type(route_entry) != list:
                route_entry = [route_entry]

            for specific_route in route_entry:
                entry = {}

                entry['protocol'] = specific_route['protocol-name']

                # Don't worry about internal routes
                if entry['protocol'] == 'Access-internal':
                    continue

                # Get the destination
                entry['route'] = destination

                # Some types don't have a metric listed
                if (
                    entry['protocol'] == 'Direct' or
                    entry['protocol'] == 'Local'
                ):
                    entry['metric'] = 0

                elif (
                    entry['protocol'] == 'Static'
                    and
                    'metric' not in specific_route
                ):
                    entry['metric'] = 1

                else:
                    entry['metric'] = specific_route['metric']

                # Get a list of next hops
                #   Some types don't have a next hop (eg, reject routes)
                if 'nh' in specific_route:
                    entry['next_hop'] = []
                    next_hop = specific_route['nh']
                    if type(next_hop) is not list:
                        next_hop = [next_hop]

                    # Loop through the next hops
                    for hop in next_hop:
                        hop_dict = {}

                        # Get the next-hop IP address
                        #   Some types don't have an IP address
                        if 'to' not in hop:
                            hop_dict['hop'] = None
                        else:
                            hop_dict['hop'] = hop['to']

                        # Get the next-hop interface
                        #   Some types don't have an interface
                        if 'via' not in hop:
                            hop_dict['interface'] = None
                        else:
                            hop_dict['interface'] = hop['via']

                        entry['next_hop'].append(hop_dict)

                my_dict['entry'].append(entry)

        return my_dict


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
