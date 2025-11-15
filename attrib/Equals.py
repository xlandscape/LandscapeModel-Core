"""Class definition for the Landscape Model Equals attribute."""
import base
import typing


class Equals(base.DataAttribute):
    """Checks whether two values are equal."""
    # CHANGELOG
    base.VERSION.added("1.1.6", "Value equality checker")
    base.VERSION.changed("1.3.33", "`attrib.Equals.check()` returns base.CheckResult instead of tuple")
    base.VERSION.changed("1.3.33", "`attrib.Equals` refactored")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Equals`")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Equals` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Equals` got new base class `base.DataAttribute`")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Equals`")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.Equals`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Equals`")
    base.VERSION.changed("1.15.4", "String representations of `attrib.Equals` is now more readable")
    base.VERSION.changed("1.18.0", "Code refactory in `attrib.Equals`")

    def __init__(self, value: typing.Any, severity: int = 1) -> None:
        """
        Initializes an Equals attribute.

        Args:
            value: The value to check.
            severity: The severity if expected and actual values are unequal.
        """
        self._value = value
        self._severity = severity

    def __repr__(self) -> str:
        return f"Equals: `{self.value}`"

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
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

        Returns:
            A string containing the name of the attribute checker.
        """
        return "EqualsChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.

        Returns:
            An integer representing the default severity.
        """
        return self._severity

    @property
    def value(self) -> typing.Any:
        """
        Gets the value to compare with.

        Returns:
            The value to compare with.
        """
        return self._value
