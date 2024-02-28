"""Imports of the `components` module."""
from .BeeForage import *
from .BeeHave import *
from .CsvReader import *
from .DeleteFolder import *
from .DepositionToPecSoil import *
from .DepositionToReach import *
from .DoseResponse import *
from .EnvironmentalFate import *
from .ExportData import *
from .ReportingDistribution import *
from .ReportingHydrographicMap import *
from .HydrologyFromTimeSeries import *
from .LandCoverToVegetation import *
from .LandscapeScenarioPreparation import *
from .LandscapeScenario import *
from .MarsWeather import *
from .MarsWeather2 import *
from .PpmCalendar import *
from .Soil import *
from .TerRQ import *
from .UserParameters import *
from .WaterTemperatureFromAirTemperature import *

import base.VERSION

# CHANGELOG
base.VERSION.added("1.1.1", "`components` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `components` namespace")
base.VERSION.added("1.4.1", "Changelog in `components` ")
base.VERSION.changed("1.4.1", "Removed `components.VERSION` ")
base.VERSION.changed("1.4.9", "`components` imports updated to reflect renamed components")
base.VERSION.changed("1.6.1", "`components` imports updated to reflect renamed components")
base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.__init__` ")
base.VERSION.added("1.14.0", "default mappings for land cover to vegetation and vegetation to bee forage")
base.VERSION.added("1.14.0", "default dictionary for vegetation classes")
