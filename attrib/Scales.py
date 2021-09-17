"""
Class definition of the Landscape Model Scales attribute.
"""
import base


class Scales(base.DataAttribute):
    """
    Checks whether values have specific scales.
    """
    # CHANGELOG
    base.VERSION.added("1.3.33", "Scale attribute checker")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Scales` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Scales` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Scales` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Scales` ")

    def __init__(self, expected_scales: str, severity: int = 2) -> None:
        self._scales = expected_scales
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values for scales compliance.
        :param values: The values to check.
        :return: A tuple representing the result of the check.
        """
        if values.scales is None:
            return base.CheckResult((self._severity, "Values have unknown scale, requested scale ignored"), values)
        if values.scales == self._scales:
            return base.CheckResult((4, "Values have scales " + str(self._scales)), values)
        return base.CheckResult(
            (self._severity, "Values have scales " + values.scales + ", not " + str(self._scales)), values)

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        return "ScalesChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.
        :return: A number representing the default severity of violations.
        """
        return self._severity

    @property
    def scales(self) -> str:
        """
        Gets the scales to check for.
        :return: A string specifying the scales.
        """
        return self._scales
