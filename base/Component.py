"""
Class definition of the Landscape Model component class.
"""
import base


class Component:
    """
    The base type for all Landscape Model components.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Component` class representing Landscape Model components")
    base.VERSION.changed("1.3.33", "`base.Component` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Component`")

    def __init__(self, name, default_observer, default_store):
        self._inputs = base.InputContainer(self)
        self._name = name
        self._outputs = base.OutputContainer(self)
        self._defaultObserver = default_observer
        self._defaultStore = default_store
        self._module = None
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        raise NotImplementedError

    @property
    def default_observer(self):
        """
        Gets the default observer of the component.
        :return: The default observer of the component.
        """
        return self._defaultObserver

    @property
    def default_store(self):
        """
        Gets the default store of the component.
        :return: The default store of the component.
        """
        return self._defaultStore

    @property
    def inputs(self):
        """
        Gets the inputs of the component.
        :return: The inputs of the component.
        """
        return self._inputs

    @property
    def name(self):
        """
        Gets the name of the component.
        :return: A string containing the name of the component.
        """
        return self._name

    @property
    def outputs(self):
        """
        Gets the outputs of the component.
        :return: The outputs of the component.
        """
        return self._outputs

    @property
    def module(self):
        """
        Gets the module used by the component.
        :return: The module used by the component.
        """
        return self._module
