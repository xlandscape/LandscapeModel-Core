"""Class definition of a Landscape Model component output."""
import base
import typing


class Output:
    """A Landscape Model component output."""
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
    base.VERSION.fixed("1.5.6", "Handling of omitted `base.Output` attribute hints")
    base.VERSION.added("1.7.0", "Type hints to `base.Output` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.Output` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.Output` ")
    base.VERSION.added("1.15.0", "Messages if `base.Output` misses descriptions")
    base.VERSION.added("1.15.8", "Possibility to skip initial attribute checks for `base.Output`")

    def __init__(
            self,
            name: str,
            store: base.Store,
            component: typing.Optional["base.Component"] = None,
            default_attributes: typing.Optional[typing.Mapping[str, typing.Any]] = None,
            description: typing.Optional[str] = None,
            attribute_hints: typing.Optional[typing.Mapping[str, typing.Any]] = None,
            skip_initial_attribute_checks: bool = False
    ) -> None:
        """
        Initializes an output.

        Args:
            name: The name of the output.
            store: The store associated with the output.
            component: The component to which the output belongs.
            default_attributes: The default attributes of the output.
            description: A description of the output.
            attribute_hints: Documentation hints of the output.
        """
        self._name = name
        self._store = store
        self._component = component
        if component is None:
            self._storeName = name
        else:
            self._storeName = f"{component.name}/{name}"
        self._default_attributes = {} if default_attributes is None else default_attributes
        self._description = description
        self._attribute_hints = {} if attribute_hints is None else attribute_hints
        if component and component.default_observer and not skip_initial_attribute_checks:
            if not default_attributes:
                component.default_observer.write_message(3, f"Output {name} is missing default attributes")
            if not description or len(description) < 64:
                component.default_observer.write_message(3, f"Output {name} is missing a detailed description")
            if not attribute_hints:
                component.default_observer.write_message(3, f"Output {name} is missing attribute hints")

    def describe(self) -> dict[str, typing.Any]:
        """
        Describes the data provided by the output.

        Returns:
            Nothing.
        """
        return self.store.describe(self.store_name)

    def get_values(self, **keywords) -> typing.Any:
        """
        Gets the values from te output.

        Args:
            **keywords: Additional keywords controlling the data retrieval.

        Returns:
            The values in their respective format.
        """
        values = self.store.get_values(self.store_name, **keywords)
        return values

    def set_values(self, values: typing.Any, **keywords) -> None:
        """
        Sets the values of the output.

        Args:
            values: The new vales for the output.
            **keywords: Additional keywords controlling the data storage.

        Returns:
            Nothing.
        """
        for attribute, value in self._default_attributes.items():
            if attribute not in keywords:
                keywords[attribute] = value
        self.store.set_values(self.store_name, values, **keywords)

    @property
    def component(self) -> typing.Optional["base.Component"]:
        """
        The component to which the output belongs.

        Returns:
            A Landscape Model component.
        """
        return self._component

    @property
    def name(self) -> str:
        """
        The name of the output.

        Returns:
            A string of the output name.
        """
        return self._name

    @property
    def store(self) -> base.Store:
        """
        The store that is used by the output to store data.

        Returns:
            A Landscape model data store.
        """
        return self._store

    @property
    def store_name(self) -> str:
        """
        The name of the data store that is used by the output.

        Returns:
            A string of the data store name.
        """
        return self._storeName

    @property
    def default_attributes(self) -> dict[str, typing.Any]:
        """
        A set of default attributes associated with the output.

        Returns:
            A dictionary of attribute names and their default value.
        """
        return self._default_attributes

    @property
    def description(self) -> str:
        """
        A textual description of the input.

        Returns:
            A string containing the textual description of the input.
        """
        return self._description

    @property
    def attribute_hints(self) -> dict[str, typing.Any]:
        """
        Contains hints about data attributes useful for the documentation of the output.

        Returns:
            A dictionary of attribute types and textual or object hints.
        """
        return self._attribute_hints
