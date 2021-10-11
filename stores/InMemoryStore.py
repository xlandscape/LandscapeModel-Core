"""
Class definition of the In-Memory Landscape Model store.
"""
import base
import numpy
import typing


class InMemoryStore(base.Store):
    """
    A Landscape model store that manages data exchange entirely by Python objects in memory.

    PARAMETERS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`store.InMemoryStore` ")
    base.VERSION.changed("1.3.27", "`store.InMemoryStore` `slice` keyword renamed to `slices`")
    base.VERSION.changed("1.3.27", "`store.InMemoryStore` updated")
    base.VERSION.changed("1.3.33", "`store.InMemoryStore` stores physical unit if specified")
    base.VERSION.added("1.4.1", "Changelog in `store.InMemoryStore` ")
    base.VERSION.changed("1.4.1", "`store.InMemoryStore` class documentation")
    base.VERSION.changed("1.4.9", "`store.InMemoryStore` data type access")
    base.VERSION.changed("1.5.3", "`store.InMemoryStore` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `stores.InMemoryStore` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `stores.InMemoryStore` ")

    def __init__(self) -> None:
        self._data = {}
        self._scales = {}
        self._unit = {}

    def describe(self, name: str) -> dict[str, typing.Any]:
        """
        Describes a data set in the store.
        :param name: The name of the data set.
        :return: A dictionary describing the data set.
        """
        return {"scales": self._scales[name], "unit": self._unit[name]}

    def get_values(self, name: str, **keywords) -> typing.Any:
        """
        Gets the values of a data set from the store.
        :param name: The name of the data set.
        :param keywords: Additional keywords.
        :return: The values of the data set in their original representation.
        """
        try:
            values = self._data[name]
        except KeyError:
            raise KeyError(f"InMemoryStore does not contain data for '{name}'")
        return values

    def set_values(
            self,
            name: str,
            values: typing.Any,
            scales: typing.Optional[str] = None,
            unit: typing.Optional[str] = None,
            shape: typing.Optional[typing.Sequence[int]] = None,
            data_type: typing.Optional[type] = None,
            chunks: typing.Optional[typing.Sequence[slice]] = None,
            create: bool = True,
            slices: typing.Optional[typing.Sequence[slice]] = None
    ) -> None:
        """
        Stores a data set in the store.
        :param name: The name of the data set.
        :param values: The values of the data set.
        :param scales: The scales to which the values of the data set apply.
        :param unit: The physical unit of the values.
        :param shape: The shape of a newly created empty array.
        :param data_type: The data type of a newly created empty array.
        :param chunks: The chunk size for a newly created empty array.
        :param create: Specifies whether a data set should be created or not.
        :param slices: Defines the portion of the data set that was passed to the function.
        :return: Nothing.
        """
        if isinstance(values, type):
            type_name = f"{values.__module__}.{values.__qualname__}"
            # noinspection SpellCheckingInspection
            if type_name == "numpy.ndarray" and create:
                self._data[name] = numpy.zeros(shape, data_type)
            else:
                raise TypeError(f"Unsupported type: {type(values)}")
        elif isinstance(values, numpy.ndarray) and slices is not None:
            self._data[name][slices] = values
        else:
            self._data[name] = values
        self._scales[name] = scales
        self._unit[name] = unit

    def has_dataset(self, name: str, partial: bool = False) -> bool:
        """
        Checks whether a dataset exists in the store or not.
        :param name: The name of the dataset.
        :param partial: Specifies whether to also check partial dataset paths or not.
        :return: A boolean value indicating whether the dataset exists or not.
        """
        return name in self._data
