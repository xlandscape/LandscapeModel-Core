"""
Class definition for the Landscape Model Equals attribute.
"""
import base
import typing


class Equals(base.DataAttribute):
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
    base.VERSION.changed("1.7.0", "`attrib.Equals` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Equals` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.Equals` ")

    def __init__(self, value: typing.Any, severity: int = 1) -> None:
        self._value = value
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks the values.
        :param values: The values to check.
        :return: A CheckResults object.
        """
        if self._value == values.values:
            return base.CheckResult((4, f"Equals {self.value}"), values)
        else:
            return base.CheckResult(
                (self._severity, f"Value {values.values} does not equal {self.value}"),
                values
            )

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.
        :return: A string containing the name.
        """
        return "EqualsChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.
        :return: An integer representing the default severity.
        """
        return self._severity

    @property
    def value(self) -> typing.Any:
        """
        Gets the value to compare with.
        :return: The value to compare with.
        """
        return self._value
