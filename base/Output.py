"""
Class definition of a Landscape Model component output.
"""
import base


class Output:
    """
    A Landscape Model component output.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Output` class for representing component outputs")
    base.VERSION.changed("1.3.13", "`base.Output` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Output` ")
    base.VERSION.changed("1.5.0", "`base.Output` manages default attributes")
    base.VERSION.changed("1.5.0", "`base.Output` output description and hints for attribute descriptions")
    base.VERSION.changed("1.5.0", "usage of specified defaults if no attributes passed in a call to set values")
    base.VERSION.added(
        "1.5.0", "`base.Output` properties `default_attributes`, `description` and `attribute_hints` ")
    base.VERSION.changed("1.5.1", "small changes in `base.Output` changelog")
    base.VERSION.changed("1.5.3", "`base.Output` changelog uses markdown for code elements")

    def __init__(self, name, store, component=None, default_attributes=None, description=None, attribute_hints=None):
        self._name = name
        self._store = store
        self._component = component
        if component is None:
            self._storeName = name
        else:
            self._storeName = component.name + "/" + name
        self._default_attributes = {} if default_attributes is None else default_attributes
        self._description = description
        self._attribute_hints = attribute_hints
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
        for attribute, value in self._default_attributes.items():
            if attribute not in keywords:
                keywords[attribute] = value
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

    @property
    def default_attributes(self):
        """
        A set of default attributes associated with the output.
        :return: A dictionary of attribute names and their default value.
        """
        return self._default_attributes

    @property
    def description(self):
        """
        A textual description of the input.
        :return: A string containing the textual description of the input.
        """
        return self._description

    @property
    def attribute_hints(self):
        """
        Contains hints about data attributes useful for documentation.
        :return: A dictionary of attribute types and textual or object hints.
        """
        return self._attribute_hints
