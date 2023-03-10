"""
Class definition of the Landscape Scenario Preparation component.
"""
import base
import os
import xml.etree.ElementTree
from osgeo import ogr, gdal
import shutil
import math
import numpy as np
import scipy.ndimage
import typing


class LandscapeScenarioPreparation(base.Component):
    """
    A component that prepares landscape scenarios ingested by the LandscapeScenario component from geo-files.

    INPUTS
    OutputPath: The path where to write the landscape scenario to.
    LandscapeScenarioVersion: The version of the landscape scenario.
    LandscapeScenarioDescription: A description of the landscape scenario.
    TargetFieldLandUseLandCoverType: The identifier of the target land-use / land-cover type.
    BaseLandscapeGeometries: The base landscape geometries.
    FeatureIdAttribute: The name of the feature ID attribute.
    DEM: A digital elevation model.

    OUTPUTS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.3.28", "`components.LandscapeScenarioPreparation` component")
    base.VERSION.changed("1.3.29", "`components.LandscapeScenarioPreparation` can calculate flow grids from DEM")
    base.VERSION.added("1.4.1", "Changelog in `components.LandscapeScenarioPreparation` ")
    base.VERSION.changed("1.4.1", "`components.LandscapeScenarioPreparation` class documentation")
    base.VERSION.changed("1.4.9", "`components.LandscapeScenarioPreparation` spell check exclusion")
    base.VERSION.changed("1.5.3", "`components.LandscapeScenarioPreparation` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.1", "Updated `components.LandscapeScenarioPreparation` to new metadata format")
    base.VERSION.added("1.7.0", "Type hints to `components.LandscapeScenarioPreparation` ")
    base.VERSION.changed(
        "1.7.0", "Harmonized init signature of `components.LandscapeScenarioPreparation` with base class")
    base.VERSION.changed(
        "1.8.0", "Replaced Legacy format strings by f-strings in `components.LandscapeScenarioPreparation` ")
    base.VERSION.changed(
        "1.9.6", "Replaced GDAL constants by numerical values in `components.LandscapeScenarioPreparation` ")
    base.VERSION.changed("1.12.6", "Mitigated weak code warning in `components.LandscapeScenarioPreparation` ")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(LandscapeScenarioPreparation, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input("OutputPath", (), self.default_observer),
            base.Input("LandscapeScenarioVersion", (), self.default_observer),
            base.Input("LandscapeScenarioDescription", (), self.default_observer),
            base.Input("TargetFieldLandUseLandCoverType", (), self.default_observer),
            base.Input("HabitatLUseLandCoverTypes", (), self.default_observer),
            base.Input("BaseLandscapeGeometries", (), self.default_observer),
            base.Input("FeatureIdAttribute", (), self.default_observer),
            base.Input("FeatureLandUsLandCoverTypeAttribute", (), self.default_observer),
            base.Input("DEM", (), self.default_observer)
        ])

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        output_path = self.inputs["OutputPath"].read().values
        os.makedirs(output_path)
        landscape_package = xml.etree.ElementTree.Element("landscape_package")
        meta = xml.etree.ElementTree.SubElement(landscape_package, "meta")
        xml.etree.ElementTree.SubElement(meta, "version").text = self.inputs["LandscapeScenarioVersion"].read().values
        xml.etree.ElementTree.SubElement(meta, "description").text = self.inputs[
            "LandscapeScenarioDescription"].read().values
        xml.etree.ElementTree.SubElement(meta, "target_type").text = self.inputs[
            "TargetFieldLandUseLandCoverType"].read().values
        xml.etree.ElementTree.SubElement(meta, "habitat_types").text = self.inputs[
            "HabitatLandUseLandCoverTypes"].read().values
        ogr_driver = ogr.GetDriverByName("ESRI Shapefile")
        base_landscape_geometries = self.inputs["BaseLandscapeGeometries"].read().values
        ogr_data_set = ogr_driver.Open(base_landscape_geometries, 0)
        ogr_layer = ogr_data_set.GetLayer()
        extent = ogr_layer.GetExtent()
        xml.etree.ElementTree.SubElement(meta, "ROI_extent").text = ", ".join([str(x) for x in extent])
        for ext in [".shp", ".shx", ".dbf", ".prj"]:
            shutil.copyfile(os.path.splitext(base_landscape_geometries)[0] + ext,
                            os.path.join(output_path,
                                         os.path.splitext(os.path.basename(base_landscape_geometries))[0]) + ext)
        base_element = xml.etree.ElementTree.SubElement(landscape_package, "base")
        xml.etree.ElementTree.SubElement(base_element, "base_landscape_geometries").text = os.path.basename(
            base_landscape_geometries)
        xml.etree.ElementTree.SubElement(base_element, "feature_id_attribute").text = self.inputs[
            "FeatureIdAttribute"].read().values
        xml.etree.ElementTree.SubElement(base_element, "feature_type_attribute").text = self.inputs[
            "FeatureLandUseLandCoverTypeAttribute"].read().values
        xml.etree.ElementTree.SubElement(base_element, "additional_attributes")
        supplementary = xml.etree.ElementTree.SubElement(landscape_package, "supplementary")
        raster_cols = int(round(extent[1] - extent[0]))
        raster_rows = int(round(extent[3] - extent[2]))
        raster_driver = gdal.GetDriverByName("GTiff")
        dem = self.inputs["DEM"].read().values
        if os.path.isfile(dem):
            dem_raster = gdal.Open(dem)
            geo_transform = dem_raster.GetGeoTransform()
            cell_extent = (
                max(0, int(math.floor((extent[0] - geo_transform[0]) / geo_transform[1])) - 1),
                max(0, int(math.floor((extent[3] - geo_transform[3]) / geo_transform[5])) - 1),
                min(dem_raster.RasterXSize - 1, int(math.ceil((extent[1] - geo_transform[0]) / geo_transform[1])) + 1),
                min(dem_raster.RasterYSize - 1, int(math.ceil((extent[2] - geo_transform[3]) / geo_transform[5])) + 1)
            )
            dem_values = dem_raster.GetRasterBand(1).ReadAsArray(
                cell_extent[0],
                cell_extent[1],
                cell_extent[2] - cell_extent[0] + 1,
                cell_extent[3] - cell_extent[1] + 1
            )
            flow_dir = scipy.ndimage.generic_filter(
                dem_values,
                lambda x: (0, 1, 4, 16, 64)[int(np.argmin(x[[2, 3, 4, 1, 0]]))],
                footprint=((0, 1, 0), (1, 1, 1), (0, 1, 0)),
                output=np.core.dtype('b')
            )
            flow_dir_data_set = raster_driver.Create(
                os.path.join(output_path, "flow.tif"),
                flow_dir.shape[1],
                flow_dir.shape[0],
                1,
                1,
                ["COMPRESS=LZW"]
            )
            flow_dir_data_set.SetGeoTransform([
                geo_transform[0] + geo_transform[1] * cell_extent[0],
                geo_transform[1],
                0,
                geo_transform[3] + geo_transform[5] * cell_extent[1],
                0,
                geo_transform[5]
            ])
            flow_dir_data_set.SetProjection(dem_raster.GetProjection())
            output_band = flow_dir_data_set.GetRasterBand(1)
            output_band.WriteArray(flow_dir, 0, 0)
        else:
            self.default_observer.write_message(2, "No DEM provided - generating generic flow from West to East")
            flow_raster = raster_driver.Create(
                os.path.join(output_path, "flow.tif"), raster_cols, raster_rows, 1, 1, ["COMPRESS=LZW"])
            flow_raster.SetGeoTransform((extent[0], 1, 0, extent[3], 0, -1))
            flow_raster.SetProjection(ogr_layer.GetSpatialRef().ExportToWkt())
            gdal.RasterizeLayer(flow_raster, [1], ogr_layer, burn_values=[1])
        xml.etree.ElementTree.SubElement(
            supplementary,
            "flow_grid",
            {"deviatingExtent": "confirmed"}
        ).text = "flow.tif"
        land_use_raster = raster_driver.Create(
            os.path.join(output_path, "land_use.tif"), raster_cols, raster_rows, 1, 2, ["COMPRESS=LZW"])
        land_use_raster.SetGeoTransform((extent[0], 1, 0, extent[3], 0, -1))
        land_use_raster.SetProjection(ogr_layer.GetSpatialRef().ExportToWkt())
        gdal.RasterizeLayer(
            land_use_raster,
            [1],
            ogr_layer,
            burn_values=[1],
            options=[f"ATTRIBUTE={self.inputs['FeatureLandUseLandCoverTypeAttribute'].read().values}"])
        xml.etree.ElementTree.SubElement(supplementary, "land_use_raster").text = "land_use.tif"
        analysis_buffer_raster = raster_driver.Create(os.path.join(
            output_path, "AnalysisBuffer.tif"), raster_cols, raster_rows, 1, 1, ["COMPRESS=LZW"])
        analysis_buffer_raster.SetGeoTransform((extent[0], 1, 0, extent[3], 0, -1))
        analysis_buffer_raster.SetProjection(ogr_layer.GetSpatialRef().ExportToWkt())
        gdal.RasterizeLayer(analysis_buffer_raster, [1], ogr_layer, burn_values=[255])
        memory_driver = ogr.GetDriverByName("MEMORY")
        memory_data_set = memory_driver.CreateDataSource("analysisBuffers")
        ogr_layer.SetAttributeFilter(
            f"{self.inputs['FeatureLandUseLandCoverTypeAttribute'].read().values}="
            f"{self.inputs['TargetFieldLandUseLandCoverType'].read().values}"
        )
        for buffer_distance in [100, 50, 20, 5, 2, 1]:
            memory_layer = memory_data_set.CreateLayer("analysisBuffer.shp", ogr_layer.GetSpatialRef(),
                                                       ogr.wkbPolygon)
            feature_definition = memory_layer.GetLayerDefn()
            for feature in ogr_layer:
                field_geometry = feature.GetGeometryRef()
                buffer_geometry = field_geometry.Buffer(buffer_distance)
                output_feature = ogr.Feature(feature_definition)
                output_feature.SetGeometry(buffer_geometry)
                memory_layer.CreateFeature(output_feature)
            ogr_layer.ResetReading()
            gdal.RasterizeLayer(analysis_buffer_raster, [1], memory_layer, burn_values=[buffer_distance])
            memory_data_set.DeleteLayer("analysisBuffer.shp")
        gdal.RasterizeLayer(analysis_buffer_raster, [1], ogr_layer, burn_values=[0])
        xml.etree.ElementTree.SubElement(supplementary, "analysis_distance_groups").text = "AnalysisBuffer.tif"
        # noinspection SpellCheckingInspection
        xml.etree.ElementTree.ElementTree(landscape_package).write(
            os.path.join(output_path, "package.xinfo"), "utf-8", True)
