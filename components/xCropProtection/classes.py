import typing
from osgeo import ogr
from .distributions import *
from .types import *
from .functions import *

class Tank:
    """
    Implementation of the content of a tank.

    INPUTS
    Products: List of products within the tank. This describes a list of random variables for the products.
    """
    
    def __init__(self) -> None:
        self._products = None
        self._applicationRates = None

    @property
    def Products(self) -> Variable:
        return self._products

    @Products.setter
    def Products(self, value: Variable) -> None:
        self._products = value

    @property
    def ApplicationRates(self) -> Variable:
        return self._applicationRates

    @ApplicationRates.setter
    def ApplicationRates(self, value: Variable) -> None:
        self._applicationRates = value

    def sample_application_rates(self, day: int, field: int) -> typing.List[float]:

        # sample application rates:
        application_rates = []
        appl_rates = self._applicationRates.get((day, field), ("time/day, space/base_geometry"))
        for appl_rate in appl_rates:
            application_rates.append(appl_rate.get((day, field), ("time/day, space/base_geometry")))
        
        return application_rates

    def sample_tank(self, day: int, field: int) -> typing.Tuple[typing.List[str], typing.List[float]]:

        # sample tank:
        products = self._products.get((day, field), ("time/day, space/base_geometry"))
        application_rates = self.sample_application_rates(day, field)

        return products, application_rates

    # Returns the scale of products in the tank. Checks that the Product and Application Rate scales are the same
    def sample_application_type(self) -> str:
        if self._products.Scales != self._applicationRates.Scales:
            raise TypeError(f'Product and ApplicationRate scales must be the same. {self._products.Scales} and {self._applicationRates.Scales} is invalid.')
        return self._products.Scales

class Application:
    """
    Implementation of a single application.

    INPUTS
    Technology: Technology used for the application. This describes a random variable for the technology.
    ApplicationRate: Application rate of the application. This describes a random variable for the application rate.
    """

    def __init__(self) -> None:
        self._applicationWindow = None
        self._inCropBuffer = None
        self._inFieldMargin = None
        self._minimumAppliedArea = None
        self._tank = None
        self._technology = None

    @property
    def ApplicationWindow(self) -> Variable:
        return self._applicationWindow

    @ApplicationWindow.setter
    def ApplicationWindow(self, value: Variable) -> None:
        self._applicationWindow = value

    @property
    def InCropBuffer(self) -> Variable:
        return self._inCropBuffer

    @InCropBuffer.setter
    def InCropBuffer(self, value: Variable) -> None:
        self._inCropBuffer = value

    @property
    def InFieldMargin(self) -> Variable:
        return self._inFieldMargin

    @InFieldMargin.setter
    def InFieldMargin(self, value: Variable) -> None:
        self._inFieldMargin = value

    @property
    def MinimumAppliedArea(self) -> Variable:
        return self._minimumAppliedArea

    @MinimumAppliedArea.setter
    def MinimumAppliedArea(self, value: Variable) -> None:
        self._minimumAppliedArea = value

    @property
    def Tank(self) -> Tank:
        return self._tank

    @Tank.setter
    def Tank(self, value: Tank) -> None:
        self._tank = value

    @property
    def Technology(self) -> Variable:
        return self._technology

    @Technology.setter
    def Technology(self, value: Variable) -> None:
        self._technology = value

    def apply_today(self, day: int, field: int) -> bool:

        # check if day is first day of application window:
        appl_window = self._applicationWindow.get((day, field), ("time/day, space/base_geometry"))
        if day != appl_window.Start:
            return False
        return True

    def can_apply_on_geometry(self, day: int, field: int, field_geometry: bytes) -> bool:

        # get crop buffer, field margin and minimum applied area:
        in_crop_buffer = self._inCropBuffer.get((day, field), ("time/day, space/base_geometry"))
        in_field_margin = self._inFieldMargin.get((day, field), ("time/day, space/base_geometry"))
        min_applied_area = self._minimumAppliedArea

        # check area:
        applied_geometry = ogr.CreateGeometryFromWkb(field_geometry)
        if in_crop_buffer + in_field_margin > 0:
            applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
        if applied_geometry.GetArea() < min_applied_area:
            return False
        return True

    def sample_tank(self, day: int, field: int) -> typing.Tuple[typing.List[str], typing.List[float]]:
        return self._tank.sample_tank(day, field)
    
    def sample_application_type(self) -> str:
        return self._tank.sample_application_type()

    def sample_technology(self, day: int, field: int) -> str:
        return self._technology.get((day, field), ("time/day, space/base_geometry"))

    def sample_application_datetime(self, day: int, field: int) -> typing.Union[MonthDay, MonthDayTime]:
        appl_window = self._applicationWindow.get((day, field), ("time/day, space/base_geometry"))
        return appl_window.sample()

    def sample_application(self, day: int, field: int, field_geometry: bytes) -> typing.Tuple[typing.List[str], typing.List[float], str, float, bytes, str]:

        # sample products, technology, application rate and date/time:
        products, application_rates = self.sample_tank(day, field)
        application_type = self.sample_application_type()
        technology = self.sample_technology(day, field)
        application_datetime = self.sample_application_datetime(day, field)
        application_datetime = application_datetime.toordinal(datetime.date.fromordinal(day).year)

        # get applied geometry:
        in_crop_buffer = self._inCropBuffer.get((day, field), ("time/day, space/base_geometry"))
        in_field_margin = self._inFieldMargin.get((day, field), ("time/day, space/base_geometry"))
        applied_geometry = ogr.CreateGeometryFromWkb(field_geometry)
        if in_crop_buffer + in_field_margin > 0:
            applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
        applied_geometry = bytes(applied_geometry.ExportToWkb())

        return products, application_rates, technology, application_datetime, applied_geometry, application_type

class PPMCalendar:
    """
    Implementation of an application calendar. Here, the term `application calendar` refers to an application window, a tank content and any restrictions regarding applications.

    INPUTS
    TargetCrops: Target crops of the application calendar.
    ApplicationWindow: Application window of the application calendar. This describes a random variable for the application date.
    InCropBuffer: An in-crop buffer used during application. This describes a random variable for the in-crop buffer.
    InFieldMargin: An margin without crops within fields. This describes a random variable for the margin.
    MinimumAppliedArea: The minimum applied area considered. This describes a variable for the minimum applied area.
    Tank: Tank content of the application calendar.
    """

    def __init__(self) -> None:
        self._temporalValidity = None
        self._targetCrops = None
        self._targetFields = None
        self._indications = None
        self._minAppliedArea = None

    @property
    def TemporalValidity(self) -> Variable:
        return self._temporalValidity

    @TemporalValidity.setter
    def TemporalValidity(self, value: Variable) -> None:
        self._temporalValidity = value

    @property
    def TargetCrops(self) -> Variable:
        return self._targetCrops

    @TargetCrops.setter
    def TargetCrops(self, value: Variable) -> None:
        self._targetCrops = value

    @property
    def TargetFields(self) -> Variable:
        return self._targetFields

    @TargetFields.setter
    def TargetFields(self, value: Variable) -> None:
        self._targetFields = value

    @property
    def Indications(self) -> Variable:
        return self._indications

    @Indications.setter
    def Indications(self, value: Variable) -> None:
        self._indications = value

    @property
    def MinAppliedArea(self) -> Variable:
        return self._minAppliedArea

    @MinAppliedArea.setter
    def MinAppliedArea(self, value: Variable) -> None:
        self._minAppliedArea = value

    def is_valid(self, day: int, field: int) -> bool:

        # check if calendar is valid on day and field:
        temp_validity = self._temporalValidity.get((day, field), ("time/day, space/base_geometry"))
        if temp_validity == None or not temp_validity.is_within(day):
            return False
        return True

    def can_apply_on_crop(self, day: int, field: int, crop_id: int) -> bool:

        # check crop id:
        if self._targetCrops and crop_id not in self._targetCrops.get((day, field), ("time/day, space/base_geometry")):
            return False
        return True
    
    def can_apply_on_field(self, day: int, field: int, field_id: int) -> bool:

        # check field id
        if self._targetFields and field_id not in self._targetFields.get((day, field), ("time/day, space/base_geometry")):
            return False
        return True

    def sample_applications(self, day: int, field: int, field_geometry: bytes) -> typing.List[typing.Tuple[typing.List[str], typing.List[float], str, float, bytes]]:

        # loop through indications and sample applications:
        applications = []
        indications = self._indications.get((day, field), ("time/day, space/base_geometry"))
        for ind in indications:

            # get application sequence:
            appl_seq = ind.get((day, field), ("time/day, space/base_geometry"))

            # sample applications:
            for appl in appl_seq:
                # set each application's minimum applied area
                appl.MinimumAppliedArea = self.MinAppliedArea
                
                # check if application can/should be realized:
                if not appl.apply_today(day, field) or not appl.can_apply_on_geometry(day, field, field_geometry):
                    continue

                # sample application:
                prods, appl_rates, tech, appl_dt, appl_geom, appl_type = appl.sample_application(day, field, field_geometry)
                applications.append((prods, appl_rates, tech, appl_dt, appl_geom, appl_type))

        return applications

class Technology:
    """
    Describes a technology and its properties.

    INPUTS
    Technology: Name of technology.
    DriftReduction: The fraction by which spray-drift is reduced due to technological measures.
    """

    def __init__(self) -> None:
        self._technologyName = None
        self._driftReduction = None

    @property
    def TechnologyName(self) -> Variable:
        return self._technologyName

    @TechnologyName.setter
    def TechnologyName(self, value: Variable) -> None:
        self._technologyName = value

    @property
    def DriftReduction(self) -> Variable:
        return self._driftReduction

    @DriftReduction.setter
    def DriftReduction(self, value: Variable) -> None:
        self._driftReduction = value

    def initialize(self):
        self._driftReduction.initialize()

    def sample_drift_reduction(self, day: int, field: int) -> str:
        return self._driftReduction.get((day, field), ("time/day, space/base_geometry"))

