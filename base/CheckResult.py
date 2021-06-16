"""
Class definition of the Landscape ModelCheckResult class.
"""
import base


class CheckResult:
    """
    Defines a structure that contain results of attribute checks.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "base.CheckResult class for exchanging observer messages")
    base.VERSION.changed("1.3.5", "base.CheckResult refactored")
    base.VERSION.added("1.4.1", "Changelog in base.CheckResult")

    def __init__(self, message, adapted_values):
        self._message = message
        self._adapted_values = adapted_values

    @property
    def message(self):
        """
        The message returned by the check.
        :return: A tuple containing the severity and text of the message.
        """
        return self._message

    @property
    def adapted_values(self):
        """
        The adapted values.
        :return: A values object containing possibly adapted values.
        """
        return self._adapted_values
