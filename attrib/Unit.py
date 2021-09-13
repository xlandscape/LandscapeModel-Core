"""
Class definition of the Landscape Model Unit attribute.
"""
import base
import numpy


class Unit:
    """
    Checks whether values have a specific physical unit.
    """
    # CHANGELOG
    base.VERSION.added("1.3.3", "Unit attribute class to check and convert physical units (currently hard-coded)")
    base.VERSION.changed("1.3.33", "`attrib.Unit.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.3.34", "Additional unit conversions in class `attrib.Unit`")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Unit` ")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Unit` changelog uses markdown for code elements")

    def __init__(self, expected_unit, severity=2):
        self._unit = expected_unit
        self._severity = severity
        return

    def check(self, values):
        """
        Checks values of class compliance.
        :param values: The values to check.
        :return: A tuple representing the result of the check.
        """
        if values.unit == self._unit:
            return base.CheckResult((4, "Values have unit " + str(self._unit)), values)
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
                    "Cannot convert values with unit " + original_unit + ", of " + str(type(values.values))
                ),
                values
            )
        if adapted_values is not None:
            return base.CheckResult(
                (3, "Values of unit " + original_unit + " have been converted to " + str(self.unit)),
                base.Values(adapted_values, values.extension, self._unit, values.scales)
            )
        return base.CheckResult(
            (self._severity, "Values have unit " + original_unit + ", not " + str(self._unit)),
            values
        )

    def try_convert(self, value, unit):
        """
        Tries to convert a value with one physical unit to another physical unit.
        :param value: The value to convert.
        :param unit: The unit the value to convert currently is in.
        :return: The converted values or None if no conversion is possible.
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
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        return "UnitChecker"

    @property
    def severity(self):
        """
        Gets the severity of violations.
        :return: A number representing the severity of violations.
        """
        return self._severity

    @property
    def unit(self):
        """
        Gets the unit to check for.
        :return: A string specifying the unit.
        """
        return self._unit
