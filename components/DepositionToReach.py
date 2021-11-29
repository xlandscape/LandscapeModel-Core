"""
Class definition of the DepositionToReach Landscape Model component.
"""
import numpy as np
import base
import attrib


class DepositionToReach(base.Component):
    """
    Calculates the initial environmental fate in reaches for spray-drift depositions.

    INPUTS
    Deposition: The substance deposited at the water surface. A NumPy array of scales time/day, space/base_geometry.
    Values have a unit of g/ha.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach. Values have no unit.
    Mapping: Maps base geometries to reaches. A list[int] of scale space/base_geometry. Values have no unit.

    OUTPUTS
    Deposition: The substance deposited at the water surface for reaches. A NumPy array of scales time/day, space/reach.
    Values have the same unit as the input deposition.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach.
    """
    # CHANGELOG
    base.VERSION.added("1.2.3", "`components.DepositionToReach` component stub")
    base.VERSION.changed("1.2.20", "`components.DepositionToReach` basic implementation")
    base.VERSION.changed("1.2.28", "`components.DepositionToReach` outputs reach identifiers")
    base.VERSION.changed("1.3.27", "`components.DepositionToReach` specifies scales")
    base.VERSION.changed("1.3.33", "`components.DepositionToReach` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.DepositionToReach` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.DepositionToReach` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.DepositionToReach` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.DepositionToReach`")
    base.VERSION.changed("1.4.1", "`components.DepositionToReach` class documentation")
    base.VERSION.changed("1.4.9", "`components.DepositionToReach` data type access")
    base.VERSION.changed("1.5.3", "`components.DepositionToReach` changelog uses markdown for code elements")

    def __init__(self, name, observer, store):
        super(DepositionToReach, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Deposition",
                (
                    attrib.Class(np.ndarray, 1),
                    attrib.Unit("g/ha", 1),
                    attrib.Scales("time/day, space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "Reaches",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "Mapping",
                (attrib.Class("list[int]", 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("Deposition", store, self),
            base.Output("Reaches", store, self)
        ])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        reaches = self.inputs["Reaches"].read().values
        mapping = self.inputs["Mapping"].read().values
        data_set_info = self.inputs["Deposition"].describe()
        # noinspection SpellCheckingInspection
        self.outputs["Deposition"].set_values(
            np.ndarray,
            shape=(data_set_info["shape"][0], reaches.shape[0]),
            data_type=data_set_info["data_type"],
            chunks=(data_set_info["shape"][0], 1),
            scales="time/day, space/reach",
            unit=data_set_info["unit"]
        )
        for i, reachId in enumerate(reaches):
            reach_indexes = np.where(mapping == reachId)[0]
            if len(reach_indexes) == 1:
                reach_index = int(reach_indexes)
                deposition = self.inputs["Deposition"].read(
                    slices=(slice(data_set_info["shape"][0]), reach_index)).values
                self.outputs["Deposition"].set_values(deposition, slices=(slice(data_set_info["shape"][0]), i),
                                                      create=False)
            else:
                self.default_observer.write_message(2, "Could not map reach #" + str(reachId))
        self.outputs["Reaches"].set_values(reaches, scales="space/reach")
        return
