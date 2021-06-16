"""
Class definition for the HydrologyFromTimeSeries Landscape Model component.
"""
import datetime
import h5py
import numpy as np
import base
import attrib
import os


class HydrologyFromTimeseries(base.Component):
    """
    Loads hydrological data from an HDF5 file.

    INPUTS
    Timeseries: A valid file path to the input HDF5 data. A string of global scale. Value has no unit.
    FromTime: The start time of the requested hydrology. A datetime.date of global scale. Value has no unit.
    ToTime: The end time of the requested hydrology. A datetime.date of global scale. Value has no unit.
    InflowTimeseriesPath: The pah where reach-inflows are stored. A string of global scale. Value has no unit.
    ImportInflows: Specifies whether reach inflows from fields are imported. A bool of global scale. Value has no unit.

    OUTPUTS
    Flow: The water flow. A NumPy array of scales time/hour, space/reach. Values have a unit of m³/d.
    Depth: The water depth. A NumPy array of scales time/hour, space/reach. Values have a unit m.
    Reaches: The numeric identifier of reaches. A list[int] of scale space/reach.
    TimeseriesStart: The start time of the hydrological data. A datetime.datetime of global scale. Value has no unit.
    TimeseriesEnd: The end time of the hydrological data. A datetime.datetime of global scale. Value has no unit.
    Volume: The water volume. A NumPy array of scales time/hour, space/reach. Values have a unit of m³.
    Area: The water surface area. A NumPy array of scales time/hour, space/reach. Values have a unit of m².
    InflowReaches: Identifier that receive inflows from fields. A NumPy array of scale space/reach2. Values have no
    unit.
    Inflow: Inflows into reaches from fields. A NumPy array of scale time/hour, space/reach2. Values have a unit of
    m³/d.
    """
    # CHANGELOG
    base.VERSION.added("1.2.20", "components.HydrologyFromTimeSeries component")
    base.VERSION.changed("1.2.28", "components.HydrologyFromTimeSeries no longer depends on hydrography input")
    base.VERSION.changed("1.2.36", "components.HydrologyFromTimeSeries provides water body volume and wet surface area")
    base.VERSION.changed("1.2.36", "components.HydrologyFromTimeSeries allows specifying time frame")
    base.VERSION.changed("1.3.22", "More explanatory error messages in components.HydrologyFromTimeSeries")
    base.VERSION.changed("1.3.33", "components.HydrologyFromTimeSeries checks input types strictly")
    base.VERSION.changed("1.3.33", "components.HydrologyFromTimeSeries checks for physical units")
    base.VERSION.changed("1.3.33", "components.HydrologyFromTimeSeries reports physical units to the data store")
    base.VERSION.changed("1.3.33", "components.HydrologyFromTimeSeries checks for scales")
    base.VERSION.added("1.4.1", "Changelog in components.HydrologyFromTimeSeries")
    base.VERSION.changed("1.4.1", "components.HydrologyFromTimeSeries class documentation")
    base.VERSION.changed("1.4.2", "new components.HydrologyFromTimeSeries inputs InflowTimeseriesPath, ImportInflows")
    base.VERSION.changed("1.4.2", "new components.HydrologyFromTimeSeries outputs InflowReaches and Inflow")
    base.VERSION.changed("1.4.2", "components.HydrologyFromTimeSeries (optionally) reads inflows from fields")
    base.VERSION.changed("1.4.2", "Changelog description")

    def __init__(self, name, observer, store):
        super(HydrologyFromTimeseries, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Timeseries",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "FromTime",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ToTime",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "InflowTimeseriesPath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ImportInflows",
                (attrib.Class(bool, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("Flow", store, self),
            base.Output("Depth", store, self),
            base.Output("Reaches", store, self),
            base.Output("TimeseriesStart", store, self),
            base.Output("TimeseriesEnd", store, self),
            base.Output("Volume", store, self),
            base.Output("Area", store, self),
            base.Output("InflowReaches", store, self),
            base.Output("Inflow", store, self)
        ])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        timeseries = self.inputs["Timeseries"].read().values
        h5 = h5py.File(timeseries, "r")
        flow = h5["flow"]
        depth = h5["depth"]
        volume = h5["volume"]
        area = h5["area"]
        reaches = h5["reaches"][()]
        number_reaches = flow.shape[1]
        from_time = self.inputs["FromTime"].read().values
        to_time = self.inputs["ToTime"].read().values
        number_hours = int(((to_time - from_time).days + 1) * 24)
        timeseries_start = datetime.datetime.strptime(h5["time_from"][0].decode("ascii"), "%Y-%m-%dT%H:%M")
        timeseries_end = datetime.datetime.strptime(h5["time_to"][0].decode("ascii"), "%Y-%m-%dT%H:%M")
        offset_hours = int((datetime.datetime.combine(from_time, datetime.time(1)) - timeseries_start).days * 24)
        if offset_hours < 0:
            raise ValueError(
                "Requested {} too early values; values available for {} to {}".format(-offset_hours, timeseries_start,
                                                                                      timeseries_end))
        if number_hours - flow.shape[0] > 0:
            raise ValueError(
                "Requested {} too late values; values available for {} to {}".format(number_hours - flow.shape[0],
                                                                                     timeseries_start, timeseries_end))
        self.outputs["Flow"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            dtype=np.float,
            chunks=(number_hours, 1),
            scales="time/hour, space/reach",
            unit="m³/d"
        )
        self.outputs["Depth"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            dtype=np.float,
            chunks=(number_hours, 1),
            scales="time/hour, space/reach",
            unit="m"
        )
        self.outputs["Volume"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            dtype=np.float,
            chunks=(number_hours, 1),
            scales="time/hour, space/reach",
            unit="m³"
        )
        self.outputs["Area"].set_values(
            np.ndarray,
            shape=(number_hours, number_reaches),
            dtype=np.float,
            chunks=(number_hours, 1),
            scales="time/hour, space/reach",
            unit="m²"
        )
        for i in range(number_reaches):
            self.outputs["Flow"].set_values(flow[(slice(offset_hours, offset_hours + number_hours, 1), i)],
                                            slices=(slice(number_hours), i), create=False)
            self.outputs["Depth"].set_values(depth[(slice(offset_hours, offset_hours + number_hours, 1), i)],
                                             slices=(slice(number_hours), i), create=False)
            self.outputs["Volume"].set_values(volume[(slice(offset_hours, offset_hours + number_hours, 1), i)],
                                              slices=(slice(number_hours), i), create=False)
            self.outputs["Area"].set_values(area[(slice(offset_hours, offset_hours + number_hours, 1), i)],
                                            slices=(slice(number_hours), i), create=False)
        self.outputs["Reaches"].set_values(reaches, scales="space/reach")
        self.outputs["TimeseriesStart"].set_values(datetime.datetime.combine(from_time, datetime.time(1)))
        self.outputs["TimeseriesEnd"].set_values(datetime.datetime.combine(to_time, datetime.time()))
        if self._inputs["ImportInflows"].read().values:
            inflow_path = self._inputs["InflowTimeseriesPath"].read().values
            inflow_files = os.listdir(inflow_path)
            inflow_reaches = [int(f[1:-4]) for f in inflow_files]
            self._outputs["InflowReaches"].set_values(inflow_reaches, scales="space/reach2")
            self.outputs["Inflow"].set_values(
                np.ndarray,
                shape=(number_hours, len(inflow_reaches)),
                dtype=np.float,
                chunks=(number_hours, 1),
                scales="time/hour, space/reach2",
                unit="m³/d"
            )
            for reach_index, inflow_file in enumerate(inflow_files):
                self.default_observer.write_message(5, "Importing reach inflows from " + inflow_file + "...")
                inflows = np.full((number_hours,), np.inf)
                with open(os.path.join(inflow_path, inflow_file)) as f:
                    lines = f.readlines()
                    data = [line[:-1].split(",") for line in lines[1:]]
                    for record in data:
                        if record[0] != inflow_file[:-4]:
                            raise ValueError("Unexpected reach in file: " + inflow_file)
                        time_index = int((datetime.datetime.strptime(
                            record[1], "%Y-%m-%dT%H:%M") - timeseries_start).total_seconds() / 3600) - offset_hours
                        if 0 <= time_index < number_hours:
                            inflows[time_index] = float(record[2])
                    if np.any(np.isinf(inflows)):
                        raise ValueError("Unexpected temporal layout in file: " + inflow_file)
                    self.outputs["Inflow"].set_values(inflows, slices=(slice(number_hours), reach_index), create=False)
        return
