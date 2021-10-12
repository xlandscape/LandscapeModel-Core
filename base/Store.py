"""Class definition for Landscape Model stores."""
import base
import typing


class Store:
    """Base class for Landscape Model store implementations."""
    # CHANGELOG
    base.VERSION.added("1.3.28", "`base.Store` class for representing Landscape Model stores")
    base.VERSION.added("1.3.35", "`base.Store.has_dataset()` to check whether store contains specific data")
    base.VERSION.added("1.4.1", "Changelog in `base.Store` ")
    base.VERSION.changed("1.5.3", "`base.Store` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Store` ")

    def close(self) -> None:
        """
        Closes the store.

        Returns:
            Nothing.
        """
        return

    def describe(self, name: str) -> dict[str, typing.Any]:
        """
        Describes a dataset in the store.

        Args:
            name: The name of the dataset.

        Returns:
            A dictionary describing the dataset.
        """
        raise NotImplementedError

    def get_values(self, name: str, **keywords) -> typing.Any:
        """
        Gets the values of a data set from the store.

        Args:
            name: The name of the data set.
            keywords: Additional keywords.

        Returns:
            The values of the data set in their original representation.
        """
        raise NotImplementedError

    def set_values(self, name: str, values: typing.Any, scales: typing.Optional[str] = None) -> None:
        """
        Stores a data set in the store.

        Args:

            name: The name of the data set.
            values: The values of the data set.
            scales: The scales to which the values of the data set apply.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    def has_dataset(self, name: str, partial: bool = False) -> bool:
        """
        Checks whether a dataset exists in the store or not.

        Args:
            name: The name of the dataset.
            partial: Specifies whether to also check partial dataset paths or not.

        Returns:
            A boolean value indicating whether the dataset exists or not.
        """
        raise NotImplementedError
