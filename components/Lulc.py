"""
Class definition for the Landscape Model Lulc component.
"""
from osgeo import gdal
from osgeo import ogr
from osgeo import osr
import os
import base
import xml.etree.ElementTree
import attrib
import numpy as np


class Lulc(base.Component):
    """
    Provides landscape scenarios to the Landscape Model.

    INPUTS
    BaseLandscapeGeometries: A valid file path to a package file. A string of global scale. Value has no unit.
    No ontological description is associated with the input.

    OUTPUTS
    Outputs of this components are provisional, i.e., they are defined by links from inputs and have to be satisfied
    by data in the CSV file. Outputs are Crs, Extent, and information specified in the package information file of the
    landscape scenario.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`components.Lulc` component")
    base.VERSION.changed("1.2.5", "`components.Lulc` can provide flexible set of outputs")
    base.VERSION.changed("1.2.6", "`components.Lulc` provides absolute paths for directories also")
    base.VERSION.changed("1.2.18", "`components.Lulc` has new input XML schema and checks layer consistency")
    base.VERSION.changed("1.2.19", "`components.Lulc` ROI extent as meta-datum in package info file")
    base.VERSION.changed("1.2.20", "`components.Lulc` distinguishes between supplementary data formats")
    base.VERSION.changed("1.2.20", "`components.Lulc` can import additional attributes from base geometry shapefile")
    base.VERSION.changed("1.2.34", "Better exceptions in `components.Lulc` ")
    base.VERSION.changed("1.2.35", "Class checks in `components.Lulc` ")
    base.VERSION.changed("1.3.2", "Enforce strict checks in `components.Lulc` ")
    base.VERSION.changed("1.3.27", "`components.Lulc` specifies scales")
    base.VERSION.changed("1.3.33", "`components.Lulc` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.Lulc` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.Lulc` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.Lulc` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.Lulc` ")
    base.VERSION.changed("1.4.1", "`components.Lulc` class documentation")
    base.VERSION.fixed("1.4.7", "`components.Lulc` added path to proj.db zo fix errors on some systems")
    base.VERSION.changed("1.4.9", "`components.lulc` changelog uses markdown for code elements")

    def __init__(self, name, observer, store):
        super(Lulc, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "BaseLandscapeGeometries",
                (
                    attrib.Class(str, 1),
                    attrib.Unit(None, 1),
                    attrib.Scales("global", 1),
                    attrib.Ontology("")
                ),
                self.default_observer)
        ])
        self._outputs = base.ProvisionalOutputs(self, store)
        self._spatial_reference = None
        self._base_geometries_extent = None
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        os.environ["PROJ_LIB"] = os.path.abspath(os.path.join(
            os.path.dirname(__file__), "..", "bin", "Python38", "Lib", "site-packages", "osgeo", "data", "proj"))
        landscape_info_file = self.inputs["BaseLandscapeGeometries"].read().values
        landscape_info_xml = xml.etree.ElementTree.parse(landscape_info_file).getroot()
        landscape_path = os.path.dirname(os.path.abspath(landscape_info_file))
        attributes = {
            landscape_info_xml.find("base/feature_id_attribute").text: "FeatureIds",
            landscape_info_xml.find("base/feature_lulc_type_attribute").text: "LulcTypeIds"
        }
        for additionalAttribute in landscape_info_xml.find("base/additional_attributes"):
            attributes[additionalAttribute.text] = additionalAttribute.tag
        self.import_shapefile(
            os.path.join(landscape_path, landscape_info_xml.find("base/base_landscape_geometries").text),
            attributes,
            True
        )
        meta = landscape_info_xml.find("meta")
        roi = meta.find("ROI_extent")
        if roi is not None:
            extent = tuple([float(x) for x in roi.text.split(",")])
        else:
            extent = self._base_geometries_extent
        for entry in meta:
            self.outputs[entry.tag].set_values(entry.text)
        for entry in landscape_info_xml.find("supplementary"):
            if entry.text[-4:] == ".tif":
                raster_path = os.path.join(landscape_path, entry.text)
                r = gdal.Open(raster_path)
                raster_crs = r.GetProjection()
                raster_spatial_reference = osr.SpatialReference()
                raster_spatial_reference.ImportFromWkt(raster_crs)
                if not self._spatial_reference.IsSame(raster_spatial_reference):
                    self.default_observer.write_message(1, "Base CRS and CRS of " + entry.tag + " do not match")
                    raise ValueError
                raster_geo_transform = r.GetGeoTransform()
                if raster_geo_transform[2] != 0 or raster_geo_transform[4] != 0:
                    self.default_observer.write_message(1, "Raster " + entry.tag + " is skewed")
                    raise ValueError
                raster_extent = (raster_geo_transform[0],
                                 raster_geo_transform[0] + raster_geo_transform[1] * r.RasterXSize,
                                 raster_geo_transform[3] + raster_geo_transform[5] * r.RasterYSize,
                                 raster_geo_transform[3])
                if abs(extent[0] - raster_extent[0]) >= abs(raster_geo_transform[1] / 2) or abs(
                        extent[1] - raster_extent[1]) >= abs(raster_geo_transform[1] / 2) or abs(
                        extent[2] - raster_extent[2]) >= abs(raster_geo_transform[5] / 2) or abs(
                        extent[3] - raster_extent[3]) >= abs(raster_geo_transform[5] / 2):
                    if entry.attrib.setdefault("deviatingExtent", "") == "confirmed":
                        self.default_observer.write_message(
                            3,
                            "ROI and " + entry.tag + " have different extents (confirmed)")
                        self.default_observer.write_message(3, "1: " + str(extent))
                        self.default_observer.write_message(3, "2: " + str(raster_extent))
                    else:
                        self.default_observer.write_message(1, "ROI and " + entry.tag + " have different extents")
                        self.default_observer.write_message(3, "1: " + str(extent))
                        self.default_observer.write_message(3, "2: " + str(raster_extent))
                        raise ValueError
                if r.RasterXSize != int(round(extent[1] - extent[0])) or r.RasterYSize != int(
                        round(extent[3] - extent[2])):
                    if entry.attrib.setdefault("deviatingExtent", "") == "confirmed":
                        self.default_observer.write_message(
                            3,
                            "1sqm ROI and " + entry.tag + " differ in size (confirmed)"
                        )
                        self.default_observer.write_message(
                            3,
                            "1: " + str(int(round(extent[1] - extent[0]))) + " x " +
                            str(int(round(extent[3] - extent[2])))
                        )
                        self.default_observer.write_message(3, "2: " + str(r.RasterXSize) + " x " + str(r.RasterYSize))
                    else:
                        self.default_observer.write_message(1, "1sqm ROI and " + entry.tag + " differ in size")
                        self.default_observer.write_message(
                            3,
                            "1: " + str(int(round(extent[1] - extent[0]))) + " x " +
                            str(int(round(extent[3] - extent[2])))
                        )
                        self.default_observer.write_message(1, "Raster does not contain exactly one band")
                        raise ValueError
                if r.RasterCount != 1:
                    self.default_observer.write_message(3, "2: " + str(r.RasterXSize) + " x " + str(r.RasterYSize))
                    raise ValueError
                self.default_observer.write_message(5, "Importing " + raster_path)
                self.outputs[entry.tag].set_values(raster_path)
                raster_band = r.GetRasterBand(1)
                block_size_x, block_size_y = raster_band.GetBlockSize()
                cell_area = str(int(raster_geo_transform[1] * -raster_geo_transform[5]))
                dataset_name = entry.tag + "_values"
                self.outputs[dataset_name].set_values(
                    np.ndarray,
                    shape=(r.RasterXSize, r.RasterYSize),
                    data_type=np.int,
                    chunks=(min(block_size_x, r.RasterXSize), min(block_size_y, r.RasterYSize)),
                    scales="space_x/" + cell_area + "sqm, space_y/" + cell_area + "sqm"
                )
                for y_offset in range(0, r.RasterYSize, block_size_y):
                    number_rows = block_size_y if y_offset + block_size_y < r.RasterYSize else r.RasterYSize - y_offset
                    for x_offset in range(0, r.RasterXSize, block_size_x):
                        number_cols = \
                            block_size_x if x_offset + block_size_x < r.RasterXSize else r.RasterXSize - x_offset
                        data = np.transpose(raster_band.ReadAsArray(x_offset, y_offset, number_cols, number_rows))
                        self.outputs[dataset_name].set_values(
                            data,
                            slices=(slice(x_offset, x_offset + number_cols), slice(y_offset, y_offset + number_rows)),
                            create=False
                        )
            elif entry.text[-4:] == ".shp":
                shapefile_path = os.path.join(landscape_path, entry.text)
                self.outputs[entry.tag].set_values(shapefile_path)
            else:
                self.outputs[entry.tag].set_values(entry.text)
        for entry in landscape_info_xml.find("supplementary_shapefiles"):
            attributes = {}
            for attribute in entry.find("attributes"):
                attributes[attribute.attrib["column"]] = entry.tag + "_" + attribute.tag
            self.import_shapefile(
                os.path.join(landscape_path, entry.find("file_name").text),
                attributes,
                geometry_output=entry.tag + "_geom"
            )
        return

    def import_shapefile(self, file_name, attributes, is_base=False, geometry_output="Geometries"):
        """
        Imports a shapefile into the Landscape Model by storing its geometries and attributes.
        :param: file_name: The path and file name of the shapefile.
        :param: attributes: The attributes to be imported from the shapefile.
        :param: is_base: Indicates whether the imported shapefile contains the base geometries or is supplementary.
        :param: geometry_output: The name of the dataset where the geometries of the shapefile are stored.
        :return: Nothing.
        """
        ogr_driver = ogr.GetDriverByName("ESRI Shapefile")
        ogr_data_set = ogr_driver.Open(file_name, 0)
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
                self.outputs["Crs"].set_values(crs)
            else:
                self.default_observer.write_message(1, "Cannot override already set spatial base reference")
                raise ValueError
        elif not spatial_reference.IsSame(self._spatial_reference):
            self.default_observer.write_message(1, "Base CRS and CRS of " + file_name + " do not match")
            raise ValueError
        geometries = []
        values = {}
        for attribute in attributes.values():
            values[attribute] = []
        for i, feature in enumerate(ogr_layer):
            geom = feature.GetGeometryRef()
            if geom is None:
                raise ValueError("Feature number " + str(i) + " has no geometry")
            geometries.append(geom.ExportToWkb())
            for attribute in attributes.items():
                value = feature[attribute[0]]
                if value is None:
                    raise ValueError("NULL values in feature attributes are not supported ({}: {})".format(
                        file_name, attribute[0]))
                values[attribute[1]].append(value)
        self.outputs[geometry_output].set_values(geometries, scales="space/base_geometry")
        for value in values.items():
            self.outputs[value[0]].set_values(value[1], scales="space/base_geometry")
        return
