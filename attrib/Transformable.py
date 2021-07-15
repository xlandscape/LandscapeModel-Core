"""
Class definition of the Landscape Model Transformable attribute.
"""
import base


class Transformable:
    """
    Checks whether values have an attached transformation function.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`Transformable` attribute checker")
    base.VERSION.changed("1.3.33", "`attrib.Transformable.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in `attrib.Transformable`")
    base.VERSION.changed("1.5.3", "`attrib.Transformable` changelog uses markdown for code elements")

    def __init__(self, severity=2):
        self._type = type
        self._severity = severity
        return

    def check(self, values):
        """
        Checks values for an attached transformation function.
        :param values:
        :return: A CheckResult object.
        """
        if hasattr(values.extension, "t"):
            return base.CheckResult((4, "Values can be transformed"), values)
        else:
            return base.CheckResult((self._severity, "Values have no transform function"), values)

    @property
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string representing the name of the attribute checker.
        """
        return "TransformableChecker"

    @property
    def severity(self):
        """
        Gets the default severity of violations.
        :return: An integer representing the default severity of violations.
        """
        return self._severity
