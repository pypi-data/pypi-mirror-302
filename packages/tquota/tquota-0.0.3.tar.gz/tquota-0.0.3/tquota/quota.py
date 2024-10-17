# -*- coding: utf-8 -*-
"""
==========================================================
        Quota Monitoring for Cloud Environments
==========================================================

Created on:    Tue May 11, 2021, 13:00:30
Last updated:  Wed Oct 16, 2024, 13:00:30

Author:        Abdussalam Aljbri
Emails:        mr.aljbri@gmail.com, mr.aljbri@qq.com
Project GitHub: https://github.com/aljbri/tquota
Version:       0.0.2
License:       MIT License

Description:
-------------
This script implements the `Quota` class, designed to monitor and manage session time limits in cloud environments
like Kaggle or Colab with quota restrictions. It helps in tracking session time and takes action based on predefined
quota and buffer times (gap times). The class provides automatic adjustment of gap times based on average execution
time during operation.

Change Log:
-----------
v0.0.2 - Updated on Wed Oct 16, 2024
  - Introduced dynamic gap time (`auto` option) based on average execution times.
  - Added logging functionality to log remaining time.
  - Improved time validation to handle improper inputs.
  - Enhanced time format support, now allowing conversions from strings like '1h', '30m', '5s'.
  - Refactored internal code structure for readability.
  - Introduced automatic performance monitoring to calculate execution time per loop iteration.

v0.0.1 - Initial implementation (Tue May 11, 2021)
  - Basic `Quota` class to track remaining session time.
  - Static gap time support.
  - Basic time formatting and conversion.

Usage:
------
For usage examples, refer to the class-level docstring of `Quota`.
"""

import re
import logging
from timeit import default_timer


class Quota:
    """
    Monitors session time limits in cloud environments with quota limitations (e.g., Kaggle, Colab).

    This class allows users to set a quota time and a gap time, with options for automatic gap time adjustment
    based on the average execution time of operations within a loop. It can log remaining time and check if
    the time limits are reached.

    Time Format:
        The time format must be passed as a string combining digits and a single character representing the time unit:
        - 's' for seconds
        - 'm' for minutes
        - 'h' for hours
        - 'd' for days

        Examples:
        - '30s' for 30 seconds
        - '5m' for 5 minutes
        - '2h' for 2 hours
        - '1d' for 1 day

        If an invalid format is provided, a ValueError will be raised.

    Parameters:
    -----------
    - quota_time (str):
            Time quota for the session (e.g., '1h' for 1 hour, '30m' for 30 minutes).
            This is initially provided as a string and is internally converted to seconds.
            Default is '6h'.
    - gap_time (str):
            Time buffer before the quota ends to trigger actions.
            Set to 'auto' for automatic detection based on average execution time.
            Internally converted to seconds.
            Default is 'auto'.
    - enable_logging (bool, optional):
            Whether to enable logging or not. Default is False.

    Raises:
    -----------
    - ValueError:
            - If the `quota_time` or `gap_time` format is invalid. This occurs when the time strings are not formatted correctly
              (e.g., not containing valid time units like 's', 'm', 'h', 'd').
            - If the `quota_time` is less than or equal to zero. A quota time must be a positive value in seconds.
            - If the `gap_time` is greater than or equal to the `quota_time`. The gap time should be smaller than the quota time to make sense.
    - TypeError:
            - If a non-string value is provided for `quota_time` or `gap_time`. Both `quota_time` and `gap_time` must be strings to be processed.
    - AttributeError:
            - If an attempt is made to access properties or methods without proper initialization of internal values (such as accessing `execution_times` before an operation).

    Properties:
    -----------
    - start_time: The timestamp when the `Quota` instance is initialized (in seconds from `default_timer`).
    - quota_time: Total session quota time in seconds, converted from the input string (e.g., '1h' → 3600).
    - auto_gap_time: Flag to indicate whether gap time is set to 'auto', allowing dynamic adjustment.
    - gap_time: The buffer time before the quota ends. Can be statically set (manual time in seconds) or dynamically adjusted if 'auto'.
    - enable_logging: Whether to log the remaining time to the console.
    - execution_times: List of execution times (in seconds) for each loop iteration, used to calculate average execution time.
    - total_execution_time: The sum of all execution times, used for calculating the dynamic gap time.
    - last_execution_time: Timestamp of the last completed loop iteration (in seconds).
    """

    def __init__(self, quota_time='6h', gap_time='auto', enable_logging=False):
        self.start_time = default_timer()
        self.quota_time = self._to_seconds(quota_time)

        # Initialize gap time based on input, either as seconds or 0.0001 if 'auto'.
        self.auto_gap_time = gap_time in ['a', 'auto']
        self.gap_time = 0.0001 if self.auto_gap_time else self._to_seconds(gap_time)

        # Validate times
        self._validate_times()

        # Initialize logging if enabled
        self.enable_logging = enable_logging
        if self.enable_logging:
            logging.basicConfig(level=logging.INFO)

        # Initialize execution times tracker.
        self.execution_times = []  # To track execution times
        self.total_execution_time = 0.0  # To accumulate execution times
        self.last_execution_time = default_timer()  # Initialize last execution time

    def hastime(self):
        """
        Checks if the session still has time before the gap time is reached.

        Returns:
        -------
            bool: True if there is enough time left in the session, False otherwise.
        """
        self._update_gap_time()  # Update gap time based on execution history
        elapsed_time = self._remaining_time()
        return elapsed_time >= self.gap_time

    def time_up(self):
        """
        Checks if the session has reached or exceeded the quota time.

        Returns:
        -------
            bool: True if the quota time has been exceeded, False otherwise.
        """
        self._update_gap_time()  # Update gap time based on execution history
        remained_time = self._remaining_time()
        return remained_time < self.gap_time

    def remaining_time(self):
        """
        Returns the remaining time in a human-readable format.

        Returns:
        -------
            str: Remaining time formatted as "xh:xm:xs".
        """
        return self._format_time(self._remaining_time())

    def log_remaining_time(self):
        """
        Logs the remaining time to the console if logging is enabled.

        Logs:
        ----
            str: Remaining time message if logging is enabled.
        """
        if self.enable_logging:
            logging.info("Remaining time before quota is reached: {}".format(self.remaining_time()))

    def _remaining_time(self):
        """
        Calculates the remaining time in seconds.

        Returns:
            int: Remaining time in seconds.
        """
        elapsed_time = self.quota_time - (default_timer() - self.start_time)
        return max(elapsed_time, 0)

    def _to_seconds(self, wTime):
        """
        Converts a time string into seconds (e.g., '1h' -> 3600).

        Args:
            wTime: A string representing the time in the format '1h', '30m', '5s', etc.

        Returns:
            float: Time in seconds.

        Raises:
            ValueError: If the time format is invalid.
        """
        pattern = r'^(\d+)([smhd])$'
        match = re.match(pattern, wTime.lower())
        if not match:
            raise ValueError("Invalid time format: '{}'. Use format like '1h', '30m', '5s'.".format(wTime))

        time_value, unit = match.groups()
        time_value = int(time_value)
        unit_seconds = {'s': 1, 'm': 60, 'h': 3600, 'd': 86400}

        if time_value <= 0:
            raise ValueError("Time value must be greater than zero: '{}'".format(wTime))

        return time_value * unit_seconds[unit]

    def _format_time(self, seconds):
        """
        Converts seconds into a human-readable time format.

        Args:
            seconds: Time in seconds.

        Returns:
            str: A human-readable time string in the format "Xh Xm Xs".
        """
        h, rem = divmod(seconds, 3600)
        m, s = divmod(rem, 60)
        return "{}h:{}m:{}s".format(int(h), int(m), int(s))

    def _validate_times(self):
        """
        Validates that the quota time and gap time are logically consistent.

        Raises:
            ValueError: If gap time >= quota time or if either time is <= 0.
        """
        if self.gap_time >= self.quota_time:
            raise ValueError("Gap time must be smaller than the quota time.")
        if self.quota_time <= 0:
            raise ValueError("Quota time must be greater than 0.")
        if self.gap_time <= 0:
            raise ValueError("Gap time must be greater than 0.")

    def _update_gap_time(self):
        """
        Updates the gap time dynamically based on the average execution time, if `auto` mode is enabled.

        It calculates the time taken since the last operation and updates the gap time accordingly.
        """
        current_time = default_timer()  # Get the current time
        execution_time = current_time - self.last_execution_time  # Calculate time since last update
        self.execution_times.append(execution_time)  # Record the execution time
        self.total_execution_time += execution_time  # Update total execution time

        # Update gap_time to average execution time if set to 'auto' and there are recorded times
        if self.auto_gap_time and self.execution_times:
            execution_time_average = self.total_execution_time / len(self.execution_times)
            self.gap_time = execution_time_average  # Set gap_time to average in seconds

        self.last_execution_time = current_time  # Update the last execution time for the next call

    def _default_action(self):
        """
        Default action to take when the quota time is up.

        Currently, this just logs a message if logging is enabled, but can be extended for future functionality.
        """
        if self.enable_logging:
            logging.info("Quota time reached. Executing default action.")
