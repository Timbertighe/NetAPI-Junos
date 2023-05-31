"""
Get information about Junos devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: traceback
    Internal: netconf

Classes:

    Device
        Connect to a Junos device and collect information

Functions

    None

Exceptions:

    None

Misc Variables:

    RADIUS_TIMEOUT : int
        RADIUS server default timeout in seconds
    RADIUS_RETRIES : int
        RADIUS server default retries
    RADIUS_ACCPORT : int
        RADIUS server default accounting port

Author:
    Luke Robertson - May 2023
"""

import traceback as tb

import netconf


RADIUS_TIMEOUT = 5
RADIUS_RETRIES = 3
RADIUS_ACCPORT = 1813


class Device:
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
    facts()
        Get device facts, including hostname, serial, uptime, model, version
    license()
        Get license information, including license id, name, expiry
    radius()
        Get RADIUS server information, including server, timeout, retries
    syslog()
        Get syslog server information, including server, port, facility
    ntp()
        Get NTP server information, including server, version, authentication
    dns()
        Get DNS server information, including server, domain, search
    snmp()
        Get SNMP server information, including server, community, trap
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
        self.raw_license = None
        self.raw_config = None
        self.hostname = None
        self.serial = None
        self.model = None
        self.version = None
        self.uptime = None

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
            # If there was a failire to connect, return
            if connection.dev is None:
                return

            facts = connection.dev.facts

            self.raw_license = connection.rpc_commands(
                'get-license-information'
            )
            self.config = connection.get_config(
                filter=[
                    'system/radius-server',
                    'system/syslog/host',
                    'system/ntp',
                    'system/name-server',
                    'system/domain-name',
                    'snmp'
                ]
            )

            # Get the master RE
            #   This is needed as not all RE's report uptime
            '''
            BUG in PyEZ:
            If RE2 is the master, it will not be present in device facts
            Logged issue: https://github.com/Juniper/py-junos-eznc/issues/1251
            '''
            if facts['RE0'] is not None:
                master_re = 'RE0'
            elif facts['RE1'] is not None:
                master_re = 'RE1'
            elif facts['RE2'] is not None:
                master_re = 'RE2'
            else:
                master_re = 'RE3'

            # Extract uptime from the master RE
            uptime = facts[master_re]["up_time"].split(", ")
            days = 0
            hours = 0
            minutes = 0
            seconds = 0

            # The uptime string may not contain all these values
            #   Find if they exist, and extract them
            for item in uptime:
                if "days" in item:
                    days = item.split(" ")[0]
                elif "hours" in item:
                    hours = item.split(" ")[0]
                elif "minutes" in item:
                    minutes = item.split(" ")[0]
                elif "seconds" in item:
                    seconds = item.split(" ")[0]

            # Convert uptime to seconds
            uptime = int(days) * 86400
            uptime += int(hours) * 3600
            uptime += int(minutes) * 60
            uptime += int(seconds)

            # Get the rest of the device facts
            self.hostname = facts["hostname"]
            self.serial = facts["serialnumber"]
            self.model = facts["model"]
            self.version = facts["version"]
            self.uptime = uptime

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

    def facts(self):
        """
        Get device facts, including hostname, serial, uptime, model, version

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        facts : dict
            Dictionary containing device facts
        """

        facts = {
            "hostname": self.hostname,
            "serial": self.serial,
            "uptime": self.uptime,
            "model": self.model,
            "version": self.version
        }

        return facts

    def license(self):
        """
        Get license information, including license id, name, expiry

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        licenses : dict
            Dictionary containing license information
        """

        # If no licenses are installed, return None as the license id
        if 'no-licenses-installed' in self.raw_license['license-information']:
            licences = {
                "licenses": [
                    {
                        "lic_id": None,
                    }
                ]
            }

            return licences

        # Get license information
        #   If multiple licenses are installed, they will be in a list
        lic_list = []
        dev_licences = self.raw_license['license-information']['license']
        if type(dev_licences) is not list:
            dev_licences = [dev_licences]

        for licence in dev_licences:
            entry = {}
            entry['lic_id'] = licence['name']
            entry['name'] = []

            # If there is only one feature, it will not be in a list
            if type(licence['feature-block']['feature']) is list:
                features = licence['feature-block']['feature']
            else:
                features = [licence['feature-block']['feature']]

            # Get feature name and expiry
            for lic_feature in features:
                # print(lic_feature)
                entry['name'].append(lic_feature['name'])
                entry['expiry'] = \
                    lic_feature['validity-information']['end-date']['#text']

            lic_list.append(entry)

        # Return license information
        licences = {'licenses': lic_list}
        return licences

    def radius(self):
        """
        Get radius information, including server, port, acc port, timeout,
            retries, and source IP
        If there is config missing, use Junos defaults
        If there is no source IP, use an empty string

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        radius : dict
            Dictionary containing radius information
        """

        radius = {
            "radius-servers": []
        }

        # This may or may not be in list format
        #   If it is not, convert it to a list (so we can iterate over it)
        servers = self.config['configuration']['system']['radius-server']
        if type(servers) is not list:
            servers = [servers]

        # Build a dictionary of RADIUS information
        #   Some config may not be present, so use defaults
        for server in servers:
            entry = {}
            entry['server'] = server['name']
            entry['port'] = server['port']

            if 'accounting-port' in server:
                entry['acc_port'] = server['accounting-port']
            else:
                entry['acc_port'] = RADIUS_ACCPORT

            if 'timeout' in server:
                entry['timeout'] = server['timeout']
            else:
                entry['timeout'] = RADIUS_TIMEOUT

            if 'retry' in server:
                entry['retry'] = server['retry']
            else:
                entry['retry'] = RADIUS_RETRIES

            if 'source-address' in server:
                entry['source'] = server['source-address']
            else:
                entry['source'] = ''

            radius['radius-servers'].append(entry)

        return radius

    def syslog(self):
        """
        Get Syslog information, including server, facilities, level,
            source IP, and prefix

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        syslog : dict
            Dictionary containing Syslog information
        """

        # Build a dictionary of Syslog information
        syslog = {
            "syslog-servers": []
        }

        # Build a dictionary of Syslog information
        servers = self.config['configuration']['system']['syslog']['host']

        # This may or may not be in list format
        #   If it is not, convert it to a list (so we can iterate over it)
        if type(servers) is not list:
            servers = [servers]

        # Iterate over each server
        for server in servers:
            entry = {}
            entry['server'] = server['name']

            # Sometimes the 'contents' field will be a list
            #   Othertimes it is a dictionary
            if type(server['contents']) is list:
                entry['facilities'] = server['contents'][0]['name']
                syslog_levels = [key for key in server['contents'][0]]
                entry['level'] = syslog_levels[1]
            else:
                entry['facilities'] = server['contents']['name']
                syslog_levels = [key for key in server['contents']]
                entry['level'] = syslog_levels

            if 'source-address' in server:
                entry['source'] = server['source-address']
            else:
                entry['source'] = ''

            if 'log-prefix' in server:
                entry['prefix'] = server['log-prefix']
            else:
                entry['prefix'] = ''

            syslog['syslog-servers'].append(entry)

        return syslog

    def ntp(self):
        """
        Get NTP information, including server, and preferred server

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        ntp : dict
            Dictionary containing NTP information
        """

        # Build a dictionary of NTP information
        ntp = {
            "ntp-servers": []
        }

        # This may or may not be in list format
        #   If it is not, convert it to a list (so we can iterate over it)
        servers = self.config['configuration']['system']['ntp']['server']
        if type(servers) is not list:
            servers = [servers]

        for server in servers:
            entry = {}

            # Routing instances are not supported yet
            if 'routing-instance' in server:
                continue

            # Extract the server IP
            entry['server'] = server['name']

            # Figure out if this is a preferred server
            if 'prefer' in server:
                entry['prefer'] = server['prefer']
            else:
                entry['prefer'] = False

            # Add this server to the list
            ntp['ntp-servers'].append(entry)

        return ntp

    def dns(self):
        """
        Get DNS information, including server, source, domain

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        dns : dict
            Dictionary containing DNS information
        """

        # Build a dictionary of DNS information
        dns = {
            "dns-servers": {
                'domain': '',
                'servers': [
                    ]
            }
        }

        # Check if a domain name is configured
        if 'domain-name' in self.config['configuration']['system']:
            dns['dns-servers']['domain'] = \
                self.config['configuration']['system']['domain-name']

        # This may or may not be in list format
        #   If it is not, convert it to a list (so we can iterate over it)
        servers = self.config['configuration']['system']['name-server']
        if type(servers) is not list:
            servers = [servers]

        for server in servers:
            entry = {}

            # Extract the server IP
            entry['server'] = server['name']

            # Check if a source IP is configured
            if 'source-address' in server:
                entry['source'] = server['source-address']
            else:
                entry['source'] = False

            # Add this server to the list
            dns['dns-servers']['servers'].append(entry)

        return dns

    def snmp(self):
        """
        Get SNMP information, including name, contact, description,
            and communities

        Parameters
        ----------
        None

        Raises
        ------
        None

        Returns
        -------
        snmp : dict
            Dictionary containing SNMP information
        """

        # Build a dictionary of DNS information
        snmp = {
            "snmp": {
                'communities': [
                ]
            }
        }

        # Handle a case where there is no SNMP config at all
        if 'snmp' not in self.config['configuration']:
            return snmp

        # These may not be configured on all devices
        if 'name' in self.config['configuration']['snmp']:
            snmp['snmp']['name'] = self.config['configuration']['snmp']['name']
        else:
            snmp['snmp']['name'] = ''

        if 'contact' in self.config['configuration']['snmp']:
            snmp['snmp']['contact'] = \
                self.config['configuration']['snmp']['contact']
        else:
            snmp['snmp']['contact'] = ''

        if 'description' in self.config['configuration']['snmp']:
            snmp['snmp']['description'] = \
                self.config['configuration']['snmp']['description']
        else:
            snmp['snmp']['description'] = ''

        # This may or may not be in list format
        #   If it is not, convert it to a list (so we can iterate over it)
        servers = self.config['configuration']['snmp']['community']
        if type(servers) is not list:
            servers = [servers]

        for server in servers:
            entry = {}

            # Extract SNMP community information
            entry['community'] = server['name']

            if 'authorization' in server:
                entry['access'] = server['authorization']
            else:
                entry['access'] = ''

            # Get a list of SNMP clients
            client_list = []
            if 'clients' in server:
                for client in server['clients']:
                    client_list.append(client['name'])

            entry['clients'] = client_list

        snmp['snmp']['communities'].append(entry)

        return snmp


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
