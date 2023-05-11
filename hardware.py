"""
Hardware information for Juniper devices

NOTE: This only returns dummy data at the moment

Modules:
    3rd Party: None
    Internal: None

Classes:

    None

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


def cpu():
    """
    Collect CPU usage information
    Used, idle, 1 min average, 5 min average, 15 min average

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    cpu : dict
        Dictionary containing CPU usage information
    """

    cpu = {
        "cpu": {
            "used": 10,
            "idle": 90,
            "1_min": 5,
            "5_min": 1,
            "1_5min": 1
        }
    }

    return cpu


def memory():
    """
    Collect memory usage information
    Total memory, used memory

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    mem : dict
        Dictionary containing memory usage information
    """

    mem = {
        "memory": {
            "total": 1024,
            "used": 100,
        }
    }

    return mem


def disk():
    """
    Collect disk usage information
    A list of disks, containing the disk name, size and used space

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    disk : dict
        Dictionary containing disk usage information
    """

    disk = {
        "disk": [
            {
                "disk": "/dev/da1s1a",
                "size": 1024,
                "used": 100
            },
            {
                "disk": "/dev/da0s1a",
                "size": 2048,
                "used": 512
            },
        ]
    }

    return disk


def temperature():
    """
    Collect temperature information
    CPU temperature, and chassis temperature

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    temp : dict
        Dictionary containing temperature information
    """

    temp = {
        "temperature": {
            "cpu": 50,
            "chassis": 30
        }
    }

    return temp


def fan():
    """
    Collect fan information
    A list of fans, containing the fan name, speed and status

    Parameters
    ----------
    None

    Raises
    ------
    None

    Returns
    -------
    fans : dict
        Dictionary containing fan information
    """

    fans = {
        "fan": [
            {
                "fan": "fan0",
                "status": "ok",
                "rpm": 3840,
                "detail": "Normal"
            },
            {
                "fan": "fan1",
                "status": "ok",
                "rpm": 3743,
                "detail": "Normal"
            }
        ]
    }

    return fans


# Handle running as a script
if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run junos.py instead')
