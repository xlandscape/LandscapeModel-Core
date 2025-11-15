"""Class definition for the Landscape Model InList attribute."""
import base
import typing


class InList(base.DataAttribute):
    """Checks whether a value is within a list of  allowed values."""
    # CHANGELOG
    base.VERSION.added("1.4.12", "`attrib.InList` attribute to check whether a value is within a set of allowed values")
    base.VERSION.changed("1.7.0", "`attrib.InList` got new base class `base.DataAttribute`")
    base.VERSION.added("1.7.0", "Type hints to `attrib.InList`")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.InList`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.InList`")
    base.VERSION.changed("1.9.4", "`attrib.InList` can now check all items in a sequence")
    base.VERSION.changed("1.18.0", "Code refactory in `attrib.InList`")

    def __init__(self, values: typing.Sequence, severity: int = 1) -> None:
        """
        Initializes an InList attribute.

        Args:
            values: The allowed values.
            severity: The severity if values are not within the allowed values.
        """
        self._values = values
        self._severity = severity

    def __repr__(self) -> str:
        return f"InList: {', '.join(['`' + str(x) + '`' for x in self._values])}"

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if isinstance(values.values, list):
            if all([x in self._values for x in values.values]):
                return base.CheckResult((4, "All values within allowed values",), values)
            else:
                return base.CheckResult(
                    (self._severity, f"Some values are not allowed: {values.values} (allowed: {self.values})"),
                    values
                )
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

        Returns:
            A string containing the name of the attribute checker.
        """
        return "InListChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.

        Returns:
            An integer representing the default severity.
        """
        return self._severity

    @property
    def values(self) -> typing.Sequence:
        """
        Gets the value to compare with.

        Returns:
            The value to compare with.
        """
        return self._values
