"""Class definition of the Landscape Model Class attribute."""
import base
import types


class Class(base.DataAttribute):
    """Checks whether values are instances of a specific Python class."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`attrib.Class` ")
    base.VERSION.added("1.2.1", "`attrib.Class` checker support of list[int] type")
    base.VERSION.added("1.3.33", "`attrib.Class` support of list[bytes], list[float], list[str] and tuple[float]")
    base.VERSION.changed("1.3.33", "`attrib.Class.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Class` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Class` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Class` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Class` ")
    base.VERSION.changed(
        "1.7.0",
        "Removed support of string-based type definitions in `attrib.Class` in favor for generic types introduced in "
        "Python 3.9"
    )
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.Class` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Class` ")

    def __init__(self, expected_type: type, severity: int = 2) -> None:
        """
        Initializes a Class attribute.

        Args:
            expected_type: The type expected for the data.
            severity: The severity if the actual type differs from the expected type.
        """
        self._type = expected_type
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if isinstance(self._type, types.GenericAlias):
            return base.CheckResult(self.check_generic_type(values), values)
        return base.CheckResult(self.check_type(values), values)

    def check_list_type(self, values: base.Values, element_type: type) -> tuple[int, str]:
        """
        Checks whether all elements in a list of values are of a specific type.

        Args:
            values: The values to check.
            element_type: The type to check for.

        Returns:
            A tuple representing the result of the check.
        """
        if isinstance(values.values, (list, tuple)):
            if all(isinstance(x, element_type) for x in values.values):
                return 4, f"Values are of type {self.type}"
            else:
                return self.severity, f"Values are not of type {self.type}"
        else:
            return self._severity, "Values are not a list"

    def check_generic_type(self, values: base.Values) -> tuple[int, str]:
        """
        Checks values if the type to check is a generic alias.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if self.type == list[int]:
            return self.check_list_type(values, int)
        elif self.type == list[bytes]:
            return self.check_list_type(values, bytes)
        elif self.type in [tuple[float], list[float]]:
            return self.check_list_type(values, float)
        elif self.type == list[str]:
            return self.check_list_type(values, str)
        return self.severity, f"Check for unknown type {self.type}"

    def check_type(self, values: base.Values) -> tuple[int, str]:
        """
        Checks the type of scalar value.

        Args:
            values: The value to check.

        Returns:
            A tuple representing the result of the check.
        """
        if isinstance(values.values, self._type):
            return 4, f"Values are of type {self.type}"
        else:
            return (
                self._severity,
                f"Values are of type {type(values.values)}, not of type {self.type}"
            )

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        return "ClassChecker"

    @property
    def severity(self) -> int:
        """
        Gets the severity of violations.

        Returns:
            A number representing the severity of violations.
        """
        return self._severity

    @property
    def type(self) -> type:
        """
        Gets the type to check for.

        Returns:
            A class or string specifying the type.
        """
        return self._type
