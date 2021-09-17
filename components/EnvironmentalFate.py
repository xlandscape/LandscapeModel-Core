"""
Class definition for the Landscape Model EnvironmentalFate component.
"""
import math
import numpy as np
import base
import attrib
import typing


class EnvironmentalFate(base.Component):
    """
    Calculates environmental fate based on a simple half-time degradation.

    INPUTS
    SprayDriftExposure: The exposure due to spray-drift.
    RunOfExposure: The exposure due to run-off.
    SoilDT50: The half-time for substance degradation in soil.

    OUTPUTS
    Pec: The concentration of substance considering exposure and degradation. A NumPy array of scales time/day,
    space_x/1sqm, space_y/1sqm.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`components.EnvironmentalFate` component")
    base.VERSION.changed("1.1.2", "`components.EnvironmentalFate` exposure inputs made optional")
    base.VERSION.changed("1.1.5", "`components.EnvironmentalFate` stores metadata of PEC")
    base.VERSION.changed("1.3.27", "`components.EnvironmentalFate` refactored")
    base.VERSION.added("1.4.1", "Changelog in `components.EnvironmentalFate`")
    base.VERSION.changed("1.4.1", "`components.EnvironmentalFate` class documentation")
    base.VERSION.changed("1.4.9", "renamed `components.EnvironmentalFate` component")
    base.VERSION.changed("1.4.14", "added semantic descriptions to `EnvironmentalFate` component")
    base.VERSION.added("1.7.0", "Type hints to `components.EnvironmentalFate` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.EnvironmentalFate` with base class")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(EnvironmentalFate, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, (
            base.Input(
                "SprayDriftExposure",
                (attrib.Class(np.ndarray), attrib.Scales("time/day, space_x/1sqm, space_y/1sqm"), attrib.Unit("g/ha")),
                self.default_observer
            ),
            base.Input(
                "RunOffExposure",
                (attrib.Class(np.ndarray), attrib.Scales("time/day, space_x/1sqm, space_y/1sqm"), attrib.Unit("g/ha")),
                self.default_observer),
            base.Input(
                "SoilDT50", (attrib.Class(float), attrib.Scales("global"), attrib.Unit("d")), self.default_observer)
        ))
        self._outputs = base.OutputContainer(self, [base.Output("Pec", default_store, self)])

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        enabled_exposure_inputs = []
        if self.inputs["SprayDriftExposure"].provider is not None:
            enabled_exposure_inputs.append(self.inputs["SprayDriftExposure"])
        if self.inputs["RunOffExposure"].provider is not None:
            enabled_exposure_inputs.append(self.inputs["RunOffExposure"])
        data_set_info = enabled_exposure_inputs[0].describe()
        soil_dt50 = self.inputs["SoilDT50"].read().values
        self.outputs["Pec"].set_values(
            np.ndarray,
            shape=data_set_info["shape"],
            data_type=data_set_info["data_type"],
            chunks=base.chunk_size(
                (1, None, None),
                (data_set_info["shape"][0], data_set_info["shape"][1], data_set_info["shape"][2])
            ),
            scales="time/day, space_x/1sqm, space_y/1sqm",
            unit="g/ha"
        )
        pec_current_day = np.zeros(
            (1, data_set_info["shape"][1], data_set_info["shape"][2]), data_set_info["data_type"])
        for t in range(data_set_info["shape"][0]):
            current_slice = (slice(t, t + 1), slice(0, data_set_info["shape"][1]), slice(0, data_set_info["shape"][2]))
            pec_current_day *= math.exp(-math.log(2) / soil_dt50)
            for exposureInput in enabled_exposure_inputs:
                pec_current_day += exposureInput.read(slices=current_slice).values
            self.outputs["Pec"].set_values(pec_current_day, create=False, slices=current_slice, calculate_max=True)
