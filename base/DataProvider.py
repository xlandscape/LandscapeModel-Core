"""
Base class for data providers.
"""
import base


class DataProvider:
    """
    A provider of data for the Landscape Model.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "base.DataProvider class for data providers")
    base.VERSION.changed("1.3.13", "base.DataProvider refactored")
    base.VERSION.added("1.4.1", "Changelog in base.DataProvider")

    def __init__(self, output):
        self._output = output
        return

    def describe(self):
        """
        Describes a data source.
        :return: A dictionary describing the data source.
        """
        return self.output.describe()

    def get_values(self, **keywords):
        """
        Gets the values from the data provider.
        :param keywords: Additional keywords controlling the data retrieval.
        :return: The values in their corresponding type.
        """
        values = self._output.get_values(**keywords)
        return values

    @property
    def output(self):
        """
        The Landscape Model component output associate with the data provider.
        :return: A Landscape Model component output.
        """
        return self._output
