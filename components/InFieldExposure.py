"""Class definition for the Landscape Model InFieldExposure component."""
import typing
import datetime
import numpy
import math
import shapely.wkb
import base
import attrib


class InFieldExposure(base.Component):
    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(InFieldExposure, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "SimulationStart", (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global"))),
                base.Input("SimulationEnd", (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global"))),
                base.Input(
                    "BaseFeatures", (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("space/base_geometry"))),
                base.Input("DT50", (attrib.Class(list[float]), attrib.Unit("d"), attrib.Scales("chemical/substance"))),
                base.Input(
                    "AppliedField",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("other/application"))
                ),
                base.Input(
                    "ApplicationDate",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("other/application"))
                ),
                base.Input(
                    "AppliedSubstance",
                    (attrib.Class(numpy.ndarray), attrib.Unit(None), attrib.Scales("other/application"))
                ),
                base.Input(
                    "ApplicationRate",
                    (attrib.Class(numpy.ndarray), attrib.Unit("g/ha"), attrib.Scales("other/application"))
                )
            )
        )
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output(
                    "Pec",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, time/day, chemical/substance", "unit": "g"}
                ),
            )
        )

    def run(self) -> None:
        simulation_start = self.inputs["SimulationStart"].read().values
        simulated_days = (self.inputs["SimulationEnd"].read().values - simulation_start).days + 1
        base_features = self.inputs["BaseFeatures"].read()
        dt50 = self.inputs["DT50"].read()
        considered_substances = dt50.element_names[0].get_values()
        self.outputs["Pec"].set_values(
            numpy.ndarray,
            shape=(len(base_features.values), simulated_days, len(considered_substances)),
            chunks=(1, simulated_days, len(considered_substances)),
            element_names=(base_features.element_names[0], None, dt50.element_names[0]),
            geometries=(base_features.geometries[0], None, None),
            offset=(None, simulation_start, None),
            default=0
        )
        applied_field = self.inputs["AppliedField"].read()
        applied_substance = self.inputs["AppliedSubstance"].read().values
        application_date = self.inputs["ApplicationDate"].read().values
        applied_rate = self.inputs["ApplicationRate"].read().values
        applications = {}
        for i in range(applied_field.values.shape[0]):
            applications.setdefault(
                (applied_field.values[i]), {}
            ).setdefault(
                applied_substance[i], []
            ).append(
                (application_date[i], applied_rate[i])
            )
        for field, substances in applications.items():
            spatial_index = base_features.values.index(field)
            area = shapely.wkb.loads(base_features.geometries[0].get_values(slices=(spatial_index,))[0]).area
            for substance, events in substances.items():
                chemical_index = considered_substances.index(substance)
                time_series = numpy.zeros((1, simulated_days, 1))
                for event in events:
                    time_series[
                        0,
                        (datetime.datetime.fromordinal(event[0]).date() - simulation_start).days,
                        0
                    ] = event[1] * area / 1e4
                for t in range(1, time_series.shape[1]):
                    time_series[0, t, 0] = (
                            time_series[0, t, 0] +
                            time_series[0, t - 1, 0] * math.exp(-math.log(2) / dt50.values[chemical_index])
                    )
                self.outputs["Pec"].set_values(
                    time_series,
                    slices=(
                        slice(spatial_index, spatial_index + 1),
                        slice(time_series.shape[1]),
                        slice(chemical_index, chemical_index + 1)
                    ),
                    create=False
                )
