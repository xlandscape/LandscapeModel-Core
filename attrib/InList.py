"""
Class definition for the Landscape Model InList attribute.
"""
import base
import typing


class InList(base.DataAttribute):
    """
    Checks whether a value is within a list of  allowed values.
    """
    # CHANGELOG
    base.VERSION.added("1.4.12", "`attrib.InList` attribute to check whether a value is within a set of allowed values")
    base.VERSION.changed("1.7.0", "`attrib.InList` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.InList` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.InList` ")

    def __init__(self, values: typing.Sequence, severity: int = 1) -> None:
        self._values = values
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks the values.
        :param values: The values to check.
        :return: A CheckResults object.
        """
        if values.values in self._values:
            return base.CheckResult((4, "Within allowed values",), values)
        else:
            return base.CheckResult(
                (self._severity, f"Value {values.values} is not one of the allowed {self.values}"),
                values
            )

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.
        :return: A string containing the name.
        """
        return "InListChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.
        :return: An integer representing the default severity.
        """
        return self._severity

    @property
    def values(self) -> typing.Sequence:
        """
        Gets the value to compare with.
        :return: The value to compare with.
        """
        return self._values
