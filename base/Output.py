"""
Class definition of a Landscape Model component output.
"""
import base


class Output:
    """
    A Landscape Model component output.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "base.Output class for representing component outputs")
    base.VERSION.changed("1.3.13", "base.Output refactored")
    base.VERSION.added("1.4.1", "Changelog in base.Output")

    def __init__(self, name, store, component=None):
        self._name = name
        self._store = store
        self._component = component
        if component is None:
            self._storeName = name
        else:
            self._storeName = component.name + "/" + name
        return

    def describe(self):
        """
        Describes the data provided by the output.
        :return:
        """
        return self.store.describe(self.store_name)

    def get_values(self, **keywords):
        """
        Gets the values from te output.
        :param keywords: Additional keywords controlling the data retrieval.
        :return: The values in their respective format.
        """
        values = self.store.get_values(self.store_name, **keywords)
        return values

    def set_values(self, values, **keywords):
        """
        Sets the values of the output.
        :param values: The new vales for the output.
        :param keywords: Additional keywords controlling the data storage.
        :return: Nothing.
        """
        self.store.set_values(self.store_name, values, **keywords)
        return

    @property
    def component(self):
        """
        Th component to which the output belongs.
        :return: A Landscape Model component.
        """
        return self._component

    @property
    def name(self):
        """
        The name of the output.
        :return: A string of the output name.
        """
        return self._name

    @property
    def store(self):
        """
        The store that is used by the output to store data.
        :return: A Landscape model data store.
        """
        return self._store

    @property
    def store_name(self):
        """
        The name of the data store that is used by the output.
        :return: A string of the data store name.
        """
        return self._storeName
