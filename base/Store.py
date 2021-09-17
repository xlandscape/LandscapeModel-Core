"""
Class definition for Landscape Model stores.
"""
import base
import typing


class Store:
    """
    Base class for Landscape Model store implementations.
    """
    # CHANGELOG
    base.VERSION.added("1.3.28", "`base.Store` class for representing Landscape Model stores")
    base.VERSION.added("1.3.35", "`base.Store.has_dataset()` to check whether store contains specific data")
    base.VERSION.added("1.4.1", "Changelog in `base.Store` ")
    base.VERSION.changed("1.5.3", "`base.Store` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Store` ")

    def close(self) -> None:
        """
        Closes the store.
        :return: Nothing.
        """
        return

    def describe(self, name: str) -> dict[str, typing.Any]:
        """
        Describes a data set in the store (not available for the InMemoryStore).
        :param name: The name of the data set.
        :return: An empty dictionary.
        """
        raise NotImplementedError

    def get_values(self, name: str, **keywords) -> typing.Any:
        """
        Gets the values of a data set from the store.
        :param name: The name of the data set.
        :param keywords: Additional keywords.
        :return: The values of the data set in their original representation.
        """
        raise NotImplementedError

    def set_values(self, name: str, values: typing.Any, scales: typing.Optional[str] = None) -> None:
        """
        Stores a data set in the store.
        :param name: The name of the data set.
        :param values: The values of the data set.
        :param scales: The scales to which the values of the data set apply.
        :return: Nothing.
        """
        raise NotImplementedError

    def has_dataset(self, name: str, partial: bool = False) -> bool:
        """
        Checks whether a dataset exists in the store or not.
        :param name: The name of the dataset.
        :param partial: Specifies whether to also check partial dataset paths or not.
        :return: A boolean value indicating whether the dataset exists or not.
        """
        raise NotImplementedError
