"""
Class definition of the TER-RQ Landscape Model component.
"""
import numpy as np
import base
import attrib


class TerRQ(base.Component):
    """
    Calculates the TER and the RQ.

    INPUTS
    Threshold: The threshold applied. A float of global scale. Value has a unit of g/ha.
    Exposure: The exposure considered. A NumPy array of scales time/day, space_x/1sqm, space_y/1sqm. Values have a unit
    of g/ha.

    OUTPUTS
    TER: The calculated TER. A NumPy array of the same scales as the exposure input. Values have a unit of 1.
    RQ: The calculated RQ. A NumPy array of the same scales as the exposure input. Values have a unit of 1.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "components.TerRQ component")
    base.VERSION.added("1.4.1", "Changelog in components.TerRQ")
    base.VERSION.added("1.4.1", "components.TerRQ class documentation")
    base.VERSION.fixed("1.4.1", "components.TerRQ attrib namespace reference")

    def __init__(self, name, observer, store):
        super(TerRQ, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "Threshold",
                    (attrib.Class(float), attrib.Unit("g/ha"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "Exposure",
                    (
                        attrib.Class(np.ndarray),
                        attrib.Unit("g/ha"),
                        attrib.Scales("time/day, space_x/1sqm, space_y/1sqm")
                    ),
                    self.default_observer
                )
            ]
        )
        self._outputs = base.OutputContainer(self, [base.Output("TER", store, self), base.Output("RQ", store, self)])
        return

    def run(self):
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
            unit="1"
        )
        self.outputs["RQ"].set_values(
            np.ndarray,
            chunks=data_set_info["chunks"],
            shape=data_set_info["shape"],
            data_type=data_set_info["data_type"],
            scales=data_set_info["scales"],
            unit="1"
        )
        for chunkSlice in chunk_slices:
            exposure = self.inputs["Exposure"].read(slices=chunkSlice).values
            ter = np.divide(threshold, exposure, out=np.zeros_like(exposure), where=exposure > 0)
            self.outputs["TER"].set_values(ter, slices=chunkSlice, create=False, calculate_max=True)
            rq = exposure / threshold
            self.outputs["RQ"].set_values(rq, slices=chunkSlice, create=False, calculate_max=True)
        return
