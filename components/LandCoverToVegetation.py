"""Class definition for the Landscape Model LandCoverToVegetation component."""
import base
import typing
import attrib
import openpyxl
import json
import numpy


class LandCoverToVegetation(base.Component):
    """
    Translates land cover into vegetation information using a simple lookup-table approach.

    INPUTS
    LandCover: A list of integer identifiers that detail the land use / land cover type of individual elements at scale
    space/base_geometry. Identifiers have no units.
    Mapping: A file path to an Excel workbook that contains information on how to map land cover classes into
    vegetation classes.
    VegetationClasses: A JSON file containing defined vegetation classes and their numerical code.

    OUTPUTS
    Vegetation: A list of vegetation classes at a space/base_geometry scale.
    """
    # CHANGELOG
    base.VERSION.added("1.14.0", "`components.LandCoverToVegetation` ")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a LandCoverToVegetation component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(LandCoverToVegetation, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "LandCover",
                    (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                    self.default_observer
                ),
                base.Input(
                    "Mapping", (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")), self.default_observer),
                base.Input(
                    "VegetationClasses",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                )
            )
        )
        self._outputs = base.OutputContainer(
            self, (base.Output("Vegetation", default_store, self, {"scales": "space/base_geometry", "unit": None}),))

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        land_cover = self.inputs["LandCover"].read()
        mapping_file = self.inputs["Mapping"].read().values
        vegetation_classes = self.inputs["VegetationClasses"].read().values
        wb = openpyxl.open(mapping_file, True)
        mapping = {}
        with open(vegetation_classes) as f:
            vegetation_classes = json.load(f)
        for row in wb.active.iter_rows(4, values_only=True):
            if row[4] is None or row[9] is None:
                self.default_observer.write_message(2, f"No vegetation defined for land cover class {row[4]}")
            else:
                vegetation_class = vegetation_classes.get(row[9])
                if not vegetation_class:
                    self.default_observer.write_message(1, f"Unknown vegetation land cover class {row[4]}: {row[9]}")
                else:
                    mapping[row[4]] = vegetation_class
        vegetation = numpy.zeros_like(land_cover.values)
        for i, feature_land_cover in enumerate(land_cover.values):
            feature_vegetation_class = mapping.get(feature_land_cover)
            if feature_vegetation_class is None:
                self.default_observer.write_message(
                    2, f"Unknown vegetation class for land cover class {feature_land_cover}")
            else:
                vegetation[i] = feature_vegetation_class
        self.outputs["Vegetation"].set_values(
            vegetation, element_names=land_cover.element_names, geometries=land_cover.geometries)
