"""Class definition for the Landscape Model Soil component."""
import numpy
import base
import attrib
import typing
import sqlite3


class Soil(base.Component):
    """
    Reads soil information from a SQLite database and provides it to the landscape model.
    """
    # CHANGELOG
    base.VERSION.added("1.16.0", "`components.Soil` component")
    base.VERSION.changed("1.16.2", "Renamed scale other/soil_layer to other/soil_horizon")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a MarsWeather component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(Soil, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input("FilePath", (attrib.Class(str, 1), attrib.Unit(None, 1)), self.default_observer),
            base.Input(
                "SoilTypes",
                (attrib.Class(list[str]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output(
                    "HeightOfSublayer",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "cm"}
                ),
                base.Output(
                    "HeightOfCompartmentsInLayer",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "cm"}
                ),
                base.Output(
                    "NumberOfCompartmentsInLayer",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "ResidualWaterContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "SaturatedWaterContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "AlphaOfMainDryingCurve",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1/cm"}
                ),
                base.Output(
                    "ShapeParameterN",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "SaturatedVerticalHydraulicConductivity",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "cm/d"}
                ),
                base.Output(
                    "ExponentInHydraulicConductivityFunction",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "AlphaOfMainWettingCurve",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1/cm"}
                ),
                base.Output(
                    "EntryPressureHead",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "cm"}
                ),
                base.Output(
                    "SandContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "SiltContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "ClayContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "OrganicMatterContent",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}
                ),
                base.Output(
                    "pH", default_store, self, {"scales": "space/base_geometry, other/soil_horizon", "unit": "1"}),
                base.Output(
                    "Density",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "kg/m³"}
                ),
                base.Output(
                    "LenDisLiq",
                    default_store,
                    self,
                    {"scales": "space/base_geometry, other/soil_horizon", "unit": "m"}
                )
            )
        )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        with sqlite3.connect(self.inputs["FilePath"].read().values) as db:
            soils_data = {
                (x[0], x[1]): x[2:] for x in
                db.execute("""
                SELECT SOIL_ID, ISOILLAY, HSUBLAY, HCOMP, NCOMP, ORES, OSAT, ALPHA, NPAR, KSAT, LEXP, ALPHAW, H_ENPR, 
                    FraSand, FraSilt, FraClay, CntOm, pH, "table horizon", "Table horizon LenDisLiq (m)"
                FROM soils
                ORDER BY SMU, ISOILLAY, HSUBLAY
                """).fetchall()
            }
        max_number_soil_layers = max([x[1] for x in soils_data])
        soil_types = self.inputs["SoilTypes"].read()
        for i, soil_parameter in enumerate(
            (
                    "HeightOfSublayer",
                    "HeightOfCompartmentsInLayer",
                    "NumberOfCompartmentsInLayer",
                    "ResidualWaterContent",
                    "SaturatedWaterContent",
                    "AlphaOfMainDryingCurve",
                    "ShapeParameterN",
                    "SaturatedVerticalHydraulicConductivity",
                    "ExponentInHydraulicConductivityFunction",
                    "AlphaOfMainWettingCurve",
                    "EntryPressureHead",
                    "SandContent",
                    "SiltContent",
                    "ClayContent",
                    "OrganicMatterContent",
                    "pH",
                    "Density",
                    "LenDisLiq"
            )
        ):

            data = numpy.full((len(soil_types.values), max_number_soil_layers), numpy.nan)
            for j, soil_type in enumerate(soil_types.values):
                parameter = numpy.asarray([x[1][i] for x in soils_data.items() if x[0][0] == soil_type])
                data[j, :parameter.shape[0]] = parameter
            self.outputs[soil_parameter].set_values(
                data,
                chunks=(1, max_number_soil_layers),
                shape=(len(soil_types.values), max_number_soil_layers),
                data_type=numpy.float_,
                element_names=(soil_types.element_names[0], None),
                geometries=(soil_types.geometries[0], None)
            )
