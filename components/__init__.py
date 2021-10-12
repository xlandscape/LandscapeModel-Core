"""Imports of the `components` module."""
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
from .LandscapeScenarioPreparation import *
from .LandscapeScenario import *
from .MarsWeather import *
from .PpmCalendar import *
from .TerRQ import *
from .UserParameters import *

import base.VERSION

# CHANGELOG
base.VERSION.added("1.1.1", "`components` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `components` namespace")
base.VERSION.added("1.4.1", "Changelog in `components` ")
base.VERSION.changed("1.4.1", "Removed `components.VERSION` ")
base.VERSION.changed("1.4.9", "`components` imports updated to reflect renamed components")
base.VERSION.changed("1.6.1", "`components` imports updated to reflect renamed components")
base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.__init__` ")
