"""Class definition of the Landscape Model Scales attribute."""
import base


class Scales(base.DataAttribute):
    """Checks whether values have specific scales."""
    # CHANGELOG
    base.VERSION.added("1.3.33", "Scale attribute checker")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Scales` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Scales` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Scales` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Scales` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.Scales` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Scales` ")
    base.VERSION.changed("1.15.4", "String representations of `attrib.Scales` is now more readable")

    def __init__(self, expected_scales: str, severity: int = 2) -> None:
        """
        Initializes the Scales attribute.

        Args:
            expected_scales: The expected scales.
            severity: The severity if actual scales differ from the expected scales.
        """
        self._scales = expected_scales
        self._severity = severity

    def __repr__(self) -> str:
        return f"Scales: `{self.scales}`"

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if values.scales is None:
            return base.CheckResult((self._severity, "Values have unknown scale, requested scale ignored"), values)
        if values.scales == self._scales:
            return base.CheckResult((4, f"Values have scales {self.scales}"), values)
        return base.CheckResult(
            (self._severity, f"Values have scales {values.scales}, not {self.scales}"), values)

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        return "ScalesChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.

        Returns:
            A number representing the default severity of violations.
        """
        return self._severity

    @property
    def scales(self) -> str:
        """
        Gets the scales to check for.

        Returns:
            A string specifying the scales.
        """
        return self._scales
