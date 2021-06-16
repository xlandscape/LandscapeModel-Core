"""
Class definition of the Landscape Model DataAttributes class.
"""
import base


class DataAttributes:
    """
    A container for data attributes.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "base.DataAttributes class as a data attribute container")
    base.VERSION.changed("1.3.33", "base.DataAttributes refactored")
    base.VERSION.added("1.3.33", "base.DataAttributes.append() for dynamically adding data attributes")
    base.VERSION.added("1.4.1", "Changelog in base.DataAttributes")

    def __init__(self, attributes):
        self._attributes = attributes
        return

    def __iter__(self):
        return self._attributes.__iter__()

    def append(self, attribute):
        """
        Appends another attribute to the list of present attributes.
        :param attribute: The attribute to append.
        :return: Nothing
        """
        self._attributes.append(attribute)
        return
