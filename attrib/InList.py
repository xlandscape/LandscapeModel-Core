"""
Class definition for the Landscape Model InList attribute.
"""
import base


class InList:
    """
    Checks whether a value is within a list of  allowed values.
    """
    # CHANGELOG

    def __init__(self, values, severity=1):
        self._values = values
        self._severity = severity
        return

    def check(self, values):
        """
        Checks the values.
        :param values: The values to check.
        :return: A CheckResults object.
        """
        if values.values in self._values:
            return base.CheckResult((4, "Within allowed values",), values)
        else:
            return base.CheckResult(
                (self._severity, "Value " + str(values.values) + " is not one of the allowed " + str(self.values)),
                values
            )

    @property
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string containing the name.
        """
        return "InListChecker"

    @property
    def severity(self):
        """
        Gets the default severity of violations.
        :return: An integer representing the default severity.
        """
        return self._severity

    @property
    def values(self):
        """
        Gets the value to compare with.
        :return: The value to compare with.
        """
        return self._values
