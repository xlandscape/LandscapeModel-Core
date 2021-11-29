"""
Class definition of the Dose-Response Landscape Model component.
"""
import numpy as np
import base
import attrib


class DoseResponse(base.Component):
    """
    Calculates an effect based on a log-logistic dose-response function.

    INPUTS
    SlopeFactor: The slope parameter of the log-logistic function. A float with global scale. Value has unit 1.
    EC50: The concentration of 50 percent effect. A float with global scale. Value has a unit g/ha.
    Exposure: The exposure for which effects are to be calculated. A NumPy array with scales time/day, space_x/1sqm,
    space_y/1sqm. Values have a unit g/ha.

    OUTPUTS
    Effect: The calculated effect. A NumPy array with the same scale as the exposure input. Values have a unit of 1.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.DoseResponse` component")
    base.VERSION.added("1.4.1", "Changelog in `components.DoseResponse`")
    base.VERSION.changed("1.4.1", "`components.DoseResponse` class documentation")
    base.VERSION.fixed("1.4.1", "`components.DoseResponse` attrib namespace reference")
    base.VERSION.changed("1.4.9", "`components.DoseResponse` data type access")
    base.VERSION.changed("1.5.3", "`components.DoseResponse` changelog uses markdown for code elements")

    def __init__(self, name, observer, store):
        super(DoseResponse, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "SlopeFactor",
                    (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "EC50",
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
        self._outputs = base.OutputContainer(self, [base.Output("Effect", store, self)])
        return

    def run(self):
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
            unit="1"
        )
        for chunkSlice in chunk_slices:
            exposure = self.inputs["Exposure"].read(slices=chunkSlice).values
            effect = 1 / (1 + np.exp(slope_factor * (np.log(exposure) - np.log(ec50))))
            self.outputs["Effect"].set_values(effect, slices=chunkSlice, create=False, calculate_max=True)
        return
