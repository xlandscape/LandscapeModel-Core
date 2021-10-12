"""Class definition of the Landscape Model DataAttributes class."""
import base
import typing


class DataAttributes:
    """A container for data attributes."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.DataAttributes` class as a data attribute container")
    base.VERSION.changed("1.3.33", "`base.DataAttributes` refactored")
    base.VERSION.added("1.3.33", "`base.DataAttributes.append()` for dynamically adding data attributes")
    base.VERSION.added("1.4.1", "Changelog in `base.DataAttributes`")
    base.VERSION.changed("1.5.3", "`base.DataAttributes` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.DataAttributes` ")

    def __init__(self, attributes: typing.Sequence[base.DataAttribute]) -> None:
        """
        Initializes a DataAttributes container.

        Args:
            attributes: The initial attributes packed into the container.
        """
        self._attributes = list(attributes)

    def __iter__(self) -> typing.Iterator[base.DataAttribute]:
        """
        Provides an iterator over the data attributes in the container.

        Returns:
            An iterator over the data attributes in the container.
        """
        return self._attributes.__iter__()

    def append(self, attribute: base.DataAttribute) -> None:
        """
        Appends another attribute to the list of present attributes.

        Args:
            attribute: The attribute to append.

        Returns:
            Nothing
        """
        self._attributes.append(attribute)
