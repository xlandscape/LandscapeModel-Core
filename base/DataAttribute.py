"""
Class definition of the Landscape Model DataAttribute class.
"""
import base


class DataAttribute:
    """
    Checks whether values comply to a specification regarding a specific data attribute and potentially transforms them.
    """
    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.
        :param values: The values to check.
        :return: A tuple representing the result of the check.
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        raise NotImplementedError
