"""
The Junos plugin for the Net-API framework

Modules:
    3rd Party: xmlrpc.server, json
    Internal: device, hardware, interfaces, lldp, vlans, mac, routing, ospf,
        netconf

Classes:

    None

Functions

    device_info
        Collect device information
    device_hardware
        Collect hardware information
    device_interfaces
        Collect interface information
    device_lldp
        Collect LLDP information
    device_vlans
        Collect vlan information
    device_mac
        Collect MAC table information
    device_routing
        Collect routing table information
    device_ospf
        Collect OSPF information
    rpc_server
        Start the XML-RPC server

Exceptions:

    None

Misc Variables:

    HOSTNAME : str
        Hostname to bind the XML-RPC server to
    PORT : int
        Port to bind the XML-RPC server to

Author:
    Luke Robertson - May 2023
"""

# External imports
from xmlrpc.server import SimpleXMLRPCServer
import json

# Internal imports
import device
import hardware
import interfaces
import lldp
import vlans
import mac
import routing
import ospf


# RPC settings
#   Use 'localhost' to only allow connections from the local machine
#   Update to an IP or FQDN to allow connections from other machines
HOSTNAME = 'localhost'
PORT = 8000


def device_info(host, user, password):
    """
    Collect device information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing device information
    """

    info = {}

    with device.Device(host=host, user=user, password=password) as my_device:
        info.update(my_device.facts())
        info.update(my_device.license())
        info.update(my_device.radius())
        info.update(my_device.syslog())
        info.update(my_device.ntp())
        info.update(my_device.dns())
        info.update(my_device.snmp())

    return json.dumps(info)


def device_hardware(host, user, password):
    """
    Collect hardware information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing device information
    """

    info = {}

    info.update(hardware.cpu())
    info.update(hardware.memory())
    info.update(hardware.disk())
    info.update(hardware.temperature())
    info.update(hardware.fan())

    return json.dumps(info)


def device_interfaces(host, user, password):
    """
    Collect interface information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing interface information
    """

    info = {}

    info.update(interfaces.interfaces())

    return json.dumps(info)


def device_lldp(host, user, password):
    """
    Collect LLDP information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing LLDP information
    """

    info = {}

    info.update(lldp.interfaces())

    return json.dumps(info)


def device_vlans(host, user, password):
    """
    Collect VLAN information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing VLAN information
    """

    info = {}

    info.update(vlans.vlans())

    return json.dumps(info)


def device_mac(host, user, password):
    """
    Collect MAC address table information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing MAC information
    """

    info = {}

    info.update(mac.mac_table())

    return json.dumps(info)


def device_routing(host, user, password):
    """
    Collect routing table information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing routing table information
    """

    info = {}

    info.update(routing.routing_table())

    return json.dumps(info)


def device_ospf(host, user, password):
    """
    Collect OSPF information

    Parameters
    ----------
    host : str
        Hostname or IP address of the device
    user : str
        Username to authenticate with
    password : str
        Password to authenticate with

    Raises
    ------
    None

    Returns
    -------
    info : json
        JSON formatted string containing OSPF information
    """

    info = {}

    info.update(ospf.ospf())
    info.update(ospf.areas())
    info.update(ospf.neighbours())
    info.update(ospf.interfaces())

    return json.dumps(info)


def rpc_server():
    """
    Start the XML-RPC server, and exposes functions to the client

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    None
    """

    # Create the server
    print('Starting server...')
    server = SimpleXMLRPCServer((HOSTNAME, PORT))

    # Register the functions
    server.register_function(device_info, 'device_info')
    server.register_function(device_hardware, 'hardware')
    server.register_function(device_interfaces, 'interfaces')
    server.register_function(device_lldp, 'lldp')
    server.register_function(device_vlans, 'vlans')
    server.register_function(device_mac, 'mac')
    server.register_function(device_routing, 'routing')
    server.register_function(device_ospf, 'ospf')

    # Start the server
    server.serve_forever()


# Run the server
if __name__ == '__main__':
    rpc_server()
