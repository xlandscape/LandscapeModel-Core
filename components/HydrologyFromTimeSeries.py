"""Class definition for the HydrologyFromTimeSeries Landscape Model component."""
import datetime
import h5py
import numpy as np
import base
import attrib
import os
import typing


class HydrologyFromTimeSeries(base.Component):
    """
    Loads hydrological data from a hydrological scenario. A hydrological scenario is normally part of a scenario
    intended for aquatic simulations and consists of the following elements: a HDF5-file that contains the hydrological
    parameters flow, depth, volume and area (see output description for more details) plus some metadata, and, possibly,
    a folder containing CSV files detailing the lateral inflows of reaches.
    """
    # CHANGELOG
    base.VERSION.added("1.2.20", "`components.HydrologyFromTimeSeries` component")
    base.VERSION.changed("1.2.28", "`components.HydrologyFromTimeSeries` no longer depends on hydrography input")
    base.VERSION.changed(
        "1.2.36", "`components.HydrologyFromTimeSeries` provides water body volume and wet surface area")
    base.VERSION.changed("1.2.36", "`components.HydrologyFromTimeSeries` allows specifying time frame")
    base.VERSION.changed("1.3.22", "More explanatory error messages in `components.HydrologyFromTimeSeries` ")
    base.VERSION.changed("1.3.33", "`components.HydrologyFromTimeSeries` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.HydrologyFromTimeSeries` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.HydrologyFromTimeSeries` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.HydrologyFromTimeSeries` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.HydrologyFromTimeSeries` ")
    base.VERSION.changed("1.4.1", "`components.HydrologyFromTimeSeries` class documentation")
    base.VERSION.changed("1.4.2", "new `components.HydrologyFromTimeSeries` inputs InflowTimeSeriesPath, ImportInflows")
    base.VERSION.changed("1.4.2", "new `components.HydrologyFromTimeSeries` outputs InflowReaches and Inflow")
    base.VERSION.changed("1.4.2", "`components.HydrologyFromTimeSeries` (optionally) reads inflows from fields")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "renamed `components.HydrologyFromTimeSeries` component")
    base.VERSION.changed("1.6.0", "`components.HydrologyFromTimeSeries` casts exported WKB geometries to bytes")
    base.VERSION.added("1.7.0", "Type hints to `components.HydrologyFromTimeSeries` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.HydrologyFromTimeSeries` with base class")
    base.VERSION.changed(
        "1.8.0", "Replaced Legacy format strings by f-strings in `components.HydrologyFromTimeSeries` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.HydrologyFromTimeSeries` ")
    base.VERSION.changed("1.10.0", "`components.HydrologyFromTimeSeries` reports global scale of time span outputs")
    base.VERSION.changed("1.10.0", "`components.HydrologyFromTimeSeries` reports element names of outputs")
    base.VERSION.added("1.10.3", "Further consistency checks to `HydrologyFromTimeSeries` component")
    base.VERSION.changed("1.11.0", "`components.HydrologyFromTimeSeries` specifies offsets of outputs")
    base.VERSION.fixed(
        "1.14.4", "Fixed dimensionality of `Deposition` output in `components.HydrologyFromTimeSeries` component")
    base.VERSION.changed("1.15.6", "Updated description of `HydrologyFromTimeSeries` component")
    base.VERSION.added("1.15.6", "Input descriptions to `HydrologyFromTimeSeries` component")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a HydrologyFromTimeSeries component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(HydrologyFromTimeSeries, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "TimeSeries",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="A valid file path to the input HDF5 data. This data must follow a specific format. See "
                            "any of the publicly available hydrological scenarios for an example."
            ),
            base.Input(
                "FromTime",
                (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The start time of the hydrological data. This specifies the first date for which "
                            "hydrological data is imported into the Landscape Model. It must lay within the time frame "
                            "for which data is available. Consult the scenario documentation for this time frame."
            ),
            base.Input(
                "ToTime",
                (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The end time of the hydrological data.This specifies the last date for which "
                            "hydrological data is imported into the Landscape Model. It must lay within the time frame "
                            "for which data is available. Consult the scenario documentation for this time frame."
            ),
            base.Input(
                "InflowTimeSeriesPath",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The path where reach-inflows are stored. This path must contain a CSV file for each reach "
                            "that receives lateral inflows. See any of the publicly available hydrological scenarios "
                            "to learn about the specific format of the CSV files."
            ),
            base.Input(
                "ImportInflows",
                (attrib.Class(bool), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="Specifies whether lateral inflows from fields are imported. Setting this input to `False` "
                            "will skip the import of CSV files from the `InflowTimeSeriesPath`. This decreases the "
                            "processing time of the component, but can only be done if none of the components in the "
                            "simulation require data on lateral inflows. This input should also be set to `False` if "
                            "the hydrological scenario does not contain information on lateral inflows, In this case, "
                            "it will not be possible to run components that require according data."
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output(
                "Flow",
                default_store,
                self,
                {"data_type": np.float, "scales": "time/hour, space/reach", "unit": "m³/d"},
                attribute_hints={
                    "type": np.ndarray,
                    "shape": (
                        "the number of hours represented by the time span between the `FromTime` and the `ToTime`",
                        "the number of reaches as stored in the `TimeSeries` input"
                    ),
                    "chunks": "for fast retrieval of timeseries",
                    "element_names": (None, "as specified by the `Reaches` output"),
                    "offset": ("as specified by the `FromTime` input", None)
                }
            ),
            base.Output(
                "Depth",
                default_store,
                self,
                {"data_type": np.float, "scales": "time/hour, space/reach", "unit": "m"},
                attribute_hints={
                    "type": np.ndarray,
                    "shape": (
                        "the number of hours represented by the time span between the `FromTime` and the `ToTime`",
                        "the number of reaches as stored in the `TimeSeries` input"
                    ),
                    "chunks": "for fast retrieval of timeseries",
                    "element_names": (None, "as specified by the `Reaches` output"),
                    "offset": ("as specified by the `FromTime` input", None)
                }
            ),
            base.Output(
                "Reaches",
                default_store,
                self,
                {"scales": "space/reach"},
                "This output lists the element names of the reaches as retrieved from the `TimeSeries` input. All "
                "outputs that have a scale of `space/reach` report reaches in the order specified by this input, "
                "except the `Inflow` output which reports reaches in the order of the `InflowReaches` output.",
                {
                    "type": np.ndarray,
                    "shape": "the number of reaches as stored in the `TimeSeries` input",
                    "element_names": ("as specified by the output itself",)
                }
            ),
            base.Output("TimeSeriesStart", default_store, self, {"scales": "global"}),
            base.Output("TimeSeriesEnd", default_store, self, {"scales": "global"}),
            base.Output(
                "Volume",
                default_store,
                self,
                {"data_type": np.float, "scales": "time/hour, space/reach", "unit": "m³"},
                attribute_hints={
                    "type": np.ndarray,
                    "shape": (
                        "the number of hours represented by the time span between the `FromTime` and the `ToTime`",
                        "the number of reaches as stored in the `TimeSeries` input"
                    ),
                    "chunks": "for fast retrieval of timeseries",
                    "element_names": (None, "as specified by the `Reaches` output"),
                    "offset": ("as specified by the `FromTime` input", None)
                }
            ),
            base.Output(
                "Area",
                default_store,
                self,
                {"data_type": np.float, "scales": "time/hour, space/reach", "unit": "m²"},
                attribute_hints={
                    "type": np.ndarray,
                    "shape": (
                        "the number of hours represented by the time span between the `FromTime` and the `ToTime`",
                        "the number of reaches as stored in the `TimeSeries` input"
                    ),
                    "chunks": "for fast retrieval of timeseries",
                    "element_names": (None, "as specified by the `Reaches` output"),
                    "offset": ("as specified by the `FromTime` input", None)
                }
            ),
            base.Output(
                "InflowReaches",
                default_store,
                self,
                {"scales": "space/reach"},
                "This output lists the element names of reaches as reported by the `Inflow` output. This order may "
                "differ from the order of reaches in all other outputs with scale `space/reach`.",
                {
                    "type": np.ndarray,
                    "shape": ("the number of reaches for which inflow-data is available",),
                    "element_names": ("as specified by the output itself",)
                }
            ),
            base.Output(
                "Inflow",
                default_store,
                self,
                {"data_type": np.float, "scales": "time/hour, space/reach", "unit": "m³/d"},
                attribute_hints={
                    "type": np.ndarray,
                    "shape": (
                        "the number of hours represented by the time span between the `FromTime` and the `ToTime`",
                        "the number of reaches as stored in the `InflowReaches` input"
                    ),
                    "chunks": "for fast retrieval of timeseries",
                    "element_names": (None, "as specified by the `InflowReaches` output"),
                    "offset": ("as specified by the `FromTime` input", None)
                }
            )
        ])
        if self.default_observer:
            self.default_observer.write_message(
                3,
                "The TimeSeriesStart output will be removed from a future version of the HydrologyFromTimeSeries "
                "component",
                "The according information can be retrieved from the outputs with scale `time/hour`"
            )
            self.default_observer.write_message(
                3,
                "The TimeSeriesEnd output will be removed from a future version of the HydrologyFromTimeSeries "
                "component",
                "The according information can be retrieved from the outputs with scale `time/hour`"
            )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        time_series = self.inputs["TimeSeries"].read().values
        h5 = h5py.File(time_series)
        flow = h5["flow"]
        depth = h5["depth"]
        volume = h5["volume"]
        area = h5["area"]
        reaches = h5["reaches"][()]
        number_reaches = flow.shape[1]
        from_time = self.inputs["FromTime"].read().values
        to_time = self.inputs["ToTime"].read().values
        number_hours = int(((to_time - from_time).days + 1) * 24)
        time_series_start = datetime.datetime.strptime(h5["time_from"][0].decode("ascii"), "%Y-%m-%dT%H:%M")
        time_series_end = datetime.datetime.strptime(h5["time_to"][0].decode("ascii"), "%Y-%m-%dT%H:%M")
        offset_time = datetime.datetime.combine(from_time, datetime.time(1))
        offset_hours = int((offset_time - time_series_start).days * 24)
        time_series_length = int((time_series_end - time_series_start).total_seconds() / 3600) + 1
        if time_series_length != flow.shape[0] or time_series_length != depth.shape[0] or \
                time_series_length != volume.shape[0] or time_series_length != area.shape[0]:
            self.default_observer.write_message(2, "Temporal inconsistency in hydrological scenario")
            self.default_observer.write_message(2, "It is highly recommended checking your hydrological scenario")
        if offset_hours < 0:
            raise ValueError(
                f"Requested {-offset_hours} too early values; values available for {time_series_start} to "
                f"{time_series_end}"
            )
        if number_hours - flow.shape[0] > 0:
            raise ValueError(
                f"Requested {number_hours - flow.shape[0]} too late values; values available for {time_series_start} "
                f"to {time_series_end}"
            )
        self.outputs["Reaches"].set_values(reaches, element_names=(self.outputs["Reaches"],))
        self.outputs["Flow"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            chunks=(number_hours, 1),
            element_names=(None, self.outputs["Reaches"]),
            offset=(offset_time, None)
        )
        self.outputs["Depth"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            chunks=(number_hours, 1),
            element_names=(None, self.outputs["Reaches"]),
            offset=(offset_time, None)
        )
        self.outputs["Volume"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            chunks=(number_hours, 1),
            element_names=(None, self.outputs["Reaches"]),
            offset=(offset_time, None)
        )
        self.outputs["Area"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            chunks=(number_hours, 1),
            element_names=(None, self.outputs["Reaches"]),
            offset=(offset_time, None)
        )
        for i in range(number_reaches):
            self.outputs["Flow"].set_values(
                flow[(slice(offset_hours, offset_hours + number_hours, 1), slice(i, i + 1))],
                slices=(slice(number_hours), slice(i, i + 1)),
                create=False
            )
            self.outputs["Depth"].set_values(
                depth[(slice(offset_hours, offset_hours + number_hours, 1), slice(i, i + 1))],
                slices=(slice(number_hours), slice(i, i + 1)),
                create=False
            )
            self.outputs["Volume"].set_values(
                volume[(slice(offset_hours, offset_hours + number_hours, 1), slice(i, i + 1))],
                slices=(slice(number_hours), slice(i, i + 1)),
                create=False
            )
            self.outputs["Area"].set_values(
                area[(slice(offset_hours, offset_hours + number_hours, 1), slice(i, i + 1))],
                slices=(slice(number_hours), slice(i, i + 1)),
                create=False
            )
        self.outputs["TimeSeriesStart"].set_values(datetime.datetime.combine(from_time, datetime.time(1)))
        self.outputs["TimeSeriesEnd"].set_values(datetime.datetime.combine(to_time, datetime.time()))
        if self._inputs["ImportInflows"].read().values:
            inflow_path = self._inputs["InflowTimeSeriesPath"].read().values
            inflow_files = os.listdir(inflow_path)
            inflow_reaches = [int(f[1:-4]) for f in inflow_files]
            self.outputs["InflowReaches"].set_values(inflow_reaches, element_names=(self.outputs["InflowReaches"],))
            self.outputs["Inflow"].set_values(
                np.ndarray,
                shape=(number_hours, len(inflow_reaches)),
                chunks=(number_hours, 1),
                element_names=(None, self.outputs["InflowReaches"]),
                offset=(offset_time, None)
            )
            for reach_index, inflow_file in enumerate(inflow_files):
                self.default_observer.write_message(5, f"Importing reach inflows from {inflow_file}...")
                inflows = np.full((number_hours,), np.inf)
                with open(os.path.join(inflow_path, inflow_file)) as f:
                    lines = f.readlines()
                    data = [line[:-1].split(",") for line in lines[1:]]
                    for record in data:
                        if record[0] != inflow_file[:-4]:
                            raise ValueError(f"Unexpected reach in file: {inflow_file}")
                        time_index = int((datetime.datetime.strptime(
                            record[1], "%Y-%m-%dT%H:%M") - time_series_start).total_seconds() / 3600) - offset_hours
                        if 0 <= time_index < number_hours:
                            inflows[time_index] = float(record[2])
                    if np.any(np.isinf(inflows)):
                        raise ValueError(f"Unexpected temporal layout in file: {inflow_file}")
                    self.outputs["Inflow"].set_values(inflows, slices=(slice(number_hours), reach_index), create=False)
