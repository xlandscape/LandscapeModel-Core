"""
Class definition of the TER-RQ Landscape Model component.
"""
import numpy as np
import base
import attrib
import typing


class TerRQ(base.Component):
    """
    Calculates the TER and the RQ.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.TerRQ` component")
    base.VERSION.added("1.4.1", "Changelog in `components.TerRQ`")
    base.VERSION.added("1.4.1", "`components.TerRQ` class documentation")
    base.VERSION.fixed("1.4.1", "`components.TerRQ` attrib namespace reference")
    base.VERSION.changed("1.4.9", "`components.TerRQ` data type access")
    base.VERSION.changed("1.5.3", "`components.TerRQ` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `components.TerRQ`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.TerRQ` with base class")
    base.VERSION.changed("1.12.4", "Order of exposure input scales in `components.TerRQ`")
    base.VERSION.changed("1.12.4", "`components.TerRQ` reports offsets of output")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(TerRQ, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "Threshold",
                    (attrib.Class(float), attrib.Unit("g/ha"), attrib.Scales("global")),
                    self.default_observer,
                    description="The threshold applied. A float of global scale. Value has a unit of g/ha."
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
                    "The exposure considered. A NumPy array of scales time/day, space_x/1sqm, space_y/1sqm. Values "
                    "have a unit of g/ha."
                )
            ]
        )
        self._outputs = base.OutputContainer(
            self,
            [
                base.Output(
                    "TER",
                    default_store,
                    self,
                    description=
                    "The calculated TER. A NumPy array of the same scales as the exposure input. Values have a unit of "
                    "1."
                ),
                base.Output(
                    "RQ",
                    default_store,
                    self,
                    description=
                    "The calculated RQ. A NumPy array of the same scales as the exposure input. Values have a unit of "
                    "1."
                )
            ]
        )

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        data_set_info = self._inputs["Exposure"].describe()
        threshold = self.inputs["Threshold"].read().values
        chunk_slices = base.chunk_slices(data_set_info["shape"], data_set_info["chunks"])
        self.outputs["TER"].set_values(
            np.ndarray,
            chunks=data_set_info["chunks"],
            shape=data_set_info["shape"],
            data_type=data_set_info["data_type"],
            scales=data_set_info["scales"],
            unit="1",
            offset=data_set_info["offsets"]
        )
        self.outputs["RQ"].set_values(
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
            ter = np.divide(threshold, exposure, out=np.zeros_like(exposure), where=exposure > 0)
            self.outputs["TER"].set_values(ter, slices=chunkSlice, create=False, calculate_max=True)
            rq = exposure / threshold
            self.outputs["RQ"].set_values(rq, slices=chunkSlice, create=False, calculate_max=True)
