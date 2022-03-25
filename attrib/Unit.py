"""Class definition of the Landscape Model Unit attribute."""
import base
import numpy
import typing


class Unit(base.DataAttribute):
    """Checks whether values have a specific physical unit."""
    # CHANGELOG
    base.VERSION.added("1.3.3", "Unit attribute class to check and convert physical units (currently hard-coded)")
    base.VERSION.changed("1.3.33", "`attrib.Unit.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.3.34", "Additional unit conversions in class `attrib.Unit`")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Unit` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Unit` changelog uses markdown for code elements")
    base.VERSION.added("1.6.4", "`attrib.Unit` support for lists")
    base.VERSION.added("1.6.4", "Further unit conversion to `attrib.Unit` ")
    base.VERSION.changed("1.7.0", "`attrib.Unit` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Unit` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `attrib.Unit` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Unit` ")
    base.VERSION.changed("1.10.0", "`attrib.Unit` keeps element names for converted values")

    def __init__(self, expected_unit: typing.Optional[str], severity: int = 2) -> None:
        """
        Initializes a Unit attribute.

        Args:
            expected_unit: The expected unit.
            severity: The severity if the actual unit differs from the expected unit.
        """
        self._unit = expected_unit
        self._severity = severity

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        if values.unit == self._unit:
            return base.CheckResult((4, f"Values have unit {self.unit}"), values)
        original_unit = str(values.unit)
        if isinstance(values.values, float) or isinstance(values.values, numpy.ndarray):
            adapted_values = self.try_convert(values.values, original_unit)
        elif isinstance(values.values, list) and all([isinstance(x, float) for x in values.values]):
            adapted_values = [self.try_convert(x, original_unit) for x in values.values]
            if adapted_values[0] is None:
                adapted_values = None
        else:
            return base.CheckResult(
                (
                    self._severity,
                    f"Cannot convert values with unit {original_unit} of {type(values.values)}"
                ),
                values
            )
        if adapted_values is not None:
            return base.CheckResult(
                (3, f"Values of unit {original_unit} have been converted to {self.unit}"),
                base.Values(
                    adapted_values,
                    values.extension,
                    self._unit,
                    values.scales,
                    values.element_names,
                    values.offsets,
                    values.geometries
                )
            )
        return base.CheckResult(
            (self._severity, f"Values have unit {original_unit}, not {self.unit}"),
            values
        )

    def try_convert(self, value: float, unit: str) -> typing.Optional[float]:
        """
        Tries to convert a value with one physical unit to another physical unit.

        Args:
            value: The value to convert.
            unit: The unit the value to convert currently is in.

        Returns:
            The converted values or None if no conversion is possible.
        """
        if unit == "g/ha" and self._unit == "mg/m²":
            return value * .1
        elif unit == "m³/d" and self._unit == "m³/s":
            return value / 86400
        elif unit == "mg/m³" and self._unit == "ng/l":
            return value * 1e3
        elif unit == "g/m³" and self._unit == "ng/l":
            return value * 1e6
        elif unit == "1/h" and self._unit == "1/d":
            return value * 24
        elif unit == "l/(ng*h)" and self._unit == "l/(ng*d)":
            return value * 24
        elif unit == "g/m³" and self._unit == "mg/m³":
            return value * 1e3
        elif unit == "g/cm³" and self._unit == "kg/m³":
            return value * 1e3
        return None

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        return "UnitChecker"

    @property
    def severity(self) -> int:
        """
        Gets the severity of violations.

        Returns:
            A number representing the severity of violations.
        """
        return self._severity

    @property
    def unit(self) -> str:
        """
        Gets the unit to check for.

        Returns:
            A string specifying the unit.
        """
        return self._unit
