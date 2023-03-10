"""Class definition of a Landscape Model component generating hydrographic maps."""
import base
import attrib
import osgeo.ogr
import matplotlib.path
import matplotlib.patches
import matplotlib.pyplot
import matplotlib.colors
import matplotlib.cm
import numpy
import datetime
import os
import typing


class ReportingHydrographicMap(base.Component):
    """
    Draws a map displaying the distribution of values in a hydrographic network.

    INPUTS
    Hydrography: The hydrographic network geometries. A list[bytes] of scale space/base_geometry.
    HydrographicReachIds: The identifiers of reaches according to the hydrography. A list[int] of scale
    space/base_geometry.
    SimulationStart: The first day of the simulation. A `datetime.date` of global scale.
    DisplayedTime: The time displayed in the map. A `datetime.date` of global scale.
    Values: The values to map onto the hydrographic network. A NumPy array.
    ValuesReachIds: The reach identifiers according to the values. A list[int] of scale space/reach.
    Title: The title of the plot. A string of global scale.
    OutputFile: A valid path to a file where the plot is written to. A string of global scale.
    DisplayedUnit: The unit in which values should be displayed. A string of global scale.
    ScaleMaxValue: The maximum value to which the legend is scaled. A float of global scale.
    ScaleMinValue: The minimum value to which the legend is scaled. A float of global scale.
    ValuesNormalization: The normalization applied to the values. A string of global scale.
    ColorMap: The color map used for displaying the values. A list[str] with global scale.

    OUTPUTS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.ReportingHydrographicMap` component")
    base.VERSION.added("1.4.1", "Changelog in `components.ReportingHydrographicMap`")
    base.VERSION.changed("1.4.1", "`components.ReportingHydrographicMap` class documentation")
    base.VERSION.added("1.4.5", "`components.ReportingHydrographicMap.draw()` static method")
    base.VERSION.changed("1.4.5", "`components.ReportingHydrographicMap.__init__` `observer` argument renamed")
    base.VERSION.changed("1.4.9", "`components.ReportingHydrographicMap` changelog uses markdown for code elements")
    base.VERSION.changed("1.5.3", "`components.ReportingHydrographicMap` markdown usage extended")
    base.VERSION.added("1.7.0", "Type hints to `components.ReportingHydrographicMap` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.ReportingHydrographicMap` with base class")
    base.VERSION.changed(
        "1.8.0", "Replaced Legacy format strings by f-strings in `components.ReportingHydrographicMap` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.ReportingHydrographicMap` ")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a ReportingHydrographicMap component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(ReportingHydrographicMap, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "Hydrography",
                    (attrib.Class(list[bytes], 1),  attrib.Scales("space/base_geometry", 1)),
                    self.default_observer
                ),
                base.Input(
                    "HydrographicReachIds",
                    (attrib.Class(list[int], 1), attrib.Scales("space/base_geometry", 1)),
                    self.default_observer
                ),
                base.Input(
                    "SimulationStart",
                    (attrib.Class(datetime.date, 1), attrib.Scales("global", 1)),
                    self.default_observer
                ),
                base.Input(
                    "DisplayedTime",
                    (attrib.Class(datetime.datetime, 1), attrib.Scales("global", 1)),
                    self.default_observer
                ),
                base.Input("Values", [attrib.Class(numpy.ndarray, 1)], self.default_observer),
                base.Input(
                    "ValuesReachIds",
                    (attrib.Class(list[int], 1), attrib.Scales("space/reach", 1)),
                    self.default_observer
                ),
                base.Input("Title", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input("OutputFile", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input("DisplayedUnit", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input(
                    "ScaleMaxValue", (attrib.Class(float, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input(
                    "ScaleMinValue", (attrib.Class(float, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input(
                   "ValuesNormalization", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input(
                    "ColorMap", (attrib.Class(list[str], 1), attrib.Scales("global", 1)), self.default_observer)
            ]
        )
        self._outputs = base.OutputContainer(self, [])

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        if self._inputs["DisplayedUnit"].has_provider:
            self._inputs["Values"].attributes.append(attrib.Unit(self._inputs["DisplayedUnit"].read().values, 1))
        hydrography = self._inputs["Hydrography"].read().values
        hydrography_reaches = self._inputs["HydrographicReachIds"].read().values
        simulation_start = self._inputs["SimulationStart"].read().values
        displayed_time = self._inputs["DisplayedTime"].read().values
        values_description = self._inputs["Values"].describe()
        if "time/hour" in values_description["scales"]:
            time_index = int(
                (displayed_time - datetime.datetime.combine(simulation_start, datetime.time())).total_seconds() / 3600)
        elif "time/year" in values_description["scales"]:
            time_index = displayed_time.year - simulation_start.year
        else:
            raise ValueError("Cannot handle temporal scale of values")
        reach_count = self._inputs["Values"].describe()["shape"][1]
        values = self._inputs["Values"].read(slices=(time_index, slice(0, reach_count))).values
        value_reaches = self._inputs["ValuesReachIds"].read().values
        fig = matplotlib.pyplot.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        min_x, max_x = float("Inf"), float("-Inf")
        min_y, max_y = float("Inf"), float("-Inf")
        min_value, max_value = min(values), max(values)
        if self._inputs["ScaleMaxValue"].has_provider:
            max_value = self._inputs["ScaleMaxValue"].read().values
        if self._inputs["ScaleMinValue"].has_provider:
            min_value = self._inputs["ScaleMinValue"].read().values
        else:
            min_value = max(min_value, 1e-9)
        normalization = matplotlib.colors.Normalize(vmin=min_value, vmax=max_value, clip=True)
        na_value = -99
        if self._inputs["ValuesNormalization"].has_provider:
            values_normalization = self._inputs["ValuesNormalization"].read().values
            if values_normalization == "log10":
                normalization = matplotlib.colors.LogNorm(vmin=min_value, vmax=max_value, clip=True)
                na_value = 0
            else:
                raise ValueError(f"Unknown normalization option {values_normalization}")
        color_map = self._inputs["ColorMap"].read().values \
            if self._inputs["ColorMap"].has_provider \
            else ("green", "yellow", "red")

        color_mapper = matplotlib.cm.ScalarMappable(
            norm=normalization,
            cmap=matplotlib.colors.LinearSegmentedColormap.from_list("", color_map)
        )
        for index, wkb in enumerate(hydrography):
            geometry = osgeo.ogr.CreateGeometryFromWkb(wkb)
            x = [geometry.GetX(i) for i in range(geometry.GetPointCount())]
            min_x = min(min_x, min(x))
            max_x = max(max_x, max(x))
            y = [geometry.GetY(i) for i in range(geometry.GetPointCount())]
            min_y = min(min_y, min(y))
            max_y = max(max_y, max(y))
            codes = [matplotlib.path.Path.LINETO] * len(x)
            codes[0] = matplotlib.path.Path.MOVETO
            path = matplotlib.path.Path(numpy.column_stack((x, y)), codes)
            value = values[value_reaches.index(hydrography_reaches[index])]
            ax.add_patch(
                matplotlib.patches.PathPatch(
                    path,
                    fill=False,
                    color=(.67, .67, .67, 1) if value == na_value else color_mapper.to_rgba(value),
                    linewidth=2 if value == na_value else 3
                )
            )
        ax.set_xlim(min_x - (max_x - min_x) * .05, max_x + (max_x - min_x) * .05)
        ax.set_ylim(min_y - (max_y - min_y) * .05, max_y + (max_y - min_y) * .05)
        ax.set_aspect(1)
        fig.colorbar(color_mapper, ax=ax)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        ax.set_title(self._inputs["Title"].read().values)
        output_file = self._inputs["OutputFile"].read().values
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        matplotlib.pyplot.savefig(output_file)

    @staticmethod
    def draw(
            data_store: str,
            hydrography: str,
            hydrographic_reach_ids: str,
            simulation_start: datetime.date,
            displayed_time: datetime.date,
            values: str,
            values_reach_ids: str,
            title: str,
            output_file: str,
            displayed_unit: typing.Optional[str] = None,
            scale_max_value: typing.Optional[float] = None,
            scale_min_value: typing.Optional[float] = None,
            values_normalization: typing.Optional[str] = None,
            color_map: typing.Optional[typing.Sequence[str]] = None
    ) -> None:
        """
        Draws a map displaying the distribution of values in a hydrographic network.

        Args:
            data_store: The file path where the X3df store is located.
            hydrography: The name of the dataset containing the hydrographic network geometries.
            hydrographic_reach_ids: The name of the dataset containing the identifiers of reaches.
            simulation_start: The name of the dataset containing the first day of the simulation.
            displayed_time: The time displayed in the map as a datetime.date.
            values: The name of the dataset containing the values to map onto the hydrographic network.
            values_reach_ids: The name of the dataset containing the reach identifiers according to the values.
            title: The title of the plot.
            output_file: A valid path to a file where the plot is written to.
            displayed_unit: The unit in which values should be displayed.
            scale_max_value: The maximum value to which the legend is scaled.
            scale_min_value: The minimum value to which the legend is scaled.
            values_normalization: The normalization applied to the values.
            color_map: The color map used for displaying the values as a list of strings.

        Returns:
            Nothing.
        """
        base.reporting(
            data_store,
            ReportingHydrographicMap,
            (
                ("DisplayedTime", displayed_time),
                ("Title", title),
                ("OutputFile", output_file),
                ("DisplayedUnit", displayed_unit),
                ("ScaleMaxValue", scale_max_value),
                ("ScaleMinValue", scale_min_value),
                ("ValuesNormalization", values_normalization),
                ("ColorMap", color_map)
            ),
            (
                ("Hydrography", hydrography),
                ("HydrographicReachIds", hydrographic_reach_ids),
                ("SimulationStart", simulation_start),
                ("Values", values),
                ("ValuesReachIds", values_reach_ids)
            )
        )
