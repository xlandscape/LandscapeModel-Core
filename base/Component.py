"""Class definition of the Landscape Model component class."""
import base
import typing


class Component:
    """The base type for all Landscape Model components."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Component` class representing Landscape Model components")
    base.VERSION.changed("1.3.33", "`base.Component` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Component`")
    base.VERSION.changed("1.5.3", "`base.Component` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Component`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.Component`")
    base.VERSION.changed("1.18.0", "Code refactory in `base.Component`")

    VERSION: base.VersionCollection

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        self._inputs = base.InputContainer(self)
        self._name = name
        self._outputs = base.OutputContainer(self)
        self._defaultObserver = default_observer
        self._defaultStore = default_store
        self._module = None

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        raise NotImplementedError

    @property
    def default_observer(self) -> base.Observer:
        """
        Gets the default observer of the component.

        Returns:
            The default observer of the component.
        """
        return self._defaultObserver

    @property
    def default_store(self) -> base.Store:
        """
        Gets the default store of the component.

        Returns:
            The default store of the component.
        """
        return self._defaultStore

    @property
    def inputs(self) -> base.InputContainer:
        """
        Gets the inputs of the component.

        Returns:
            The inputs of the component.
        """
        return self._inputs

    @property
    def name(self) -> str:
        """
        Gets the name of the component.

        Returns:
            A string containing the name of the component.
        """
        return self._name

    @property
    def outputs(self) -> base.OutputContainer:
        """
        Gets the outputs of the component.

        Returns:
            The outputs of the component.
        """
        return self._outputs

    @property
    def module(self) -> base.Module:
        """
        Gets the module used by the component.

        Returns:
            The module used by the component.
        """
        return self._module
