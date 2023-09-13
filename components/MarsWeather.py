"""Class definition for the Landscape Model MarsWeather component."""
import datetime
import numpy as np
import base
import attrib
import typing


class MarsWeather(base.Component):
    """
    Provides MARS weather data from a CSV fle to the Landscape Model.

    INPUTS
    FilePath: A valid file path to a CSV file containing MARS weather data. A string of global scale. Value has no unit.
    FirstDate: The first date of the requested weather information. A `datetime.date` of global scale. The value has no
    unit.
    LastDate: The last date of the requested weather information. A `datetime.date` of global scale. The value has no
    unit.

    OUTPUTS
    TEMPERATURE_AVG: The average temperature. A NumPy array of scale time/day. Values have a unit of °C.
    """
    # CHANGELOG
    base.VERSION.added("1.2.40", "`components.MarsWeather` component")
    base.VERSION.changed("1.3.27", "`components.MarsWeather` specifies scales")
    base.VERSION.changed("1.3.33", "`components.MarsWeather` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.MarsWeather` checks for physical units")
    base.VERSION.changed(
        "1.3.33", "`components.MarsWeather` reports physical unit of average temperature to data store")
    base.VERSION.changed("1.3.33", "`components.MarsWeather` checks for scales")
    base.VERSION.changed("1.3.35", "`components.MarsWeather` no longer uses a provisional output container")
    base.VERSION.added("1.4.1", "Changelog in `components.MarsWeather` ")
    base.VERSION.changed("1.4.1", "`components.MarsWeather` class documentation")
    base.VERSION.changed("1.4.13", "added physical units to `MarsWeather` outputs")
    base.VERSION.changed("1.5.0", "`components.MarsWeather` iterates over output objects instead of names")
    base.VERSION.changed("1.5.1", "small changes in `components.MarsWeather` changelog")
    base.VERSION.changed("1.5.3", "`components.MarsWeather` changelog uses markdown for code elements")
    base.VERSION.changed("1.5.4", "`components.MarsWeather` warning if weather file misses parameters")
    base.VERSION.added("1.7.0", "Type hints to `components.MarsWeather` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.MarsWeather` with base class")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `components.MarsWeather` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.MarsWeather` ")
    base.VERSION.changed("1.11.0", "`components.MarsWeather` specifies offsets of outputs")
    base.VERSION.changed(
        "1.13.0", "`components.MarsWeather` now stores entire timeseries, regardless of simulation period")
    base.VERSION.added(
        "1.13.0", "`stores.X3dfStore` functionality to reference scale 'time/day' with native coordinates")
    base.VERSION.changed("1.15.1", "Added scale attribute to `FilePath` input of `MarsWeather` component")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a MarsWeather component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(MarsWeather, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "FilePath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global")),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output("TEMPERATURE_AVG", default_store, self),
                base.Output("PRECIPITATION", default_store, self),
                base.Output("ET0", default_store, self),
                base.Output("WINDSPEED", default_store, self),
                base.Output("RADIATION", default_store, self)
            )
        )
        self._units = {
            "TEMPERATURE_AVG": "°C",
            "PRECIPITATION": "mm/d",
            "ET0": "mm/d",
            "WINDSPEED": "m/s",
            "RADIATION": "kJ/(m²*d)"
        }

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        with open(self.inputs["FilePath"].read().values) as f:
            data = f.readlines()
        data = [line[:-1].split(",") for line in data]
        date_idx = (data[0].index("YEAR"), data[0].index("MONTH"), data[0].index("DAY"))
        first_date = datetime.date(int(data[1][date_idx[0]]), int(data[1][date_idx[1]]), int(data[1][date_idx[2]]))
        for component_output in self.outputs:
            if component_output.name in data[0]:
                idx = data[0].index(component_output.name)
                output_data = np.array([float(r[idx]) for r in data[1:]], dtype=np.float32)
                output = self.outputs[component_output.name]
                output.set_values(
                    output_data,
                    scales="time/day",
                    unit=self._units[component_output.name],
                    offset=(first_date,),
                    requires_indexing=True
                )
            else:
                self.default_observer.write_message(2, f"Weather file does not contain field {component_output.name}")
