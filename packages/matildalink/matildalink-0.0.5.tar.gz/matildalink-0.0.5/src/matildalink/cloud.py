"""Module for CSP-related specification.

"""

import enum

class InstanceType(enum.Enum):
    """Cloud instance types.

    Notes
    -----
    Our current implementation only supports AWS.

    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """Customize the values returned by enum.auto.

        This function lets the client get the string representation of the
        instance type in the standard form (e.g., 'g5.xlarge') by
        ``InstanceType.G5_XLARGE.value``.

        """
        return name.lower().replace('_', '.')

    G5_XLARGE = enum.auto()
    G6_XLARGE = enum.auto()

class Cloud(enum.Enum):
    """Cloud service provider (CSP).

    Notes
    -----
    We only support AWS currently.

    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """Customize the values returned by enum.auto.

        """
        return name.lower()

    AWS = enum.auto()

class Region(enum.Enum):
    """Cloud Region.

    Notes
    -----
    Our current implementation only supports AWS.

    """

    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        """Customize the values returned by enum.auto.

        This function lets the client get the string representation of the
        region in the standard form (e.g., 'us-east-1') by
        ``Region.US_EAST_1``.

        """
        return name.lower().replace('_', '-')

    US_EAST_1 = enum.auto()

class AZ(enum.Enum):
    """Availability zone.

    """
    pass
