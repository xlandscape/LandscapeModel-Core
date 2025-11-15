"""Class definition of the PpmCalendar Landscape Model component."""
from osgeo import ogr
import datetime
import numpy as np
import random
import base
import attrib
import typing


class PpmCalendar(base.Component):
    """
    Creates a calendar for pesticide applications for all or some landscape features of a specific type based on fixed
    values for application rate, technological drift reduction, in-crop buffers and in-field margin. Application dates
    are uniformly sampled from application windows. It is possible to specify application sequences by defining more
    than one application window. Whether a specific landscape feature receives an application is controlled by a
    specified probability.
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
    base.VERSION.changed("1.2.27", "`ProbabilityFieldApplied` introduced in `components.PpmCalendar`")
    base.VERSION.changed("1.3.27", "`components.PpmCalendar` specifies scales")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks input types strictly")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks for physical units")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` reports physical units to the data store")
    base.VERSION.changed("1.3.33", "`components.PpmCalendar` checks for scales")
    base.VERSION.added("1.4.1", "Changelog in `components.PpmCalendar`")
    base.VERSION.changed("1.4.1", "`components.PpmCalendar` class documentation")
    base.VERSION.changed("1.5.3", "`components.PpmCalendar` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.0", "`components.PpmCalendar` casts exported WKB geometries to bytes")
    base.VERSION.changed("1.6.1", "Renamed some parameters in `components.PpmCalendar`")
    base.VERSION.added("1.7.0", "Type hints to `components.PpmCalendar`")
    base.VERSION.added("1.7.0", "Type hints to `components.SprayApplication`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.PpmCalendar` with base class")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `components.PpmCalendar`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.PpmCalendar`")
    base.VERSION.changed("1.15.6", "Updated description of `PpmCalendar` component")
    base.VERSION.added("1.15.6", "Input descriptions to `PpmCalendar` component")
    base.VERSION.added("1.15.8", "Documentation of outputs in `PpmCalendar` component")
    base.VERSION.changed("1.16.0", "`TargetLandUseLandCoverType` input in `PpmCalendar` component now is a list of int")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a PpmCalendar.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(PpmCalendar, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "SimulationStart",
                (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The first day of the simulation. No applications prior to this date will be written into "
                            "the calendar."
            ),
            base.Input(
                "SimulationEnd",
                (attrib.Class(datetime.date), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The last day of the simulation. No applications after this date will be written into the "
                            "calendar."
            ),
            base.Input(
                "ApplicationWindows",
                (attrib.Class(str), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="A definition of application windows. The value must follow the format "
                            "`MM-DD to MM-DD[, MM-DD to MM-DD...]`, where `MM` is the month of year and `DD` is the "
                            "day of month. Application dates are sampled within the specified time window for each "
                            "year in the period from `SimulationStart` to `SimulationEnd` individually. If multiple "
                            "application windows are specified, a single application will take place in each of the "
                            "windows, sampled individually."
            ),
            base.Input(
                "Fields",
                (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                self.default_observer,
                description="A list of identifiers of individual geometries. This input will be removed in a future "
                            "version of the `PpmCalendar` component."
            ),
            base.Input(
                "LandUseLandCoverTypes",
                (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                self.default_observer,
                description="The land-use and land-cover type of spatial units. This information is used to determine "
                            "applied landscape elements (i.e., target fields), by only considering base geometries "
                            "that have a land use/land cover type equal to the `TargetLandUseLandCoverType` input."
            ),
            base.Input(
                "TargetLandUseLandCoverType",
                (attrib.Class(list[int]), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="The land-use or land-cover type that receives pesticide applications. It filters the base "
                            "geometries described by the `LandUseLandCoverTypes` input to those that have the "
                            "according value. Only the filtered landscape elements will be considered for "
                            "applications, based on a probability defined by the `ProbabilityFieldApplied` input."
            ),
            base.Input(
                "ApplicationRate",
                (attrib.Class(float), attrib.Unit("g/ha"), attrib.Scales("global")),
                self.default_observer,
                description="The application rate. The `PpmCalendar` component applies the same rate to all "
                            "applications. If your use-case requires different rates, e.g., within an application "
                            "sequence, another component has to be used."
            ),
            base.Input(
                "TechnologyDriftReduction",
                (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer,
                description="The fraction by which spray-drift is reduced due to technological measures. The "
                            "technological drift-reduction has to be a value between `0` and `1`, with `0`"
                            "representing spray-equipment that does not reduce drift-deposition relative to the "
                            "equipment used for the derivation of regulatory drift-depositions values and `1`"
                            "resulting in drift-deposition being prevented entirely due to technological measures."
            ),
            base.Input(
                "InCropBuffer",
                (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                self.default_observer,
                description="An in-crop buffer used during application. The in-crop buffer is a section along the "
                            "boundary of the applied landscape feature of the specified width that does not receive "
                            "applications. The in-crop buffer is geometrically removed from the applied feature to "
                            "determine the applied area."
            ),
            base.Input(
                "InFieldMargin",
                (attrib.Class(float), attrib.Unit("m"), attrib.Scales("global")),
                self.default_observer,
                description="A margin without crops within fields. The in-field margin is an additional section "
                            "between the boundary of the applied landscape feature and the in-crop buffer that is, "
                            "like the in-crop buffer, does not receive applications, but is also considered to have no "
                            "crops planted on it. Like the in-crop buffer, it is geometrically removed from the base "
                            "geometries to derive the geometry of the applied area."
            ),
            base.Input(
                "FieldGeometries",
                (attrib.Class(list[bytes]), attrib.Unit(None), attrib.Scales("space/base_geometry")),
                self.default_observer,
                description="The geometries of individual landscape parts. This input will be removed in a future "
                            "version of the `PpmCalendar` component."
            ),
            base.Input(
                "MinimumAppliedArea",
                (attrib.Class(float), attrib.Unit("m²"), attrib.Scales("global")),
                self.default_observer,
                description="The minimum applied area considered. If the applied area of a landscape feature is, "
                            "after applying the in-crop buffer and in-field margin is smaller than this threshold, "
                            "then no application is scheduled for this feature."
            ),
            base.Input(
                "RandomSeed",
                (attrib.Class(int), attrib.Unit(None), attrib.Scales("global")),
                self.default_observer,
                description="An initialization for the random number generator. Setting this input to a value other "
                            "than `0` seeds the random number generator. This can be useful for debugging or checking "
                            "results. A value of `0` initializes the random number generator randomly."
            ),
            base.Input(
                "ProbabilityFieldApplied",
                (attrib.Class(float), attrib.Unit("1"), attrib.Scales("global")),
                self.default_observer,
                description="The probability with which a field is applied, given as a number between `0` and `1`. A "
                            "landscape feature is excluded entirely from the PPM calendar, if it is not selected for "
                            "application based on the probability specified here. A value of `0` would result in an "
                            "empty PPM calendar, a value of `1` in all landscape features being applied, if no other "
                            "considerations (land use/land cover type filter and minimum area applied) prevent this."
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output(
                "AppliedFields",
                default_store,
                self,
                {"scales": "other/application"},
                "The element names of the applied fields. This output should not be interpreted in a way that "
                "necessarily the entire field received an application, for the spatial extent of the application see "
                "the `AppliedAreas` output, instead. The values of this output link, however, applications to fields, "
                "which can be an interesting parameter for statistics or plotting.",
                {
                    "type": np.ndarray,
                    "data_type": np.int,
                    "shape": ("the number of applications simulated by the component",)
                }
            ),
            base.Output(
                "ApplicationDates",
                default_store,
                self,
                {"scales": "other/application"},
                "The dates at which applications were conducted. Dates are represented as ordinal numbers, as a result "
                "of applying the according function of the `datetime.date` object.",
                {
                    "type": np.ndarray,
                    "data_type": int,
                    "shape": ("the number of applications simulated by the component",)
                }
            ),
            base.Output(
                "ApplicationRates",
                default_store,
                self,
                {"scales": "other/application"},
                "The application rates for each individual application. See the `ApplicationRate` input for further "
                "details.",
                {
                    "type": np.ndarray,
                    "data_type": np.double,
                    "shape": ("the number of applications simulated by the component",),
                    "unit": "the same as that of the `ApplicationRate` input"
                }
            ),
            base.Output(
                "TechnologyDriftReductions",
                default_store,
                self,
                {"scales": "other/application"},
                "The spray-drift reduction by the spray-equipment, expressed as a fraction between `0` and `1`. See "
                "the `TechnologyDriftReduction` input for more details.",
                {
                    "type": np.ndarray,
                    "data_type": np.double,
                    "shape": ("the number of applications simulated by the component",),
                    "unit": "the same as that of the `TechnologyDriftReduction` input"
                }
            ),
            base.Output(
                "AppliedAreas",
                default_store,
                self,
                {"scales": "other/application"},
                "The geometries of the applied areas, represented in Well-Known-Bytes notation. See the `InCropBuffer` "
                "and `InFieldMargin` inputs for further details on how the geometries are derived.",
                {
                    "type": list[bytes],
                    "shape": ("the number of applications simulated by the component",)
                }
            )
        ])
        if self.default_observer:
            self.default_observer.write_message(
                3,
                "The Fields input will be removed in a future version of the PpmCalendar component",
                "The element names will be retrieved from the metadata of the LandUseLandCoverTypes input"
            )
            self.default_observer.write_message(
                3,
                "The FieldGeometries input will be removed in a future version of the PpmCalendar component",
                "The geometries will be retrieved from the metadata of the LandUseLandCoverTypes input"
            )

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
        """
        simulation_start_year = self.inputs["SimulationStart"].read().values.year
        simulation_end_year = self.inputs["SimulationEnd"].read().values.year
        application_windows = [x.split(" to ") for x in self.inputs["ApplicationWindows"].read().values.split(", ")]
        fields = self.inputs["Fields"].read().values
        land_use_types = self.inputs["LandUseLandCoverTypes"].read().values
        target_land_use_types = self.inputs["TargetLandUseLandCoverType"].read().values
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
            if land_use_types[i] in target_land_use_types:
                field = fields[i]
                applied_geometry = ogr.CreateGeometryFromWkb(self.inputs["FieldGeometries"].read(slices=(i,)).values[0])
                if in_crop_buffer + in_field_margin > 0:
                    applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
                if applied_geometry.GetArea() >= minimum_applied_area and \
                        random.uniform(0, 1) <= probability_field_applied:
                    for year in range(simulation_start_year, simulation_end_year + 1):
                        for applicationWindow in application_windows:
                            window_start = datetime.datetime.strptime(
                                f"{year}-{applicationWindow[0]}", "%Y-%m-%d").date()
                            window_end = datetime.datetime.strptime(f"{year}-{applicationWindow[1]}", "%Y-%m-%d").date()
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
        self.outputs["AppliedFields"].set_values(applied_fields)
        self.outputs["ApplicationDates"].set_values(application_dates)
        self.outputs["ApplicationRates"].set_values(application_rates, unit=application_rate.unit)
        self.outputs["TechnologyDriftReductions"].set_values(
            technology_drift_reductions,
            unit=technology_drift_reduction.unit
        )
        self.outputs["AppliedAreas"].set_values(applied_areas)


class SprayApplication:
    """Describes an individual spray-application."""

    def __init__(
            self,
            field: int,
            date: datetime.date,
            ppp: str,
            application_rate: base.Values,
            technology_drift_reduction: base.Values,
            in_crop_buffer: float
    ) -> None:
        """
        Initializes a spray application.

        Args:
            field: The applied field.
            date: The date of application.
            ppp: The product used during application.
            application_rate: The application rate.
            technology_drift_reduction: The rate of drift reduction due to used equipment.
            in_crop_buffer: The in-crop buffer considered during application.
        """
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

        Returns:
            The application rate.
        """
        return self._applicationRate

    @property
    def date(self) -> datetime.date:
        """
        The date when application takes place.

        Returns:
            The application date.
        """
        return self._date

    @property
    def field(self) -> int:
        """
        The field that is applied

        Returns:
            The field identifier.
        """
        return self._field

    @property
    def in_crop_buffer(self) -> float:
        """
        The in-crop buffer that is applied during application.

        Returns:
            The buffer width in meters.
        """
        return self._inCropBuffer

    @property
    def ppp(self) -> str:
        """
        The plant production product that is applied.

        Returns:
            The identifier of the plant protection product.
        """
        return self._ppp

    @property
    def technology_drift_reduction(self) -> base.Values:
        """
        The drift-reducing technology that is used.

        Returns:
            The fraction of spray-drift that is reduced by applying drift-reducing technology.
        """
        return self._technologyDriftReduction
