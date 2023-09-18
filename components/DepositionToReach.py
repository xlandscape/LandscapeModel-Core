"""
Class definition of the DepositionToReach Landscape Model component.
"""
import os.path

import numpy as np
import base
import attrib
import typing
import datetime


class DepositionToReach(base.Component):
    """
    Calculates the average spray-drift deposition for reaches based on spray-drift depositions reported for base
    geometries. Base geometries are mapped to reaches, whereby the base geometry should represent an average uncovered
    area of the reach. For cases, where the base geometries contain areas of reaches that are actually covered (e.g.,
    underground), the `DepositionToReach` component allows to explicitly state this fact and exclude the reaches from
    reception of spray-drift deposition. The component has also a mode where depositions are load from a CSV file,
    which helps in simulations where spray-drift depositions are not simulated bit are known from other sources.

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
    base.VERSION.changed("1.11.0", "`components.DepositionToReach` allows predefining deposition in a CSV file")
    base.VERSION.fixed(
        "1.12.3", "Removed warning for unused deposition from file `components.DepositionToReach` if path is specified")
    base.VERSION.fixed(
        "1.14.4", "Fixed dimensionality of `Deposition` output in `components.DepositionToReach` component")
    base.VERSION.changed("1.15.1", "Included types in `DepositionToReach` input attributes")

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
                (attrib.Class(np.ndarray), attrib.Unit("g/ha"), attrib.Scales("time/day, space/base_geometry")),
                self.default_observer,
                description="The rate at which the substance is deposited at the water surface. The values of this "
                            "input should represent an average over the uncovered area of the reach, but the maximum "
                            "of the day."
            ),
            base.Input(
                "Reaches",
                (attrib.Class(np.ndarray), attrib.Unit(None), attrib.Scales("space/reach")),
                self.default_observer,
                description="The identifiers of individual reaches. This information is used alongside the values of "
                            "the `Mapping` input to associate individual reaches to their base geometries representing "
                            "average uncovered reach surfaces."
            ),
            base.Input(
                "Mapping",
                (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                self.default_observer,
                description="Maps base geometries to reaches. Each reach should be represented also as a base geometry "
                            "showing its average uncovered area if it is at least partially exposed to spray-drift."
            ),
            base.Input(
                "SprayDriftCoverage",
                (
                    attrib.Class(list[float]),
                    attrib.Unit("1"),
                    attrib.Scales("space/base_geometry"),
                    attrib.InList((0., 1.))
                ),
                self.default_observer,
                description="The fraction of a reach surface that is not exposed to spray drift. If this value is `0`, "
                            "the spray-deposition reported for the base geometry is also reported for the reach. If "
                            "the value is `1`, a deposition of `0` is reported instead. Allowing to set the coverage "
                            "of reaches to `1` helps in scenarios, where, e.g., the geodata does not differentiate "
                            "between under- and overground reaches."
            ),
            base.Input(
                "DepositionInputSource",
                (
                    attrib.Unit(None),
                    attrib.Scales("global"),
                    attrib.InList(("DepositionInput", "DepositionInputFile")),
                    attrib.Class(str)
                ),
                self.default_observer,
                description="Specifies from what source the deposition input is retrieved. If set to "
                            "`DepositionInputFile`, the data is read from the `DepositionInputFile`. In this case, all "
                            "other inputs are ignored and the deposition reported for each reach is entirely "
                            "determined by the values in the input file. Reaches not listed there will receive a "
                            "deposition of `0`. If the `DepositionInputSource` is set to `DepositionInput`, the value "
                            "of the `DepositionInputFile` input is ignored."
            ),
            base.Input(
                "DepositionInputFile",
                (attrib.Unit(None), attrib.Scales("global"), attrib.Class(str)),
                self.default_observer,
                description="The path to a CSV file containing predefined depositions in g/ha per reach and day. The "
                            "CSV file must have an arbitrary header row and data rows consisting of the date of "
                            "exposure in the format `%Y-%m-%d`, the numerical identifier of the reach that is exposed "
                            "and the value of deposition as a floating point number in g/ha."
            )
        ])
        self._outputs = base.OutputContainer(self, (base.Output("Deposition", default_store, self),))
        if self.default_observer:
            self.default_observer.write_message(
                2,
                "DepositionToReach currently does not check the identity of base geometries",
                "Make sure that inputs of scale space/base_geometry retrieve data in the same base geometry-order"
            )

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
            element_names=(None, reaches.element_names[0]),
            offset=(data_set_info["offsets"])
        )
        deposition_input_source = self.inputs["DepositionInputSource"].read().values
        deposition_input_file = self.inputs["DepositionInputFile"].read().values
        if deposition_input_source == "DepositionInput":
            if os.path.isfile(deposition_input_file):
                self.default_observer.write_message(
                    2,
                    "Deposition configured to be taken from input, but deposition file specified; file will be ignored"
                )
            for i, reachId in enumerate(reaches.values):
                reach_indexes = np.where(mapping == reachId)[0]
                if len(reach_indexes) == 1 and coverage[i] == 0:
                    reach_index = int(reach_indexes)
                    deposition = self.inputs["Deposition"].read(
                        slices=(slice(data_set_info["shape"][0]), slice(reach_index, reach_index + 1))).values
                    self.outputs["Deposition"].set_values(
                        deposition, slices=(slice(data_set_info["shape"][0]), slice(i, i + 1)), create=False)
                elif coverage[i] != 1:
                    self.default_observer.write_message(2, f"Could not map reach #{reachId}; no deposition placed")
        elif deposition_input_source == "DepositionInputFile":
            self.default_observer.write_message(
                2, "Input file configured as deposition source; values provided by deposition input are ignored")
            with open(deposition_input_file) as f:
                f.readline()
                for line in f:
                    data = line[:-1].split(",")
                    time_index = (
                            datetime.datetime.strptime(data[0], "%Y-%m-%d").date() - data_set_info["offsets"][0]).days
                    reach_indexes = np.where(reaches.values == np.array(int(data[1])))[0]
                    if len(reach_indexes) == 1:
                        reach_index = int(reach_indexes)
                        self.outputs["Deposition"].set_values(
                            np.array(float(data[2])), slices=(time_index, reach_index), create=False)
                    else:
                        self.default_observer.write_message(
                            2, f"Could not map reach #{reach_index}; no deposition placed")
        else:
            raise ValueError(f"Unknown deposition source: {deposition_input_source}")
