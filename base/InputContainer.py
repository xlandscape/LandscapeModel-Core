"""
Class definition of the Landscape Model InputContainer class.
"""
import base
import typing


class InputContainer:
    """
    A container for component inputs.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.InputContainer` class for collecting the inputs of a component")
    base.VERSION.added("1.2.3", "Added `base.InputContainer.append()` and `.__contains__()` ")
    base.VERSION.changed("1.3.33", "`base.InputContainer` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.InputContainer` ")
    base.VERSION.changed("1.5.3", "`base.InputContainer` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.InputContainer` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.InputContainer` ")

    def __init__(
            self,
            component: typing.Optional["base.Component"] = None,
            inputs: typing.Optional[typing.Sequence[base.Input]] = None
    ) -> None:
        self._items = {}
        self._component = component
        if inputs is not None:
            for component_input in inputs:
                self._items[component_input.name] = component_input

    def __contains__(self, item: base.Input) -> bool:
        return item in self._items

    def __getitem__(self, key: str) -> base.Input:
        try:
            component_input = self._items[key]
        except KeyError:
            if isinstance(self._component, base.Component):
                raise KeyError(f"Component '{self.component.name}' has no input named '{key}'")
            else:
                raise KeyError(f"There is no output named '{key}'")
        return component_input

    def __setitem__(self, key: str, value: base.Output) -> None:
        self[key].provider = base.DataProvider(value)

    def __iter__(self) -> typing.Iterator[base.Input]:
        return self._items.values().__iter__()

    def append(self, component_input: base.Input) -> None:
        """
        Appends an input to the input container.
        :param component_input: The input to append.
        :return: Nothing.
        """
        self._items[component_input.name] = component_input

    @property
    def component(self) -> typing.Optional["base.Component"]:
        """
        Gets the component to which the input container belongs.
        :return: The component of the input container.
        """
        return self._component
