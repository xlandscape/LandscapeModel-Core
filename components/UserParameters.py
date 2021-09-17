"""
Class definition for the Landscape Model UserParameters component.
"""
import typing

import base


class UserParameters(base.Component):
    """
    Encapsulates a set of user-defined parameters as a Landscape Model component.

    INPUTS
    None.

    OUTPUTS
    As defined by the user parameters passed to the initialization method of the component.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`components.UserParameters` component")
    base.VERSION.changed("1.3.27", "`components.UserParameters` specifies scales")
    base.VERSION.changed("1.3.27", "`components.UserParameters` expects list of `UserParameters` as values")
    base.VERSION.added("1.3.33", "`components.UserParameters.unit` ")
    base.VERSION.changed("1.3.33", "`components.UserParameters` reports physical units to the data store")
    base.VERSION.added("1.4.1", "Changelog in `components.UserParameters` ")
    base.VERSION.changed("1.4.1", "`components.UserParameters` class documentation")
    base.VERSION.changed("1.5.3", "`components.UserParameters` changelog uses markdown for code elements")

    def __init__(
            self, name: str,
            values: typing.Sequence["UserParameter"],
            default_observer: base.Observer,
            default_store: typing.Optional[base.Store]
    ) -> None:
        super(UserParameters, self).__init__(name, default_observer, default_store)
        outputs = []
        for parameter in values:
            output = base.Output(parameter.name, default_store)
            output.set_values(parameter.values, scales=parameter.scales, unit=parameter.unit)
            outputs.append(output)
        self._outputs = base.OutputContainer(self, outputs)

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        return


class UserParameter:
    """
    A single user-defined parameter.
    """
    def __init__(
            self,
            name: str,
            values: str,
            scales: typing.Optional[str] = None,
            unit: typing.Optional[str] = None
    ) -> None:
        self._name = name
        self._values = values
        self._scales = scales
        self._unit = unit

    @property
    def name(self) -> str:
        """
        The name of the parameter.
        :return: The parameter name.
        """
        return self._name

    @property
    def values(self) -> str:
        """
        The values of the parameter.
        :return: The parameter values.
        """
        return self._values

    @property
    def scales(self) -> typing.Optional[str]:
        """
        The scales of the parameter.
        :return: The parameter scales.
        """
        return self._scales

    @property
    def unit(self) -> typing.Optional[str]:
        """
        The physical unit of the parameter.
        :return: A string representing the physical unit of the parameter.
        """
        return self._unit
