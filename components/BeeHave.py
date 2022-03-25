"""Class definition for the Landscape Model BeeHave component."""
import base
import typing
import attrib
import os
import numpy
import shapefile
import math
import shapely.geometry
import shapely.wkb


class BeeHave(base.Component):
    """
    Prepares a BeeHave scenario.

    INPUTS
    ProcessingPath: The working directory for the component.

    OUTPUTS
    None.
    """
    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a BeeHave component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(BeeHave, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            (
                base.Input(
                    "ProcessingPath",
                    (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "Nectar",
                    (
                        attrib.Class(numpy.ndarray),
                        attrib.Unit("L/(m²*d)"),
                        attrib.Scales("space/base_geometry, time/day")
                    ),
                    self.default_observer
                ),
                base.Input(
                    "Pollen",
                    (
                        attrib.Class(numpy.ndarray),
                        attrib.Unit("g/(m²*d)"),
                        attrib.Scales("space/base_geometry, time/day")
                    ),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveMapCenterPointX",
                    (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "BeeHaveMapCenterPointY",
                    (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridRadii",
                    (attrib.Class(list[float]), attrib.Unit("m"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridSteps",
                    (attrib.Class(int), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                ),
                base.Input(
                    "SegmentationGridNumberSegmentsPerRadius",
                    (attrib.Class(list[int]), attrib.Unit("1"), attrib.Scales("global")),
                    self.default_observer
                )
            )
        )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        def polar_point(origin_point, angle, d):
            """
            Translates polar coordinates of a point into cartesian coordinates.

            Args:
                origin_point: The cartesian coordinates of the polar coordinate system's origin.
                angle: The angle of the polar coordinate point.
                d: The distance of the polar coordinate point.

            Returns:
                A tuple containing the cartesian coordinates of the polar coordinate point.
            """
            return (
                origin_point.x + math.sin(math.radians(angle)) * d,
                origin_point.y + math.cos(math.radians(angle)) * d
            )

        processing_path = self.inputs["ProcessingPath"].read().values
        os.makedirs(processing_path)
        steps = self.inputs["SegmentationGridSteps"].read().values
        step_angle_width = 360 / steps
        segments_output_file = os.path.join(processing_path, "segments.shp")
        w = shapefile.Writer(segments_output_file, shapefile.POLYGON)
        w.field("ID", "I")
        radii = self.inputs["SegmentationGridRadii"].read().values
        segments = self.inputs["SegmentationGridNumberSegmentsPerRadius"].read().values
        if len(segments) != len(radii):
            raise ValueError("Number of segments and radii do not match.")
        center = shapely.geometry.Point(
            self.inputs["BeeHaveMapCenterPointX"].read().values, self.inputs["BeeHaveMapCenterPointY"].read().values)
        nectar = self.inputs["Nectar"].read()
        pollen = self.inputs["Pollen"].read()
        if nectar.geometries[0].store_name != pollen.geometries[0].store_name:
            raise ValueError("Geometries of nectar and pollen differ.")
        if nectar.values.shape != pollen.values.shape:
            raise ValueError("Shapes of nectar and pollen differ.")
        consolidated_output_file = os.path.join(processing_path, "consolidated.shp")
        patches = [shapely.wkb.loads(x).buffer(0) for x in nectar.geometries[0].get_values()]
        output_file = os.path.join(processing_path, "BeeHave.txt")
        i = 1
        for radius_id in range(0, len(radii)):
            for segment in range(segments[radius_id]):
                segment_vertices = []
                if radius_id == 0:
                    for z in range(steps):
                        segment_vertices.append(polar_point(center, z * step_angle_width, radii[radius_id]))
                else:
                    for z in range(0, int(360 / segments[radius_id]) + 1):
                        segment_vertices.append(
                            polar_point(
                                center, z * step_angle_width + segment * 360 / segments[radius_id], radii[radius_id]))
                    for z in range(int(360 / segments[radius_id]), -1, -1):
                        segment_vertices.append(polar_point(
                            center, z * step_angle_width + segment * 360 / segments[radius_id], radii[radius_id - 1]))
                w.poly([segment_vertices])
                w.record(i)
                i += 1
        w.close()
        segment_sf = shapefile.Reader(segments_output_file)
        segment_polygons = [shapely.geometry.Polygon(x.points) for x in segment_sf.shapes()]
        w = shapefile.Writer(consolidated_output_file, shapefile.POINT)
        w.field("VEG_TYPE")
        w.field("AREA", "N", 10, 2)
        for attribute in ("NECTAR", "POLLEN"):
            for day in range(pollen.values.shape[1]):
                w.field(f"{attribute}_{day}", "N", 10, 4)
        patch_types = {}
        for segment in segment_polygons:
            type_dictionary = {}
            for patch in range(len(patches)):
                if numpy.count_nonzero(nectar.values[patch]) + numpy.count_nonzero(pollen.values[patch]) > 0:
                    if segment.intersects(patches[patch]):
                        patch_type = hash(numpy.append(nectar.values[patch], pollen.values[patch]).tobytes())
                        if patch_type not in patch_types:
                            patch_types[patch_type] = {
                                "nectar": nectar.values[patch],
                                "pollen": pollen.values[patch],
                                "label": str(len(patch_types) + 1)
                            }
                        intersection = patches[patch].intersection(segment)
                        if not intersection.is_empty:
                            if patch_type in type_dictionary:
                                type_dictionary[patch_type] = type_dictionary[patch_type].union(intersection)
                            else:
                                type_dictionary[patch_type] = patches[patch].intersection(intersection)
            for key in type_dictionary:
                centroid = type_dictionary[key].centroid
                w.point(centroid.x, centroid.y)
                area = type_dictionary[key].area
                values = {"VEG_TYPE": patch_types[key]["label"], "AREA": area}
                for attribute in ("NECTAR", "POLLEN"):
                    for day in range(pollen.values.shape[1]):
                        values[f"{attribute}_{day}"] = patch_types[key][attribute.lower()][day] * area
                w.record(**values)
        w.close()
        sf = shapefile.Reader(consolidated_output_file)
        points = sf.shapeRecords()
        station_id = 1
        with open(output_file, "w") as f:
            f.write(
                "day\tID\toldPatchID\tpatchType\tdistance_m\txcor\tycor\tsize_sqm\tquantityPollen_g\tConcentration\t"
                "quantityNectar_l\tcalcDetectProb\tmodelDetectProb\tNectarGathering_s\tPollenGathering_s\n"
            )
            for i, point in enumerate(points):
                distance = math.sqrt(
                    math.pow(
                        center.x - point.shape.points[0][0], 2.0) + math.pow(center.y - point.shape.points[0][1], 2.0))
                if round(distance, 2) > 0:
                    for day in range(pollen.values.shape[1]):
                        pollen_index = f"POLLEN_{day}"
                        nectar_index = f"NECTAR_{day}"
                        f.write(
                            f"{day + 1}\t{station_id}\t{station_id}\t{int(float(point.record['VEG_TYPE']))}\t"
                            f"{format(distance, 'f')}\t{format(center.x - point.shape.points[0][0], 'f')}\t"
                            f"{format(center.y - point.shape.points[0][1], 'f')}\t{format(point.record['AREA'], 'f')}\t"
                            f"{format(point.record[pollen_index], 'f')}\t"
                            f"1.5\t{format(point.record[nectar_index], 'f')}\t"
                            f"{format(1 / distance * math.sqrt(point.record['AREA']) / 100, 'f')}\t-999\t1200\t600\n"
                        )
                    station_id += 1
