"""
Class definition of a Landscape Model component input.
"""
import base
import typing


class Input:
    """
    A Landscape Model component input.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Input` class for representing component inputs")
    base.VERSION.changed("1.3.13", "`base.Input` refactored")
    base.VERSION.changed("1.3.33", "`base.Input.read()` passes metadata from provider to `base.Values` object")
    base.VERSION.added("1.4.1", "Changelog in `base.Input`")
    base.VERSION.added("1.5.0", "`base.Input.description` ")
    base.VERSION.changed("1.5.3", "`base.Input` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Input` ")

    def __init__(
            self,
            name: str,
            attributes: typing.Sequence[base.DataAttribute],
            observer: typing.Optional["base.Observer"] = None,
            provider: typing.Optional[base.DataProvider] = None,
            description: typing.Optional[str] = None
    ) -> None:
        self._name = name        
        self._provider = provider
        self._attributes = base.DataAttributes(attributes)
        self._messages = []
        self._observer = observer
        self._extensions = []
        self._description = description

    def add_extension(self, extension: base.Extension) -> None:
        """
        Adds an extension to the input.
        :param extension: The extension to add.
        :return: Nothing.
        """
        self._extensions.append(extension)

    def describe(self) -> dict[str, typing.Any]:
        """
        Describes the data of the inout.
        :return: A dictionary containing metadata about the input data.
        """
        return self.provider.describe()

    def read(self, **keywords) -> base.Values:
        """
        Reads values from the input.
        :param keywords: Additional keywords controlling the data retrieval.
        :return: The data values in their respective format.
        """
        if self._provider is None:
            raise ValueError("Input '" + self._name + "' has no provider")
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
        :return: A list of attributes.
        """
        return self._attributes

    @property
    def messages(self) -> list[tuple[int, str]]:
        """
        Message generated by the input.
        :return: A list of message strings.
        """
        return self._messages

    @property
    def name(self) -> str:
        """
        The name of the input.
        :return: A string of the input's name.
        """
        return self._name

    @property
    def observer(self) -> typing.Optional["base.Observer"]:
        """
        The observer associated with the input.
        :return: A Landscape Model observer.
        """
        return self._observer

    @observer.setter
    def observer(self, value: "base.Observer") -> None:
        """
        Sets the observer of the input.
        :param value: The observer to be used by the input.
        :return: Nothing.
        """
        self._observer = value

    @property
    def provider(self) -> typing.Optional[base.DataProvider]:
        """
        The provider of the input data.
        :return: A Landscape Model data provider.
        """
        return self._provider

    @provider.setter
    def provider(self, value: base.DataProvider) -> None:
        """
        Sets the provider of the input data.
        :param value: The provider to use.
        :return: Nothing.
        """
        self._provider = value

    @property
    def has_provider(self) -> bool:
        """
        Indicates whether the input has a provider.
        :return: True if the input has a provider else false.
        """
        return self._provider is not None

    @property
    def description(self) -> typing.Optional[str]:
        """
        A textual description of the input.
        :return: A string containing the textual description of the input.
        """
        return self._description
