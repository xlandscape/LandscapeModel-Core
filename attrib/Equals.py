"""
Class definition for the Landscape Model Equals attribute.
"""
import base


class Equals:
    """
    Checks whether two values are equal.
    """
    # CHANGELOG
    base.VERSION.added("1.1.6", "Value equality checker")
    base.VERSION.changed("1.3.33", "`attrib.Equals.check()` returns base.CheckResult instead of tuple")
    base.VERSION.changed("1.3.33", "`attrib.Equals` refactored")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Equals` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Equals` changelog uses markdown for code elements")

    def __init__(self, value, severity=1):
        self._value = value
        self._severity = severity
        return

    def check(self, values):
        """
        Checks the values.
        :param values: The values to check.
        :return: A CheckResults object.
        """
        if self._value == values.values:
            return base.CheckResult((4, "Equals " + str(self.value)), values)
        else:
            return base.CheckResult(
                (self._severity, "Value " + str(values.values) + " does not equal " + str(self.value)),
                values
            )

    @property
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string containing the name.
        """
        return "EqualsChecker"

    @property
    def severity(self):
        """
        Gets the default severity of violations.
        :return: An integer representing the default severity.
        """
        return self._severity

    @property
    def value(self):
        """
        Gets the value to compare with.
        :return: The value to compare with.
        """
        return self._value
