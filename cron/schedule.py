"""
Schedules tasks
    Tasks may run at a particular time, or at a particular interval

Modules:

    3rd Party: TBA
    Internal: TBA

Classes:

    Schedule
        Create an object to represent a scheduled task

Functions

    None

Exceptions:

    None

Misc Variables:

    None

Author:
    Luke Robertson - May 2023
"""

from apscheduler.triggers.interval import IntervalTrigger


class Schedule:
    """
    Create an object to represent a scheduled task
    Tasks may run at a particular time, or at a particular interval
    The task may be repeated, or run only once

    Attributes
    ----------
    TBA

    Methods
    -------
    __init__()
        Class constructor
    schedule_at()
        Schedule tasks to run at a particular time
    schedule_every()
        Schedule tasks to run at a particular interval
    start()
        Starts the scheduled task
    """

    def __init__(self, function, scheduler):
        """
        Class constructor

        Gets the request object from Flask and sets the attributes

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

        # Set the attributes
        self.function = function
        self.sched_obj = scheduler
        self.job_id = self.function.__name__
        self.job = None

    def schedule_at(self, time, **kwargs):
        """
        Schedule tasks to run at a particular time
        This will run once only, at the specified time

        Parameters:
            time : datetime
                The day/time to run the task

        Raises:
            None

        Returns:
            None
        """

        # Create the job
        self.sched_obj.add_job(
            func=self.function,
            trigger='date',
            run_date=time,
            id=self.function.__name__
        )

    def schedule_every(self, minutes):
        """
        Schedule tasks to run in x number of minutes, and repeat

        Parameters:
            minutes : int
                The number of minutes to wait before running the task

        Raises:
            None

        Returns:
            None
        """

        # Convert the time to a cron string
        interval = IntervalTrigger(minutes=minutes)

        # Schedule the task
        print("scheduling a job")
        self.job = self.sched_obj.add_job(
            func=self.function,
            trigger=interval,
            id=self.job_id
        )
        print(self.job)

    def start(self):
        """
        Starts the scheduled task

        Parameters:
            None

        Raises:
            None

        Returns:
            None
        """

        self.sched_obj.start()


if __name__ == '__main__':
    print('This module is not designed to be run as a script')
    print('Please run app.py instead')
