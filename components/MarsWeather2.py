"""
A xLandscape component for providing weather data downloaded from Agri4Cast.
"""
import datetime
import numpy
import base
import attrib
import typing
import xml.etree.ElementTree
import os


class MarsWeather2(base.Component):
    """
    The MarsWeather2 component is similar to the MarsWeather component in regard of providing weather data from CSV
    files downloaded from Agri4Cast. Unlike the MarsWeather component, the MarsWeather2 component does, however,
    allow to provide weather data for multiple weather regions in a landcape at once. This is achieved by providing
    multiple CSV files - one for each Agri4Cast grid cell - and accompanying it by an XML file describing the weather
    files and linking them to the corresponding CSV files.
    """
    # CHANGELOG
    base.VERSION.added("1.16.0", "`components.MarsWeather2` component")
    base.VERSION.changed("1.18.0", "Code refactory in `components.MarsWeather2`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a MarsWeather component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(MarsWeather2, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "FilePath",
                    (attrib.Class(str, 1), attrib.Unit(None, 1)),
                    self.default_observer,
                    description="The file path to the MARS weather file.",
                )
            ]
        )
        self._outputs = base.OutputContainer(
            self,
            (
                base.Output(
                    "TEMPERATURE_AVG",
                    default_store,
                    self,
                    description="The average air temperature."
                ),
                base.Output(
                    "PRECIPITATION",
                    default_store,
                    self,
                    description="The total precipitation."
                ),
                base.Output(
                    "ET0",
                    default_store,
                    self,
                    description="The potential evapotranspiration."
                ),
                base.Output(
                    "WINDSPEED",
                    default_store,
                    self,
                    description="The average wind speed."
                ),
                base.Output(
                    "RADIATION",
                    default_store,
                    self,
                    description="The solar radiation."
                ),
                base.Output(
                    "TEMPERATURE_MAX",
                    default_store,
                    self,
                    description="The maximum temperature."
                ),
                base.Output(
                    "TEMPERATURE_MIN",
                    default_store,
                    self,
                    description="The minimum temperature."
                ),
                base.Output(
                    "VAPOURPRESSURE",
                    default_store,
                    self,
                    description="The vapor pressure."
                ),
                base.Output(
                    "Latitude",
                    default_store,
                    self,
                    description="The latitude of the grid cell center."
                ),
                base.Output(
                    "Longitude",
                    default_store,
                    self,
                    description="The longitude of the grid cell center."
                ),
                base.Output(
                    "Altitude",
                    default_store,
                    self,
                    description="The (average?) altitude of the grid cell center."
                ),
                base.Output(
                    "WeatherRegions",
                    default_store,
                    self,
                    description="The weather regions."
                )
            )
        )
        self._units = {
            "TEMPERATURE_AVG": "°C",
            "PRECIPITATION": "mm",
            "ET0": "mm",
            "WINDSPEED": "m/s",
            "RADIATION": "kJ/m²",
            "TEMPERATURE_MAX": "°C",
            "TEMPERATURE_MIN": "°C",
            "VAPOURPRESSURE": "hPa"
        }

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        config_file = self.inputs["FilePath"].read().values
        config = xml.etree.ElementTree.parse(config_file).getroot()
        first_date: datetime.date = base.convert(config.find("FirstDate"))
        last_date = base.convert(config.find("LastDate"))
        sites = config.findall("Site")
        self.outputs["WeatherRegions"].set_values(
            [x.attrib["name"] for x in sites],
            scales="space/weather_region",
            element_names=(self.outputs["WeatherRegions"],),
            unit=None
        )
        self.outputs["Latitude"].set_values(
            [base.convert(x.find("Latitude")) for x in sites],
            scales="space/weather_region",
            element_names=(self.outputs["WeatherRegions"],),
            unit="°"
        )
        self.outputs["Longitude"].set_values(
            [base.convert(x.find("Longitude")) for x in sites],
            scales="space/weather_region",
            element_names=(self.outputs["WeatherRegions"],),
            unit="°"
        )
        self.outputs["Altitude"].set_values(
            [base.convert(x.find("Altitude")) for x in sites],
            scales="space/weather_region",
            element_names=(self.outputs["WeatherRegions"],),
            unit="m"
        )
        weather_data = {k: numpy.full(((last_date - first_date).days + 1, len(sites)), numpy.nan) for k in self._units}
        for i, site in enumerate(sites):
            with open(os.path.join(os.path.dirname(config_file), site.find("File").text)) as f:
                data = f.readlines()
            data = [line[:-1].split(",") for line in data]
            for component_output in weather_data:
                if component_output in data[0]:
                    value_idx = data[0].index(component_output)
                    day_idx = data[0].index("DAY")
                    month_idx = data[0].index("MONTH")
                    year_idx = data[0].index("YEAR")
                    for row in data[1:]:
                        time_index = (
                                datetime.date(int(row[year_idx]), int(row[month_idx]), int(row[day_idx])) -
                                first_date
                        ).days
                        weather_data[component_output][time_index, i] = float(row[value_idx])
                else:
                    self.default_observer.write_message(
                        2, f"Weather file does not contain field {component_output}")
        for output_name, output_data in weather_data.items():
            self.outputs[output_name].set_values(
                output_data,
                scales="time/day, space/weather_region",
                unit=self._units[output_name],
                offset=(first_date, None),
                element_names=(None, self.outputs["WeatherRegions"]),
                requires_indexing=True
            )
