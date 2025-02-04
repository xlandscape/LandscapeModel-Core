"""Class definition for the Landscape Model ToxicLoad component."""
import typing
import numpy
import base
import attrib


class ToxicLoad(base.Component):
    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(ToxicLoad, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "EffectConcentration", (attrib.Class(list[float]), attrib.Unit(None), attrib.Scales("chemical/substance"))),
                base.Input(
                    "Pec",
                    (
                        attrib.Class(numpy.ndarray),
                        attrib.Unit("g"),
                        attrib.Scales("space/base_geometry, time/day, chemical/substance")
                    )
                )
            )
        )
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output(
                    "ToxicLoad",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, time/day, chemical/substance", "unit": "1"}
                ),
            )
        )

    def run(self) -> None:
        pec_description = self.inputs["Pec"].describe()
        pec_substances = pec_description["element_names"][2].get_values()
        self.outputs["ToxicLoad"].set_values(
            numpy.ndarray,
            shape=pec_description["shape"],
            chunks=pec_description["chunks"],
            element_names=pec_description["element_names"],
            geometries=pec_description["geometries"],
            offset=pec_description["offsets"]
        )
        effect_concentrations = self.inputs["EffectConcentration"].read()
        substances = effect_concentrations.element_names[0].get_values()
        ecs_values = numpy.array(effect_concentrations.values)
        for field in range(pec_description["shape"][0]):
            self.outputs["ToxicLoad"].set_values(
                (self.inputs["Pec"].read(
                    slices=(
                        slice(field, field + 1),
                        slice(pec_description["shape"][1]),
                        slice(pec_description["shape"][2])
                    )
                ).values * 1e6) / ecs_values[numpy.newaxis, numpy.newaxis, :],
                slices=(
                    slice(field, field + 1), slice(pec_description["shape"][1]), slice(pec_description["shape"][2])),
                create=False
            )
