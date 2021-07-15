"""
Class definition of Landscape Model output containers.
"""
import base


class OutputContainer:
    """
    A container of Landscape Model component outputs.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.OutputContainer` class for collecting outputs of a component")
    base.VERSION.changed("1.3.5", "`base.OutputContainer` refactored")
    base.VERSION.added("1.3.21", "`base.OutputContainer.append()` for dynamically adding outputs")
    base.VERSION.added("1.4.1", "Changelog in `base.OutputContainer`")
    base.VERSION.changed(
        "1.5.0", "Iteration over `base.OutputContainer` now returns `Output` objects instead of their names")
    base.VERSION.changed("1.5.3", "`base.OutputContainer` changelog uses markdown for code elements")

    def __init__(self, component=None, outputs=None):
        self._items = {}
        self._component = component
        if outputs is not None:
            for output in outputs:
                self._items[output.name] = output
        return

    def __getitem__(self, key):
        try:
            output = self._items[key]
        except KeyError:
            if isinstance(self._component, base.Component):
                raise KeyError("Component '" + self._component.name + "' has no output named '" + str(key) + "'")
            else:
                raise KeyError("There is no output named '" + str(key) + "'")
        return output

    def __iter__(self):
        return self._items.values().__iter__()

    def append(self, output):
        """
        Adds an output to the output container.
        :param output: The output to add.
        :return: Nothing.
        """
        self._items[output.name] = output
        return

    @property
    def component(self):
        """
        Gets the component to which the output belongs.
        :return: The output's component.
        """
        return self._component


class ProvisionalOutputs(OutputContainer):
    """
    A output container that generates outputs with every linked input.
    """
    def __init__(self, component, store):
        super(ProvisionalOutputs, self).__init__(component)
        self._store = store
        return

    def __getitem__(self, key):
        self._items.setdefault(key, base.Output(key, self._store, self.component))
        return self._items[key]
