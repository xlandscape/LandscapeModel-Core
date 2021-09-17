"""
Class definition of the PpmCalendar Landscape Model component.
"""
from osgeo import ogr
import datetime
import numpy as np
import random
import base
import attrib
import typing


class PpmCalendar(base.Component):
    """
    Encapsulates the PpmCalendar as a Landscape Model component.

    INPUTS
    SimulationStart: The first day of the simulation. A datetime.date of global scale. Value has no unit.
    SimulationEnd: The last day of the simulation. A datetime.date of global scale. Value has no unit.
    ApplicationWindows: A definition of application windows. A string of global scale. Value has no unit.
    Fields: A list of identifiers of individual geometries. A list[int] of scale space/base_geometry. Values have no
    unit.
    LandUseLandCoverTypes: The land-use and land-cover type of spatial units. A list[int] of scale space/base_geometry.
    Values have no unit.
    TargetLandUseLandCoverType: The land-use or land-cover type that is applied. A string of global scale. Value has no
    unit.
    ApplicationRate: The application rate. A float of global scale. Value has a unit of g/ha.
    TechnologyDriftReduction: The fraction by which spray-drift is reduced due to technological measures. A float of
    global scale. Value has a unit of 1.
    InCropBuffer: An in-crop buffer used during application. A float of scale global. Value has a unit of m.
    InFieldMargin: An margin without crops within fields. A float of scale global. Value has a unit of m.
    FieldGeometries: The geometries of individual landscape parts. A list[bytes] of scale space/base_geometry. Values
    have no unit.
    MinimumAppliedArea: The minimum applied area considered. A float of global scale. Value has a unit of m².
    RandomSeed: A initialization for the random number generator. An int of global scale. Value has a unit of 1.
    ProbabilityFieldApplied: The probability with which a field is applied. A float of global scale. Value has a unit of
    1.

    OUTPUTS
    AppliedFields: The identifiers of applied fields. A NumPy array of scale other/application.
    ApplicationDates: The dates of application. A NumPy array of scale other/application.
    ApplicationRates: The applied rates. A NumPy array of scale other/application. Values have the same unit as the
    input application rate.
    TechnologyDriftReductions: The technological drift reductions. A NumPy array of scale other/application. Values have
    the same unit as the input drift reductions.
    AppliedAreas: The geometries of the applied areas. A list[bytes] of scale other/application. Th values have no unit.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`components.PpmCalendar` component")
    base.VERSION.changed(
        "1.1.1",
        "`components.PpmCalendar` now requires Fields and land-use / land-cover type inputs to be of type list[int]"
    )
    base.VERSION.changed("1.2.5", "`components.PpmCalendar` target land-use / land-cover type input now str")
    base.VERSION.changed("1.2.16", "`components.PpmCalendar` output refactored")
    base.VERSION.changed("1.2.20", "`components.PpmCalendar` no longer outputs SprayApplication objects")
    base.VERSION.changed("1.2.25", "components.PpmCalendar`.RandomSeed` parameter")
    base.VERSION.changed("1.2.27", "`ProbabilityFieldApplied` introduced in `components.PpmCalendar` ")
    base.VERSION.changed("1.3.27", "`components.PpmCalendar` specifies scales")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.PpmCalendar` ")
    base.VERSION.changed("1.4.1", "`components.PpmCalendar` class documentation")
    base.VERSION.changed("1.5.3", "`components.PpmCalendar` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.0", "`components.PpmCalendar` casts exported WKB geometries to bytes")
    base.VERSION.changed("1.6.1", "Renamed some parameters in `components.PpmCalendar` ")
    base.VERSION.added("1.7.0", "Type hints to `components.PpmCalendar` ")
    base.VERSION.added("1.7.0", "Type hints to `components.SprayApplication` ")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.PpmCalendar` with base class")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(PpmCalendar, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "SimulationStart",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "SimulationEnd",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationWindows",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "Fields",
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer
            ),
            base.Input(
                "LandUseLandCoverTypes",
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer
            ),
            base.Input(
                "TargetLandUseLandCoverType",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationRate",
                (attrib.Class(float, 1), attrib.Unit("g/ha", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "TechnologyDriftReduction",
                (attrib.Class(float, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "InCropBuffer",
                (attrib.Class(float, 1), attrib.Unit("m", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "InFieldMargin",
                (attrib.Class(float, 1), attrib.Unit("m", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "FieldGeometries",
                (
                    attrib.Class(list[bytes], 1),
                    attrib.Unit(None, 1),
                    attrib.Scales("space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "MinimumAppliedArea",
                (attrib.Class(float, 1), attrib.Unit("m²", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "RandomSeed",
                (attrib.Class(int, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ProbabilityFieldApplied",
                (attrib.Class(float, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("AppliedFields", default_store, self),
            base.Output("ApplicationDates", default_store, self),
            base.Output("ApplicationRates", default_store, self),
            base.Output("TechnologyDriftReductions", default_store, self),
            base.Output("AppliedAreas", default_store, self)
        ])

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing.
        """
        simulation_start_year = self.inputs["SimulationStart"].read().values.year
        simulation_end_year = self.inputs["SimulationEnd"].read().values.year
        application_windows = [x.split(" to ") for x in self.inputs["ApplicationWindows"].read().values.split(", ")]
        fields = self.inputs["Fields"].read().values
        land_use_types = self.inputs["LandUseLandCoverTypes"].read().values
        target_land_use_type = int(self.inputs["TargetLandUseLandCoverType"].read().values)
        application_rate = self.inputs["ApplicationRate"].read()
        technology_drift_reduction = self.inputs["TechnologyDriftReduction"].read()
        in_crop_buffer = self.inputs["InCropBuffer"].read().values
        in_field_margin = self.inputs["InFieldMargin"].read().values
        minimum_applied_area = self.inputs["MinimumAppliedArea"].read().values
        random_seed = self.inputs["RandomSeed"].read().values
        probability_field_applied = self.inputs["ProbabilityFieldApplied"].read().values
        if random_seed is not None and random_seed != 0:
            random.seed(random_seed)
        spray_applications = []
        applied_areas = []
        for i in range(len(land_use_types)):
            if land_use_types[i] == target_land_use_type:
                field = fields[i]
                applied_geometry = ogr.CreateGeometryFromWkb(self.inputs["FieldGeometries"].read(slices=(i,)).values[0])
                if in_crop_buffer + in_field_margin > 0:
                    applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
                if applied_geometry.GetArea() >= minimum_applied_area and \
                        random.uniform(0, 1) <= probability_field_applied:
                    for year in range(simulation_start_year, simulation_end_year + 1):
                        for applicationWindow in application_windows:
                            window_start = datetime.datetime.strptime(str(year) + "-" + applicationWindow[0],
                                                                      "%Y-%m-%d").date()
                            window_end = datetime.datetime.strptime(str(year) + "-" + applicationWindow[1],
                                                                    "%Y-%m-%d").date()
                            application_date = datetime.datetime.fromordinal(
                                random.randint(window_start.toordinal(), window_end.toordinal()))
                            spray_application = SprayApplication(field, application_date, "PPP", application_rate,
                                                                 technology_drift_reduction, in_crop_buffer)
                            spray_applications.append(spray_application)
                            applied_areas.append(bytes(applied_geometry.ExportToWkb()))
        applied_fields = np.zeros(len(spray_applications), np.int)
        application_dates = np.zeros(len(spray_applications), int)
        application_rates = np.zeros(len(spray_applications))
        technology_drift_reductions = np.zeros(len(spray_applications))
        for i, application in enumerate(spray_applications):
            applied_fields[i] = application.field
            application_dates[i] = application.date.toordinal()
            application_rates[i] = application.application_rate.values
            technology_drift_reductions[i] = application.technology_drift_reduction.values
        self.outputs["AppliedFields"].set_values(applied_fields, scales="other/application")
        self.outputs["ApplicationDates"].set_values(application_dates, scales="other/application")
        self.outputs["ApplicationRates"].set_values(
            application_rates,
            scales="other/application",
            unit=application_rate.unit
        )
        self.outputs["TechnologyDriftReductions"].set_values(
            technology_drift_reductions,
            scales="other/application",
            unit=technology_drift_reduction.unit
        )
        self.outputs["AppliedAreas"].set_values(applied_areas, scales="other/application")


class SprayApplication:
    """
    Describes an individual spray-application.
    """
    def __init__(
            self,
            field: int,
            date: datetime.date,
            ppp: str,
            application_rate: base.Values,
            technology_drift_reduction: base.Values,
            in_crop_buffer: float
    ) -> None:
        self._field = field
        self._date = date
        self._ppp = ppp
        self._applicationRate = application_rate
        self._technologyDriftReduction = technology_drift_reduction
        self._inCropBuffer = in_crop_buffer

    @property
    def application_rate(self) -> base.Values:
        """
        The rate by which a substance is sprayed.
        :return: The application rate.
        """
        return self._applicationRate

    @property
    def date(self) -> datetime.date:
        """
        The date when application takes place.
        :return: The application date.
        """
        return self._date

    @property
    def field(self) -> int:
        """
        The field that is applied
        :return: The field identifier.
        """
        return self._field

    @property
    def in_crop_buffer(self) -> float:
        """
        The in-crop buffer that is applied during application.
        :return: The buffer width in meters.
        """
        return self._inCropBuffer

    @property
    def ppp(self) -> str:
        """
        The plant production product that is applied.
        :return: The identifier of the plant protection product.
        """
        return self._ppp

    @property
    def technology_drift_reduction(self) -> base.Values:
        """
        The drift-reducing technology that is used.
        :return: The fraction of spray-drift that is reduced by applying drift-reducing technology.
        """
        return self._technologyDriftReduction
