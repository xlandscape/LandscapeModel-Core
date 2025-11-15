"""
Class definition of the Dose-Response Landscape Model component.
"""
import numpy as np
import base
import attrib
import typing


class DoseResponse(base.Component):
    """
    Calculates an effect based on a log-logistic dose-response function.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.DoseResponse` component")
    base.VERSION.added("1.4.1", "Changelog in `components.DoseResponse`")
    base.VERSION.changed("1.4.1", "`components.DoseResponse` class documentation")
    base.VERSION.fixed("1.4.1", "`components.DoseResponse` attrib namespace reference")
    base.VERSION.changed("1.4.9", "`components.DoseResponse` data type access")
    base.VERSION.changed("1.5.3", "`components.DoseResponse` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `components.DoseResponse`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.DoseResponse` with base class")
    base.VERSION.changed("1.12.4", "Order of exposure input scales in `components.DoseResponse`")
    base.VERSION.changed("1.12.4", "`components.DoseResponse` reports offsets of output")
    base.VERSION.changed("1.12.4", "Division warning suppressed in `components.DoseResponse`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(DoseResponse, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "SlopeFactor",
                    (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer,
                    description=
                    "The slope parameter of the log-logistic function. A float with global scale. Value has unit 1."
                ),
                base.Input(
                    "EC50",
                    (attrib.Class(float), attrib.Unit("g/ha"), attrib.Scales("global")),
                    self.default_observer,
                    description=
                    "The concentration of 50 percent effect. A float with global scale. Value has a unit g/ha."
                ),
                base.Input(
                    "Exposure",
                    (
                        attrib.Class(np.ndarray),
                        attrib.Unit("g/ha"),
                        attrib.Scales("space_y/1sqm, space_x/1sqm, time/day")
                    ),
                    self.default_observer,
                    description=
                    "The exposure for which effects are to be calculated. A NumPy array with scales time/day, "
                    "space_x/1sqm, space_y/1sqm. Values have a unit g/ha."
                )
            ]
        )
        self._outputs = base.OutputContainer(
            self,
            [
                base.Output(
                    "Effect",
                    default_store,
                    self,
                    description=
                    "The calculated effect. A NumPy array with the same scale as the exposure input. Values have a "
                    "unit of 1."
                )
            ]
        )

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        data_set_info = self._inputs["Exposure"].describe()
        slope_factor = self.inputs["SlopeFactor"].read().values
        ec50 = self.inputs["EC50"].read().values
        chunk_slices = base.chunk_slices(data_set_info["shape"], data_set_info["chunks"])
        self.outputs["Effect"].set_values(
            np.ndarray,
            chunks=data_set_info["chunks"],
            shape=data_set_info["shape"],
            data_type=data_set_info["data_type"],
            scales=data_set_info["scales"],
            unit="1",
            offset=data_set_info["offsets"]
        )
        for chunkSlice in chunk_slices:
            exposure = self.inputs["Exposure"].read(slices=chunkSlice).values
            with np.errstate(divide="ignore"):
                effect = 1 / (1 + np.exp(slope_factor * (np.log(exposure) - np.log(ec50))))
            self.outputs["Effect"].set_values(effect, slices=chunkSlice, create=False, calculate_max=True)
