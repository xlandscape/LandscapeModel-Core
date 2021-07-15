"""
Class definition of the Landscape Model Values class.
"""
import base


class Values:
    """
    Represents data values that are exchanged between components.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Values class` for exchanged data values")
    base.VERSION.changed("1.3.5", "`base.Values` refactored")
    base.VERSION.added("1.3.33", "Quick access to metadata by `base.Values.unit` and `base.Values.scales` ")
    base.VERSION.added("1.4.1", "Changelog in `base.Values` ")
    base.VERSION.changed("1.5.3", "`base.Values` changelog uses markdown for code elements")

    # noinspection PyUnusedLocal
    def __init__(self, values, extensions, unit=None, scales="global", **keywords):
        self._values = values
        self._extension = base.Extensions()
        for extension in extensions:
            extension.register(self)
        self._unit = unit
        self._scales = scales
        return

    @property
    def extension(self):
        """
        Gets a list of extensions associated with the values.
        :return: A Landscape Model Extensions object.
        """
        return self._extension

    @property 
    def values(self):
        """
        Gets the actual values.
        :return: A object containing the actual values in an appropriate representation.
        """
        return self._values

    @property
    def unit(self):
        """
        Gets the physical unit of the values.
        :return: A string representing the physical unit of the values.
        """
        return self._unit

    @property
    def scales(self):
        """
        Gets the scales of the values.
        :return: A string representing the physical scales of the values.
        """
        return self._scales
