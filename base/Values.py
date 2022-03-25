"""
Class definition of the Landscape Model Values class.
"""
import datetime

import base
import typing


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
    base.VERSION.added("1.7.0", "Type hints to `base.Values` ")
    base.VERSION.added("1.10.0", "`base.Values` have element names now")
    base.VERSION.changed("1.10.0", "`base.Values` switched to Google-style docstrings")
    base.VERSION.added("1.13.0", "Offset property to `base.Values` ")

    # noinspection PyUnusedLocal
    def __init__(
            self,
            values: typing.Any,
            extensions: typing.Sequence[base.Extension],
            unit: typing.Optional[str] = None,
            scales: str = "global",
            element_names: typing.Optional[typing.Sequence["base.Output"]] = None,
            offsets: typing.Optional[typing.Sequence[datetime.date]] = None,
            geometries: typing.Optional[typing.Sequence["base.Output"]] = None,
            **keywords
    ) -> None:
        """
        Initializes a Values object.

        Args:
            values: The values represented by the object.
            extensions: The extensions attached to the values.
            unit: The physical unit of the values.
            scales: The scales to which the values apply.
            element_names: The identifiers of the individual elements per scale.
            offsets: The offsets of linear scales.
            geometries: The spatial extents of scales.
            **keywords: Additional keywords not stored in the object.
        """
        self._values = values
        self._extension = base.Extensions()
        for extension in extensions:
            extension.register(self)
        self._unit = unit
        self._scales = scales
        self._element_names = element_names
        self._offsets = offsets
        self._geometries = geometries

    @property
    def extension(self) -> base.Extensions:
        """
        Gets a list of extensions associated with the values.

        Returns:
            A Landscape Model Extensions object.
        """
        return self._extension

    @property 
    def values(self) -> typing.Any:
        """
        Gets the actual values.

        Returns:
            A object containing the actual values in an appropriate representation.
        """
        return self._values

    @property
    def unit(self) -> str:
        """
        Gets the physical unit of the values.

        Returns:
        A string representing the physical unit of the values.
        """
        return self._unit

    @property
    def scales(self) -> str:
        """
        Gets the scales of the values.

        Returns:
            A string representing the physical scales of the values.
        """
        return self._scales

    @property
    def element_names(self) -> typing.Optional[typing.Sequence["base.Output"]]:
        """
        Gets the element names of the values.

        Returns:
            The identifiers of the individual elements per scale.
        """
        return self._element_names

    @property
    def offsets(self) -> typing.Optional[typing.Sequence[datetime.date]]:
        """
        Gets the offsets of the values.

        Returns:
            The offsets of the first element per scale.
        """
        return self._offsets

    @property
    def geometries(self) -> typing.Optional[typing.Sequence["base.Output"]]:
        """
        Gets the geometries of the values.

        Returns:
            The spatial extents to which the values apply per scale.
        """
        return self._geometries


class ExistingValues:
    """A class referencing to already existing values in a data store."""
    pass
