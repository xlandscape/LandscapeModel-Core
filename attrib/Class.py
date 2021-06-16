"""
Class definition of the Landscape Model Class attribute.
"""
import base


class Class:
    """
    Checks whether values are instances of a specific Python class.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "attrib.Class")
    base.VERSION.added("1.2.1", "attrib.Class checker support of list[int] type")
    base.VERSION.added("1.3.33", "attrib.Class support of list[bytes], list[float], list[str] and tuple[float]")
    base.VERSION.changed("1.3.33", "attrib.Class.check() returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in class attrib.Class")
    base.VERSION.changed("1.4.2", "Changelog description")

    def __init__(self, expected_type, severity=2):
        self._type = expected_type
        self._severity = severity
        return

    def check(self, values):
        """
        Checks values of class compliance.
        :param values: The values to check.
        :return: A tuple representing the result of the check.
        """
        if isinstance(self._type, str):
            return base.CheckResult(self.check_str_type(values), values)
        return base.CheckResult(self.check_type(values), values)

    def check_list_type(self, values, element_type):
        """
        Checks whether all elements in a list of values are of a specific type.
        :param values: The values to check.
        :param element_type: The type to check for.
        :return: A tuple representing the result of the check.
        """
        if isinstance(values.values, (list, tuple)):
            if all(isinstance(x, element_type) for x in values.values):
                return 4, "Values are of type " + str(self.type)
            else:
                return self.severity, "Values are not of type " + self.type
        else:
            return self._severity, "Values are not a list"

    def check_str_type(self, values):
        """
        Checks values if the type to check is string.
        :param values: The values to check.
        :return: A tuple representing the result of the check.
        """
        if self.type == "list[int]":
            return self.check_list_type(values, int)
        elif self.type == "list[bytes]":
            return self.check_list_type(values, bytes)
        elif self.type in ["tuple[float]", "list[float]"]:
            return self.check_list_type(values, float)
        elif self.type == "list[str]":
            return self.check_list_type(values, str)
        return self.severity, "Check for unknown type " + self.type

    def check_type(self, values):
        """
        Checks the type of a scalar value.
        :param values: The value to check.
        :return: A tuple representing the result of the check.
        """
        if isinstance(values.values, self._type):
            return 4, "Values are of type " + str(self._type)
        else:
            return (
                self._severity,
                "Values are of type " + str(type(values.values)) + ", not of type " + str(self._type)
            )

    @property
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        return "ClassChecker"

    @property
    def severity(self):
        """
        Gets the severity of violations.
        :return: A number representing the severity of violations.
        """
        return self._severity

    @property
    def type(self):
        """
        Gets the type to check for.
        :return: A class or string specifying the type.
        """
        return self._type
