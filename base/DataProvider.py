"""Base class for data providers."""
import base


class DataProvider:
    """A provider of data for the Landscape Model."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.DataProvider` class for data providers")
    base.VERSION.changed("1.3.13", "`base.DataProvider` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.DataProvider`")
    base.VERSION.changed("1.5.3", "`base.DataProvider` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.DataProvider` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.DataProvider` ")

    def __init__(self, output: base.Output) -> None:
        """
        Initializes a DataProvider.

        Args:
            output: The component output that provides the data.
        """
        self._output = output

    def describe(self) -> dict:
        """
        Describes a data source.

        Returns:
            A dictionary describing the data source.
        """
        return self.output.describe()

    def get_values(self, **keywords) -> base.Values:
        """
        Gets the values from the data provider.

        Args:
            **keywords: Additional keywords controlling the data retrieval.

        Returns:
            The values in their corresponding type.
        """
        values = self._output.get_values(**keywords)
        return values

    @property
    def output(self) -> base.Output:
        """
        The Landscape Model component output associated with the data provider.

        Returns:
            A Landscape Model component output.
        """
        return self._output
