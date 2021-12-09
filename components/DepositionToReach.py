"""
Class definition of the DepositionToReach Landscape Model component.
"""
import numpy as np
import base
import attrib
import typing


class DepositionToReach(base.Component):
    """
    Calculates the initial environmental fate in reaches for spray-drift depositions.

    INPUTS
    Deposition: The substance deposited at the water surface. A NumPy array of scales time/day, space/base_geometry.
    Values have a unit of g/ha.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach. Values have no unit.
    Mapping: Maps base geometries to reaches. A list[int] of scale space/base_geometry. Values have no unit.
    SprayDriftCoverage: The fraction of a reach surface that is not exposed to spray drift. A list[float] of scale
    space/reach. Values have no unit. Currently, only values of 0 and 1 are supported.

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
    base.VERSION.added("1.7.0", "Type hints to `components.DepositionToReach` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.DepositionToReach` with base class")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `components.DepositionToReach` ")
    base.VERSION.changed("1.10.0", "`components.DepositionToReach` reports element names of `Deposition` output")
    base.VERSION.changed("1.10.0", "`components.DepositionToReach` switched to Google-style docstrings")
    base.VERSION.added("1.10.5", "Handling of covered reaches to `components.DepositionToReach` ")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a Deposition to reach component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(DepositionToReach, self).__init__(name, default_observer, default_store)
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
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer
            ),
            base.Input(
                "SprayDriftCoverage",
                (
                    attrib.Class(list[float], 1),
                    attrib.Unit(None, 1),
                    attrib.Scales("space/reach", 1),
                    attrib.InList((0, 1))
                ),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(self, (base.Output("Deposition", default_store, self),))

    def run(self) -> None:
        """Runs the component.

        Returns:
            Nothing.
        """
        reaches = self.inputs["Reaches"].read()
        mapping = self.inputs["Mapping"].read().values
        data_set_info = self.inputs["Deposition"].describe()
        if self.inputs["SprayDriftCoverage"].has_provider:
            try:
                coverage = self.inputs["SprayDriftCoverage"].read().values
            except KeyError:
                self.default_observer.write_message(
                    2,
                    "Scenario does not contain information about spray-drift coverage; assuming no coverage for all "
                    "reaches"
                )
                coverage = [0.] * self.inputs["Reaches"].describe()["shape"][0]
        else:
            self.default_observer.write_message(
                2, "Spray-drift coverage of reaches not provided; assuming no coverage for all reaches")
            coverage = [0.] * self.inputs["Reaches"].describe()["shape"][0]
        self.outputs["Deposition"].set_values(
            np.ndarray,
            shape=(data_set_info["shape"][0], reaches.values.shape[0]),
            data_type=data_set_info["data_type"],
            chunks=(data_set_info["shape"][0], 1),
            scales="time/day, space/reach",
            unit=data_set_info["unit"],
            element_names=(None, reaches.element_names[0])
        )
        for i, reachId in enumerate(reaches.values):
            reach_indexes = np.where(mapping == reachId)[0]
            if len(reach_indexes) == 1 and coverage[i] == 0:
                reach_index = int(reach_indexes)
                deposition = self.inputs["Deposition"].read(
                    slices=(slice(data_set_info["shape"][0]), reach_index)).values
                self.outputs["Deposition"].set_values(
                    deposition, slices=(slice(data_set_info["shape"][0]), i), create=False)
            elif coverage[i] != 1:
                self.default_observer.write_message(2, f"Could not map reach #{reachId}; no deposition placed")
