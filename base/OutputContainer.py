"""Class definition of Landscape Model output containers."""
import base
import typing


class OutputContainer:
    """A container of Landscape Model component outputs."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.OutputContainer` class for collecting outputs of a component")
    base.VERSION.changed("1.3.5", "`base.OutputContainer` refactored")
    base.VERSION.added("1.3.21", "`base.OutputContainer.append()` for dynamically adding outputs")
    base.VERSION.added("1.4.1", "Changelog in `base.OutputContainer`")
    base.VERSION.changed(
        "1.5.0", "Iteration over `base.OutputContainer` now returns `Output` objects instead of their names")
    base.VERSION.changed("1.5.3", "`base.OutputContainer` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.OutputContainer`")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.OutputContainer`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.OutputContainer`")

    def __init__(
            self,
            component: typing.Optional["base.Component"] = None,
            outputs: typing.Optional[typing.Sequence[base.Output]] = None
    ) -> None:
        """
        Initializes an OutputContainer.

        Args:
            component: The component to which the container belongs.
            outputs: The outputs that are initially part of the container.
        """
        self._items = {}
        self._component = component
        if outputs is not None:
            for output in outputs:
                self._items[output.name] = output

    def __getitem__(self, key: str) -> base.Output:
        """
        Gets an output from the container by name.

        Args:
            key: The name of the output.

        Returns:
            The output with the given name.
        """
        try:
            output = self._items[key]
        except KeyError:
            if isinstance(self._component, base.Component):
                raise KeyError(f"Component '{self.component.name}' has no output named '{key}'")
            else:
                raise KeyError(f"There is no output named '{key}'")
        return output

    def __iter__(self) -> typing.Iterator[base.Output]:
        return self._items.values().__iter__()

    def append(self, output: base.Output) -> None:
        """
        Adds an output to the output container.

        Args:
            output: The output to add.

        Returns:
            Nothing.
        """
        self._items[output.name] = output

    @property
    def component(self) -> typing.Optional["base.Component"]:
        """
        Gets the component to which the output belongs.

        Returns:
            The output's component.
        """
        return self._component


class ProvisionalOutputs(OutputContainer):
    """An output container that generates outputs with every linked input."""

    def __init__(self, component: "base.Component", store: base.Store) -> None:
        """
        Initializes an ProvisionalOutputContainer.

        Args:
            component: The component to which the container belongs.
            store: The store used by the individual outputs.
        """
        super(ProvisionalOutputs, self).__init__(component)
        self._store = store

    def __getitem__(self, key: str) -> base.Output:
        """
        Gets an output from the container by name.

        Args:
            key: The name of the output.

        Returns:
            The output with the given name.
        """
        self._items.setdefault(key, base.Output(key, self._store, self.component))
        return self._items[key]
