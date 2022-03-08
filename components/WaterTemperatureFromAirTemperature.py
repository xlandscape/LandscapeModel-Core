"""Class definition of the Landscape Model WaterTemperatureFromAirTemperature component."""
import base
import typing
import attrib
import numpy as np


class WaterTemperatureFromAirTemperature(base.Component):
    """
    A simple component that takes a series of daily average air temperatures and calculates a series of daily water
    temperatures by averaging the air temperatures of the current and the two preceding days. The water temperatures
    of the first two days are set to the one calculated for the third day.

    INPUTS
    AirTemperature: A timeseries of daily average air temperatures.

    OUTPUTS
    WaterTemperature: A timeseries of daily average water temperatures.
    """
    # CHANGELOG
    base.VERSION.added("1.13.0", "`components.WaterTemperatureFromAirTemperature` component")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(WaterTemperatureFromAirTemperature, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, (
            base.Input(
                "AirTemperature",
                (attrib.Class(np.ndarray), attrib.Scales("time/day"), attrib.Unit("°C")),
                self.default_observer
            ),
        ))
        self._outputs = base.OutputContainer(
            self,
            [
                base.Output(
                    "WaterTemperature",
                    default_store,
                    self,
                    {"scales": "time/day", "unit": "°C", "requires_indexing": True}
                )
            ]
        )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        air_temperature = self.inputs["AirTemperature"].read(select={"time/day": "all"})
        cumulated_temperature = np.cumsum(np.insert(air_temperature.values, 0, 0))
        water_temperature = (cumulated_temperature[3:] - cumulated_temperature[:-3]) / 3
        water_temperature = np.round(np.insert(water_temperature, 0, [water_temperature[0], water_temperature[0]]), 2)
        self.outputs["WaterTemperature"].set_values(water_temperature, offset=air_temperature.offsets)
