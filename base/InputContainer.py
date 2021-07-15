"""
Class definition of the Landscape Model InputContainer class.
"""
import base


class InputContainer:
    """
    A container fr component inputs.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.InputContainer` class for collecting the inputs of a component")
    base.VERSION.added("1.2.3", "Added `base.InputContainer.append()` and `.__contains__()` ")
    base.VERSION.changed("1.3.33", "`base.InputContainer` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.InputContainer` ")

    def __init__(self, component=None, inputs=None):
        self._items = {}
        self._component = component
        if inputs is not None:
            for component_input in inputs:
                self._items[component_input.name] = component_input
        return

    def __contains__(self, item):
        return item in self._items

    def __getitem__(self, key):
        try:
            component_input = self._items[key]
        except KeyError:
            if isinstance(self._component, base.Component):
                raise KeyError("Component '" + self._component.name + "' has no input named '" + key + "'")
            else:
                raise KeyError("There is no output named '" + key + "'")
        return component_input

    def __setitem__(self, key, value):
        self[key].provider = base.DataProvider(value)
        return

    def __iter__(self):
        return self._items.values().__iter__()

    def append(self, component_input):
        """
        Appends an input to the input container.
        :param component_input: The input to append.
        :return: Nothing.
        """
        self._items[component_input.name] = component_input
        return

    @property
    def component(self):
        """
        Gets the component to which the input container belongs.
        :return: The component of the input container.
        """
        return self._component
