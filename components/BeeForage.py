"""Class definition for the Landscape Model BeeForage component."""
import base
import typing
import attrib
import numpy
import datetime
import openpyxl


class BeeForage(base.Component):
    """
    Simulates nectar and pollen availability to bees based on vegetation and timeseries per vegetation class.

    INPUTS
    Vegetation: Vegetation classes at a scale of space/base_geometry.
    Timeseries: A path to an Excel table containing timeseries detailing pollen and nectar availability per vegetation
    class.
    NectarPerClass: The nectar availability in L/(m²*d) for each bee forage class.
    PollenPerClass: The pollen availability in g/(m²*d) for each bee forage class.
    SimulationStart: The first day of the simulation for which bee forage availability is to be simulated.
    SimulationEnd: The last day of the simulation for which bee forage availability is to be simulated.

    OUTPUTS
    Nectar: The availability of nectar to bees in L/(m²*d) at a scale of space/base_geometry and time/day.
    Pollen: The availability of pollen to bees in g/(m²*d) at a scale of space/base_geometry and time/day.
    """
    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a BeeForage component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(BeeForage, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "Vegetation",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                    self.default_observer
                ),
                base.Input(
                    "Timeseries",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "NectarPerClass",
                    (attrib.Class(list[float]), attrib.Unit("L/(m²*d)"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "PollenPerClass",
                    (attrib.Class(list[float]), attrib.Unit("g/(m²*d)"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SimulationStart",
                    (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SimulationEnd",
                    (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                )
            )
        )
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output(
                    "Nectar", default_store, self, {"scales": "space/base_geometry, time/day", "unit": "L/(m²*d)"}),
                base.Output(
                    "Pollen", default_store, self, {"scales": "space/base_geometry, time/day", "unit": "g/(m²*d)"})
            )
        )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        timeseries_file = self.inputs["Timeseries"].read().values
        nectar_per_class = self.inputs["NectarPerClass"].read().values
        pollen_per_class = self.inputs["PollenPerClass"].read().values
        vegetation = self.inputs["Vegetation"].read()
        feature_ids = vegetation.element_names[0].get_values()
        simulation_start = self.inputs["SimulationStart"].read().values
        simulation_end = self.inputs["SimulationEnd"].read().values
        simulated_days = (simulation_end - simulation_start).days + 1
        wb = openpyxl.open(timeseries_file, True)
        mapping = {}
        for row in wb.active.iter_rows(4, values_only=True):
            if row[0]:
                mapping[row[0]] = {
                    "nectar": numpy.array(
                        [
                            nectar_per_class[
                                row[(simulation_start + datetime.timedelta(d)).month + 3]
                            ] for d in range(simulated_days)
                        ]
                    ),
                    "pollen": numpy.array(
                        [
                            pollen_per_class[
                                row[(simulation_start + datetime.timedelta(d)).month + 15]
                            ] for d in range(simulated_days)
                        ]
                    )
                }
        self.outputs["Nectar"].set_values(
            numpy.ndarray,
            shape=(len(feature_ids), simulated_days),
            chunks=(1, simulated_days),
            element_names=(vegetation.element_names[0], None),
            geometries=(vegetation.geometries[0], None),
            offset=(None, simulation_start)
        )
        self.outputs["Pollen"].set_values(
            numpy.ndarray,
            shape=(len(feature_ids), simulated_days),
            chunks=(1, simulated_days),
            element_names=(vegetation.element_names[0], None),
            geometries=(vegetation.geometries[0], None),
            offset=(None, simulation_start)
        )
        for i, vegetation_class in enumerate(vegetation.values):
            vegetation_class_timeseries = mapping.get(vegetation_class)
            if vegetation_class_timeseries is None:
                self.default_observer.write_message(
                    2, f"No bee forage defined for vegetation class {vegetation_class} (feature {feature_ids[i]})")
            else:
                if numpy.count_nonzero(vegetation_class_timeseries["nectar"]) > 0:
                    nectar_per_day = mapping[vegetation_class]["nectar"]
                    nectar_per_day.shape = (1, simulated_days)
                    self.outputs["Nectar"].set_values(
                        nectar_per_day, slices=(i, slice(0, simulated_days)), create=False)
                    pollen_per_day = mapping[vegetation_class]["pollen"]
                    pollen_per_day.shape = (1, simulated_days)
                    self.outputs["Pollen"].set_values(
                        pollen_per_day, slices=(i, slice(0, simulated_days)), create=False)
