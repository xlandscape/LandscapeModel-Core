"""Class definition for the Landscape Model LandscapeScenario component."""
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
import base
import xml.etree.ElementTree
import attrib
import numpy as np
import typing
import xmlschema
import re


class LandscapeScenario(base.Component):
    """
    Provides geospatial data of landscape scenarios to the Landscape Model. The geospatial data normally consists of a
    set of one or more shapefiles, accompanied by an arbitrary number of GeoTIFFs. The data package also includes an
    XML file named `package.xinfo` that details the contents of the package and provides metainformation about the
    package. It also links individual pieces of information, e.g., individual columns of the shapefiles' attributes, to
    an informal Landscape Model vocabulary. The set of outputs of the `LandscapeScenario` component differs on the kind
    of scenario (e.g., off-field soil scenarios versus aquatic scenarios) and is defined by an XML schema (see input
    descriptions for details). Some outputs are generic and are documented here. For additional outputs, see the
    documentation of the scenario.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`components.LandscapeScenario` component")
    base.VERSION.changed("1.2.5", "`components.LandscapeScenario` can provide flexible set of outputs")
    base.VERSION.changed("1.2.6", "`components.LandscapeScenario` provides absolute paths for directories also")
    base.VERSION.changed(
        "1.2.18", "`components.LandscapeScenario` has new input XML schema and checks layer consistency")
    base.VERSION.changed("1.2.19", "`components.LandscapeScenario` ROI extent as meta-datum in package info file")
    base.VERSION.changed("1.2.20", "`components.LandscapeScenario` distinguishes between supplementary data formats")
    base.VERSION.changed(
        "1.2.20", "`components.LandscapeScenario` can import additional attributes from base geometry shapefile")
    base.VERSION.changed("1.2.34", "Better exceptions in `components.LandscapeScenario`")
    base.VERSION.changed("1.2.35", "Class checks in `components.LandscapeScenario`")
    base.VERSION.changed("1.3.2", "Enforce strict checks in `components.LandscapeScenario`")
    base.VERSION.changed("1.3.27", "`components.LandscapeScenario` specifies scales")
    base.VERSION.changed("1.3.33", "`components.LandscapeScenario` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.LandscapeScenario` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.LandscapeScenario` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.LandscapeScenario` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.LandscapeScenario`")
    base.VERSION.changed("1.4.1", "`components.LandscapeScenario` class documentation")
    base.VERSION.fixed("1.4.7", "`components.LandscapeScenario` added path to proj.db zo fix errors on some systems")
    base.VERSION.changed("1.4.9", "`components.LandscapeScenario` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.0", "`components.LandscapeScenario` updated path to Proj4 library")
    base.VERSION.changed("1.6.0", "`components.LandscapeScenario` casts exported WKB geometries to bytes")
    base.VERSION.changed("1.6.1", "Renamed to `components.LandscapeScenario`")
    base.VERSION.changed("1.6.4", "`components.LandscapeScenario` reads physical units from package metadata")
    base.VERSION.added("1.7.0", "Type hints to `components.LandscapeScenario`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.LandscapeScenario` with base class")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `components.LandscapeScenario`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.LandscapeScenario`")
    base.VERSION.added("1.9.2", "`components.LandscapeScenario` output of base layer EPSG code")
    base.VERSION.changed("1.10.0", "`components.LandscapeScenario` reports global scale of metadata outputs")
    base.VERSION.changed("1.10.0", "`components.LandscapeScenario` gained semantics for element identifier attribute")
    base.VERSION.changed("1.10.4", "Added additional consistency check to `components.LandscapeScenario`")
    base.VERSION.changed("1.12.0", "`components.LandscapeScenario` output scale order")
    base.VERSION.changed("1.12.0", "`components.LandscapeScenario` reports offset")
    base.VERSION.changed("1.12.5", "Perform XML schema validation in `components.LandscapeScenario`")
    base.VERSION.changed(
        "1.14.0", "`components.LandscapeScenario` reports geometries of values also as value attributes")
    base.VERSION.changed("1.15.6", "Updated description of `LandscapeScenario` component")
    base.VERSION.added("1.15.6", "Input descriptions to `LandscapeScenario` component")
    base.VERSION.added("1.16.0", "Inputs of `LandscapeScenario` component are now processed by `base.convert`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a LandscapeScenario component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(LandscapeScenario, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "BaseLandscapeGeometries",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global"), attrib.Ontology("")),
                self.default_observer,
                description="A valid file path to a package file. The package file is an XML file that contains "
                            "metadata about the geospatial data of a landscape scenario. Only landscape scenarios with "
                            "auch a metadata description are compatible with the `LandscapeScenario` component. The "
                            "package file is commonly name `package.xinfo` and resides alongside the geodata of a "
                            "landscape scenario. Scenarios normally provide the absolute file path to the package file "
                            "as a macro to the landscape model. This macro is commonly named `$(:LandscapeScenario)`, "
                            "a value that should therefore normally be used for configuration of the component.  \n"
                            "The `LandscapeScenario` component allows to import landscape scenarios for a wide range "
                            "of simulations which differ in their geospatial requirements (e.g., off-field soil "
                            "simulations compared with aquatic simulations). The `GeoPackageNamespace` input defines "
                            "the domain of the simulation regarding these requirements. The structure of the XML is "
                            "described by an XML schema (`package.xsd` in the `model/variant` folder) and the package "
                            "file itself must make use of the specified namespace and validate against the XML schema."
            ),
            base.Input(
                "GeoPackageNamespace",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The XML namespace for the metadata of the landscape scenario. This should be the target "
                            "namespace of the XML schema (`model/variant/package.xsd`) of this model, e.g., "
                            "`urn:xAquaticRiskLandscapeScenarioPackageInfo` for an aquatic scenario. Make sure that "
                            "the scenario's geodata description (`package.xinfo`) makes use of this namespace."
            )
        ])
        self._outputs = base.ProvisionalOutputs(self, default_store)
        self._spatial_reference = None
        self._base_geometries_extent = None
        if self.default_observer:
            self.default_observer.write_message(
                3,
                "The LandscapeScenario component does currently not document its generic outputs",
                "Documentation will be added in a future version"
            )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """

        def strip_namespace(tag: str) -> str:
            """
            Strips the namespace from an XML tag.
            Args:
                tag: The complete tag including namespace.

            Returns:
                The tag without namespace.
            """
            return re.match("(?:{.*})?(?P<stripped_tag>.+)", tag).group(1)

        os.environ["PROJ_LIB"] = os.path.abspath(
            os.path.join(
                os.path.dirname(__file__),
                "..",
                "bin",
                "python-3.9.7-amd64",
                "Lib",
                "site-packages",
                "osgeo",
                "data",
                "proj"
            )
        )
        landscape_info_file = self.inputs["BaseLandscapeGeometries"].read().values
        schema_path = os.path.join(os.path.dirname(__file__), "..", "..", "variant", "package.xsd")
        xmlschema.XMLSchema(schema_path).validate(landscape_info_file)
        landscape_info_xml = xml.etree.ElementTree.parse(landscape_info_file).getroot()
        landscape_path = os.path.dirname(os.path.abspath(landscape_info_file))
        namespace = {"": self.inputs["GeoPackageNamespace"].read().values}
        attributes = {
            landscape_info_xml.find("base/feature_id_attribute", namespace).text: "FeatureIds",
            landscape_info_xml.find("base/feature_type_attribute", namespace).text: "FeatureTypeIds"
        }
        for additionalAttribute in landscape_info_xml.find("base/additional_attributes", namespace):
            attributes[additionalAttribute.text] = strip_namespace(additionalAttribute.tag)
        self.import_shapefile(
            os.path.join(landscape_path, landscape_info_xml.find("base/base_landscape_geometries", namespace).text),
            attributes,
            True
        )
        meta = landscape_info_xml.find("meta", namespace)
        roi = meta.find("ROI_extent", namespace)
        if roi is not None:
            extent = tuple([float(x) for x in roi.text.split(",")])
        else:
            extent = self._base_geometries_extent
        for entry in meta:
            self.outputs[strip_namespace(entry.tag)].set_values(base.convert(entry), scales="global")
        for entry in landscape_info_xml.find("supplementary", namespace):
            if entry.text[-4:] == ".tif":
                raster_path = os.path.join(landscape_path, entry.text)
                r = gdal.Open(raster_path)
                raster_crs = r.GetProjection()
                raster_spatial_reference = osr.SpatialReference()
                raster_spatial_reference.ImportFromWkt(raster_crs)
                if not self._spatial_reference.IsSame(raster_spatial_reference):
                    self.default_observer.write_message(
                        1, f"Base CRS and CRS of {strip_namespace(entry.tag)} do not match")
                    raise ValueError
                raster_geo_transform = r.GetGeoTransform()
                if raster_geo_transform[2] != 0 or raster_geo_transform[4] != 0:
                    self.default_observer.write_message(1, f"Raster {strip_namespace(entry.tag)} is skewed")
                    raise ValueError
                raster_extent = (raster_geo_transform[0],
                                 raster_geo_transform[0] + raster_geo_transform[1] * r.RasterXSize,
                                 raster_geo_transform[3] + raster_geo_transform[5] * r.RasterYSize,
                                 raster_geo_transform[3])
                if (
                        abs(extent[0] - raster_extent[0]) >= abs(raster_geo_transform[1] / 2) or
                        abs(extent[1] - raster_extent[1]) >= abs(raster_geo_transform[1] / 2) or
                        abs(extent[2] - raster_extent[2]) >= abs(raster_geo_transform[5] / 2) or
                        abs(extent[3] - raster_extent[3]) >= abs(raster_geo_transform[5] / 2)
                ):
                    if entry.attrib.setdefault("deviatingExtent", "") == "confirmed":
                        self.default_observer.write_message(
                            3,
                            f"ROI and {strip_namespace(entry.tag)} have different extents (confirmed)")
                        self.default_observer.write_message(3, f"1: {extent}")
                        self.default_observer.write_message(3, f"2: {raster_extent}")
                    else:
                        self.default_observer.write_message(
                            1, f"ROI and {strip_namespace(entry.tag)} have different extents")
                        self.default_observer.write_message(3, f"1: {extent}")
                        self.default_observer.write_message(3, f"2: {raster_extent}")
                        raise ValueError
                if r.RasterXSize != int(round(extent[1] - extent[0])) or r.RasterYSize != int(
                        round(extent[3] - extent[2])):
                    if entry.attrib.setdefault("deviatingExtent", "") == "confirmed":
                        self.default_observer.write_message(
                            3,
                            f"1sqm ROI and {strip_namespace(entry.tag)} differ in size (confirmed)"
                        )
                        self.default_observer.write_message(
                            3,
                            f"1: {int(round(extent[1] - extent[0]))} x {int(round(extent[3] - extent[2]))}"
                        )
                        self.default_observer.write_message(3, f"2: {r.RasterXSize} x {r.RasterYSize}")
                    else:
                        self.default_observer.write_message(
                            1, f"1sqm ROI and {strip_namespace(entry.tag)} differ in size")
                        self.default_observer.write_message(
                            3,
                            f"1: {int(round(extent[1] - extent[0]))} x {int(round(extent[3] - extent[2]))}"
                        )
                        self.default_observer.write_message(1, "Raster does not contain exactly one band")
                        raise ValueError
                if r.RasterCount != 1:
                    self.default_observer.write_message(3, f"2: {r.RasterYSize} x {r.RasterYSize}")
                    raise ValueError
                self.default_observer.write_message(5, f"Importing {raster_path}")
                self.outputs[strip_namespace(entry.tag)].set_values(raster_path, scales="global")
                raster_band = r.GetRasterBand(1)
                block_size_x, block_size_y = raster_band.GetBlockSize()
                cell_area = str(int(raster_geo_transform[1] * -raster_geo_transform[5]))
                dataset_name = f"{strip_namespace(entry.tag)}_values"
                self.outputs[dataset_name].set_values(
                    np.ndarray,
                    shape=(r.RasterYSize, r.RasterXSize),
                    data_type=np.int,
                    chunks=(min(block_size_y, r.RasterYSize), min(block_size_x, r.RasterXSize)),
                    scales=f"space_y/{cell_area}sqm, space_x/{cell_area}sqm",
                    offset=(raster_extent[2], raster_extent[0])
                )
                for y_offset in range(0, r.RasterYSize, block_size_y):
                    number_rows = block_size_y if y_offset + block_size_y < r.RasterYSize else r.RasterYSize - y_offset
                    for x_offset in range(0, r.RasterXSize, block_size_x):
                        number_cols = \
                            block_size_x if x_offset + block_size_x < r.RasterXSize else r.RasterXSize - x_offset
                        data = raster_band.ReadAsArray(x_offset, y_offset, number_cols, number_rows)
                        self.outputs[dataset_name].set_values(
                            data,
                            slices=(slice(y_offset, y_offset + number_rows), slice(x_offset, x_offset + number_cols)),
                            create=False
                        )
            elif entry.text[-4:] == ".shp":
                shapefile_path = os.path.join(landscape_path, entry.text)
                self.outputs[strip_namespace(entry.tag)].set_values(shapefile_path, scales="global")
            else:
                self.outputs[strip_namespace(entry.tag)].set_values(entry.text, scales="global")
        for entry in landscape_info_xml.find("supplementary_shapefiles", namespace):
            attributes = {}
            units = {}
            id_attribute = None
            for attribute in entry.find("attributes", namespace):
                attribute_name = f"{strip_namespace(entry.tag)}_{strip_namespace(attribute.tag)}"
                attributes[attribute.attrib["column"]] = attribute_name
                units[attribute_name] = attribute.attrib["unit"] if "unit" in attribute.attrib else None
                if "role" in attribute.attrib and attribute.attrib["role"] == "id":
                    id_attribute = attribute_name
            if id_attribute is None:
                raise ValueError(f"Role of id column for {strip_namespace(entry.tag)} is not asserted")
            self.import_shapefile(
                os.path.join(landscape_path, entry.find("file_name", namespace).text),
                attributes,
                geometry_output=f"{strip_namespace(entry.tag)}_geom",
                units=units,
                id_attribute=id_attribute
            )

    def import_shapefile(
            self,
            file_name: str,
            attributes: typing.Mapping[str, str],
            is_base: bool = False,
            geometry_output: str = "Geometries",
            units: typing.Optional[typing.Mapping[str, str]] = None,
            id_attribute: str = "FeatureIds"
    ) -> None:
        """
        Imports a shapefile into the Landscape Model by storing its geometries and attributes.

        Args:
            file_name: The path and file name of the shapefile.
            attributes: The attributes to be imported from the shapefile.
            is_base: Indicates whether the imported shapefile contains the base geometries or is supplementary.
            geometry_output: The name of the dataset where the geometries of the shapefile are stored.
            units: The physical units associated with the shapefile attributes.
            id_attribute:
                The name of the attribute that has the role of uniquely identifying each feature of the shapefile.

        Returns:
            Nothing.
        """
        ogr_driver = ogr.GetDriverByName("ESRI Shapefile")
        ogr_data_set = ogr_driver.Open(file_name, 0)
        assert ogr_data_set, f"Landscape scenario references a shapefile {file_name} which could not be found"
        ogr_layer = ogr_data_set.GetLayer()
        ogr_layer_spatial_reference = ogr_layer.GetSpatialRef()
        crs = ogr_layer_spatial_reference.ExportToWkt()
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromWkt(crs)
        if is_base:
            if self._spatial_reference is None:
                self._spatial_reference = spatial_reference
                self._base_geometries_extent = ogr_layer.GetExtent()
                crs_unit = ogr_layer_spatial_reference.GetLinearUnitsName()
                self.outputs["Extent"].set_values(self._base_geometries_extent, scales="space/extent", unit=crs_unit)
                self.outputs["Crs"].set_values(crs, scales="global")
                spatial_reference.AutoIdentifyEPSG()
                epsg = int(spatial_reference.GetAuthorityCode(None))
                if epsg is None:
                    self.default_observer.write_message(1, "Base coordinate system has no EPSG code")
                    raise ValueError
                self.outputs["EPSG"].set_values(epsg, scales="global")
            else:
                self.default_observer.write_message(1, "Cannot override already set spatial base reference")
                raise ValueError
        elif not spatial_reference.IsSame(self._spatial_reference):
            self.default_observer.write_message(1, f"Base CRS and CRS of {file_name} do not match")
            raise ValueError
        geometries = []
        values = {}
        for attribute in attributes.values():
            values[attribute] = []
        for i, feature in enumerate(ogr_layer):
            geom = feature.GetGeometryRef()
            if geom is None:
                raise ValueError(f"Feature number {i} has no geometry")
            geometries.append(bytes(geom.ExportToWkb()))
            for attribute in attributes.items():
                value = feature[attribute[0]]
                if value is None:
                    raise ValueError(
                        f"NULL values in feature attributes are not supported ({file_name}: {attribute[0]})")
                values[attribute[1]].append(value)
        self.outputs[geometry_output].set_values(
            geometries,
            scales="space/base_geometry",
            geometries=(self.outputs[geometry_output],),
            ignore_missing_metadata=("element_names",)
        )
        for attribute, attribute_values in values.items():
            if attribute == id_attribute:
                self._import_attribute_values(
                    attribute, attribute_values, units, self.outputs[id_attribute], self.outputs[geometry_output])
        for attribute, attribute_values in values.items():
            if attribute != id_attribute:
                self._import_attribute_values(
                    attribute, attribute_values, units, self.outputs[id_attribute], self.outputs[geometry_output])
        self.outputs[geometry_output].set_values(
            base.ExistingValues,
            element_names=(self.outputs[id_attribute],),
            ignore_missing_metadata=("geometries",)
        )

    def _import_attribute_values(
            self,
            attribute: str,
            attribute_values: list,
            units: typing.Optional[typing.Mapping[str, str]],
            element_names: base.Output,
            geometries: base.Output
    ):
        """
        Imports feature attribute values into the Landscape Model data store.

        Args:
            attribute: The name of the imported attributes.
            attribute_values: The values to import.
            units: The physical units associated with the shapefile attributes.
            element_names: The output containing the identifiers of individual features.
            geometries: The spatial extents of individual features.

        Returns:
            Nothing.
        """
        unit = None
        if units is not None and attribute in units:
            unit = units[attribute]
        self.outputs[attribute].set_values(
            attribute_values,
            scales="space/base_geometry",
            unit=unit,
            element_names=(element_names,),
            geometries=(geometries,)
        )
