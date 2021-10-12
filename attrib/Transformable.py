"""Class definition of the Landscape Model Transformable attribute."""
import base


class Transformable(base.DataAttribute):
    """Checks whether values have an attached transformation function."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`Transformable` attribute checker")
    base.VERSION.changed("1.3.33", "`attrib.Transformable.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in `attrib.Transformable`")
    base.VERSION.changed("1.5.3", "`attrib.Transformable` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Transformable` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Transformable` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Transformable` ")

    def __init__(self, severity: int = 2) -> None:
        """
        Initializes a Transformable attribute.

        Args:
            severity: The severity if values are not transformable.
        """
        self._type = type
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if hasattr(values.extension, "t"):
            return base.CheckResult((4, "Values can be transformed"), values)
        else:
            return base.CheckResult((self._severity, "Values have no transform function"), values)

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        return "TransformableChecker"

    @property
    def severity(self) -> int:
        """
        Gets the default severity of violations.

        Returns:
            An integer representing the default severity of violations.
        """
        return self._severity
