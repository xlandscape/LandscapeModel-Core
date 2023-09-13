"""Class definition of a Landscape Model component input."""
import base
import typing
import attrib


class Input:
    """A Landscape Model component input."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Input` class for representing component inputs")
    base.VERSION.changed("1.3.13", "`base.Input` refactored")
    base.VERSION.changed("1.3.33", "`base.Input.read()` passes metadata from provider to `base.Values` object")
    base.VERSION.added("1.4.1", "Changelog in `base.Input`")
    base.VERSION.added("1.5.0", "`base.Input.description` ")
    base.VERSION.changed("1.5.3", "`base.Input` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Input` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.Input` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.Input` ")
    base.VERSION.added("1.15.0", "Messages if `base.Input` misses attributes")

    def __init__(
            self,
            name: str,
            attributes: typing.Sequence[base.DataAttribute],
            observer: typing.Optional["base.Observer"] = None,
            provider: typing.Optional[base.DataProvider] = None,
            description: typing.Optional[str] = None,
            skip_initial_attribute_checks: bool = False
    ) -> None:
        """
        Initializes an Input.

        Args:
            name: The name of the input.
            attributes: The attributes of the input.
            observer: The observer used by the input.
            provider: The provider of the input.
            description: A description of the input.
        """
        self._name = name
        self._provider = provider
        self._attributes = base.DataAttributes(attributes)
        self._messages = []
        self._observer = observer
        self._extensions = []
        self._description = description
        if observer and not skip_initial_attribute_checks:
            if not any([isinstance(x, attrib.Class) for x in attributes]):
                observer.write_message(2, f"Input {name} does not specify its data type")
            if not any([isinstance(x, attrib.Scales) for x in attributes]):
                observer.write_message(2, f"Input {name} does not specify its scales")
            if not any([isinstance(x, attrib.Unit) for x in attributes]):
                observer.write_message(2, f"Input {name} does not specify its physical unit")
            if not description or len(description) < 64:
                observer.write_message(3, f"Input {name} is missing a detailed description")

    def add_extension(self, extension: base.Extension) -> None:
        """
        Adds an extension to the input.

        Args:
            extension: The extension to add.

        Returns:
            Nothing.
        """
        self._extensions.append(extension)

    def describe(self) -> dict[str, typing.Any]:
        """
        Describes the data of the inout.

        Returns:
            A dictionary containing metadata about the input data.
        """
        return self.provider.describe()

    def read(self, **keywords) -> base.Values:
        """
        Reads values from the input.

        Args:
            keywords: Additional keywords controlling the data retrieval.

        Returns:
            The data values in their respective format.
        """
        if self._provider is None:
            raise ValueError(f"Input '{self.name}' has no provider")
        values = base.Values(self.provider.get_values(**keywords), self._extensions, **self.provider.describe())
        self._messages = []
        for attrib in self._attributes:
            check_result = attrib.check(values)
            values = check_result.adapted_values
            self._messages.append((check_result.message[0], attrib.name, check_result.message[1]))
        if self._observer is not None:
            self._observer.input_get_values(self)
        return values

    @property
    def attributes(self) -> base.DataAttributes:
        """
        Attributes associated with the input data.

        Returns:
            A list of attributes.
        """
        return self._attributes

    @property
    def messages(self) -> list[tuple[int, str]]:
        """
        Message generated by the input.

        Returns:
            A list of message strings.
        """
        return self._messages

    @property
    def name(self) -> str:
        """
        The name of the input.

        Returns:
            A string of the input's name.
        """
        return self._name

    @property
    def observer(self) -> typing.Optional["base.Observer"]:
        """
        The observer associated with the input.

        Returns:
            A Landscape Model observer.
        """
        return self._observer

    @observer.setter
    def observer(self, value: "base.Observer") -> None:
        """
        Sets the observer of the input.

        Args:
            value: The observer to be used by the input.

        Returns:
            Nothing.
        """
        self._observer = value

    @property
    def provider(self) -> typing.Optional[base.DataProvider]:
        """
        The provider of the input data.

        Returns:
            A Landscape Model data provider.
        """
        return self._provider

    @provider.setter
    def provider(self, value: base.DataProvider) -> None:
        """
        Sets the provider of the input data.

        Args:
            value: The provider to use.

        Returns:
            Nothing.
        """
        self._provider = value

    @property
    def has_provider(self) -> bool:
        """
        Indicates whether the input has a provider.

        Returns:
            True if the input has a provider else false.
        """
        return self._provider is not None

    @property
    def description(self) -> typing.Optional[str]:
        """
        A textual description of the input.

        Returns:
            A string containing the textual description of the input.
        """
        return self._description
