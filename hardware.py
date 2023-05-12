"""
Hardware information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Hardware
        Connect to a Junos device and collect hardware information

Functions

    cpu
        Collect CPU usage information
    memory
        Collect memory usage information
    disk
        Collect disk usage information
    temperature
        Collect temperature information
    fans
        Collect fan information

Exceptions:

    None

Misc Variables:

    TBA

Author:
    Luke Robertson - May 2023
"""

import traceback as tb

import netconf


class Hardware:
    """
    Connect to a Junos device and collect hardware information

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
    cpu()
        Collect CPU usage information
    memory()
        Collect memory usage information
    disk()
        Collect disk usage information
    temperature()
        Collect temperature information
    fans()
        Collect fan information
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

        # Hardware information
        self.re = None
        self.storage = None
        self.fans = None

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

        # Connect to device, collect hardware information
        with netconf.Netconf(
            host=self.host,
            user=self.user,
            password=self.password
        ) as connection:
            self.re = connection.rpc_commands(
                'get-route-engine-information'
            )
            self.storage = connection.rpc_commands(
                'get-system-storage'
            )
            self.fans = connection.rpc_commands(
                'get-fan-information'
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

    def cpu(self):
        """
        Collect CPU usage information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        cpu : dict
            Dictionary containing CPU information
        """

        engine = self.re['route-engine-information']['route-engine']
        cpu = {
            "cpu": {
                "used": 100 - int(engine['cpu-idle']),
                "idle": int(engine['cpu-idle']),
                "1_min": float(engine['load-average-one']),
                "5_min": float(engine['load-average-five']),
                "15min": float(engine['load-average-fifteen'])
            }
        }

        return cpu

    def memory(self):
        """
        Collect memory usage information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        memory : dict
            Dictionary containing information
        """

        engine = self.re['route-engine-information']['route-engine']

        mem = {
            "memory": {
                "total": int(engine['memory-system-total']),
                "used": int(engine['memory-system-total-used']),
            }
        }

        return mem

    def disk(self):
        """
        Collect disk usage information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        storage : dict
            Dictionary containing information
        """

        storage = {
            "disk": []
        }

        disk_list = self.storage['system-storage-information']['filesystem']
        entry = {}
        for disk in disk_list:
            entry['disk'] = disk['filesystem-name']
            entry['size'] = disk['total-blocks']['@format']
            entry['used'] = disk['used-blocks']['@format']
            storage['disk'].append(entry)

        return storage

    def temperature(self):
        """
        Collect temperature information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        temp : dict
            Dictionary containing information
        """

        engine = self.re['route-engine-information']['route-engine']

        temp = {
            "temperature": {
                "cpu": int(engine['cpu-temperature']['@celsius']),
                "chassis": int(engine['temperature']['@celsius'])
            }
        }

        return temp

    def fan(self):
        """
        Collect fan information

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        fan : dict
            Dictionary containing information
        """

        fan = {
            "fan": []
        }

        for item in self.fans['fan-information']['fan-information-rpm-item']:
            entry = {}
            entry['fan'] = item['name']
            entry['status'] = item['status']
            entry['rpm'] = item['rpm']
            entry['detail'] = item['comment']
            fan['fan'].append(entry)

        return fan


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
