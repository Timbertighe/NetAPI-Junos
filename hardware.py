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
            # If there was a failire to connect, return
            if connection.dev is None:
                return

            facts = connection.dev.facts
            model = facts['model']

            self.re = connection.rpc_commands(
                'get-route-engine-information'
            )
            self.storage = connection.rpc_commands(
                'get-system-storage'
            )

            # EX devices use 'get-environment-information'
            #   SRX devices use 'get-fan-information'
            if 'EX' in model:
                self.fans = connection.rpc_commands(
                    'get-environment-information'
                )
            else:
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

        cpu = {
            "cpu": []
        }

        # Get the routing information information
        #   Keep in mind there may be more than one RE
        engine = self.re['route-engine-information']['route-engine']
        if type(engine) is not list:
            engine = [engine]

        for rengine in engine:
            entry = {
                "used": 100 - int(rengine['cpu-idle']),
                "idle": int(rengine['cpu-idle']),
                "1_min": float(rengine['load-average-one']),
                "5_min": float(rengine['load-average-five']),
                "15min": float(rengine['load-average-fifteen'])
            }
            cpu['cpu'].append(entry)

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

        mem = {
            "memory": []
        }

        # Get the routing information information
        #   Keep in mind there may be more than one RE
        engine = self.re['route-engine-information']['route-engine']
        if type(engine) is not list:
            engine = [engine]

        for rengine in engine:
            entry = {}

            # Get the total memory
            #   Some devices use 'memory-dram-size',
            #   others use 'memory-system-total'
            if 'memory-dram-size' in rengine:
                entry['total'] = int(rengine['memory-dram-size'].split()[0])
            else:
                entry['total'] = int(rengine['memory-system-total'])

            # Get the used memory
            #   Some devices use 'memory-buffer-utilization',
            #   others use 'memory-system-total-used'
            if 'memory-buffer-utilization' in rengine:
                entry['used'] = int(rengine['memory-buffer-utilization'])
            else:
                entry['used'] = int(rengine['memory-system-total-used'])

            mem['memory'].append(entry)

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

        # Disk information is formatted differently for SRX and EX
        if 'system-storage-information' in self.storage:
            disk_list = (
                self.storage['system-storage-information']['filesystem']
            )
            for disk in disk_list:
                entry = {
                    "filesystem": []
                }
                entry_filesystem = {}
                entry_filesystem['disk'] = disk['filesystem-name']
                entry_filesystem['size'] = disk['total-blocks']['@format']
                entry_filesystem['used'] = disk['used-blocks']['@format']
                entry['filesystem'].append(entry_filesystem)

        else:
            disk_list = (
                self.storage
                ['multi-routing-engine-results']
                ['multi-routing-engine-item']
            )

            # This may or may not already be a list
            if type(disk_list) is not list:
                disk_list = [disk_list]

            for disk in disk_list:
                entry = {
                    "filesystem": []
                }
                for filesystem in (
                    disk['system-storage-information']['filesystem']
                ):
                    entry_filesystem = {}
                    entry_filesystem['disk'] = filesystem['filesystem-name']
                    entry_filesystem['size'] = (
                        filesystem['total-blocks']['@format']
                    )
                    entry_filesystem['used'] = (
                        filesystem['used-blocks']['@format']
                    )
                    entry['filesystem'].append(entry_filesystem)

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

        temp = {
            "temperature": []
        }

        # Get the routing information information
        #   Keep in mind there may be more than one RE
        engine = self.re['route-engine-information']['route-engine']
        if type(engine) is not list:
            engine = [engine]

        for rengine in engine:
            entry = {
                "cpu": int(rengine['cpu-temperature']['@celsius']),
                "chassis": int(rengine['temperature']['@celsius'])
            }
            temp['temperature'].append(entry)

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

        # Fan information is formatted differently for SRX and EX
        if 'environment-information' in self.fans:
            for item in (
                self.fans['environment-information']['environment-item']
            ):
                if item['class'] == 'Fans':
                    entry = {}
                    entry['fan'] = item['name']
                    entry['status'] = item['status']
                    entry['rpm'] = 'N/A'
                    entry['detail'] = item['comment']
                    fan['fan'].append(entry)

        # SRX formatting
        else:
            for item in (
                self.fans['fan-information']['fan-information-rpm-item']
            ):
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
