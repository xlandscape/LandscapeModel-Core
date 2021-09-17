"""
Class definition of the Landscape Model DataAttributes class.
"""
import base
import typing


class DataAttributes:
    """
    A container for data attributes.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.DataAttributes` class as a data attribute container")
    base.VERSION.changed("1.3.33", "`base.DataAttributes` refactored")
    base.VERSION.added("1.3.33", "`base.DataAttributes.append()` for dynamically adding data attributes")
    base.VERSION.added("1.4.1", "Changelog in `base.DataAttributes`")
    base.VERSION.changed("1.5.3", "`base.DataAttributes` changelog uses markdown for code elements")

    def __init__(self, attributes: typing.Sequence[base.DataAttribute]) -> None:
        self._attributes = list(attributes)

    def __iter__(self) -> typing.Iterator[base.DataAttribute]:
        return self._attributes.__iter__()

    def append(self, attribute: base.DataAttribute) -> None:
        """
        Appends another attribute to the list of present attributes.
        :param attribute: The attribute to append.
        :return: Nothing
        """
        self._attributes.append(attribute)
