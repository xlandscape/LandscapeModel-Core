from asyncio import proactor_events
from multiprocessing.sharedctypes import Value
import random
import typing
import base
import attrib
import datetime
from osgeo import ogr
from .distributions import RandomVariable, Distribution
from .functions import *

class ApplicationWindowDistribution(Distribution):
    """
    Implementation of an application window.

    INPUTS
    ApplicationDateStart: First possible date.
    ApplicationDateEnd: Last possible date.
    ApplicationTimeStart: First possible time.
    ApplicationTimeEnd: Last possible time.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store],
        format: str
    ) -> None:
        super(ApplicationWindowDistribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "ApplicationDateStart",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationDateEnd",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationTimeStart",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationTimeEnd",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._format = format
        self._applicationDateStart = None
        self._applicationDateEnd = None
        self._applicationTimeStart = None
        self._applicationTimeEnd = None

    def initialize(self):
        self._applicationDateStart = self._inputs["ApplicationDateStart"].read().values
        self._applicationDateEnd = self._inputs["ApplicationDateEnd"].read().values
        self._applicationTimeStart = self._inputs["ApplicationTimeStart"].read().values
        self._applicationTimeEnd = self._inputs["ApplicationTimeEnd"].read().values

    def sample(self, current_year: int) -> float:

        if not self._applicationDateStart or not self._applicationDateEnd or not self._applicationTimeStart or not self._applicationTimeEnd:
            raise Exception("Parameters were not initialized!")

        # format values:
        if self._format == "YYYY-MM-DD":
            application_date_start = datetime.datetime.strptime(self._applicationDateStart, "%Y-%m-%d").date()
            application_date_end = datetime.datetime.strptime(self._applicationDateEnd, "%Y-%m-%d").date()
        elif self._format == "MM-DD":
            application_date_start = datetime.datetime.strptime(self._applicationDateStart, "%m-%d").date()
            application_date_start = application_date_start.replace(year = current_year)
            application_date_end = datetime.datetime.strptime(self._applicationDateEnd, "%m-%d").date()
            application_date_end = application_date_end.replace(year = current_year)
        else:
            raise ValueError("Incorrect format given!")
        application_time_start = datetime.datetime.strptime(self._applicationTimeStart, "%H:%M").time()
        application_time_end = datetime.datetime.strptime(self._applicationTimeEnd, "%H:%M").time()

        # sample date as int:
        start_day = application_date_start.toordinal()
        end_day = application_date_end.toordinal()
        date = random.randint(start_day, end_day)

        # sample time in seconds:
        start_seconds = application_time_start.hour * 60 * 60 + application_time_start.minute * 60 + application_time_start.second
        end_seconds = application_time_end.hour * 60 * 60 + application_time_end.minute * 60 + application_time_end.second
        time = random.randint(start_seconds, end_seconds)

        # convert seconds to days:
        time /= 60 * 60 * 24

        # add date and time to get exact application date:
        date_time = date + time
        return date_time

class Tank(base.Component):
    """
    Implementation of the content of a tank.

    INPUTS
    Products: List of products within the tank. This describes a list of random variables for the products.
    """
    
    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(Tank, self).__init__(name, default_observer, default_store)
        self._products = None

    @property
    def Products(self) -> typing.List[RandomVariable]:
        return self._products

    @Products.setter
    def Products(self, value: typing.List[RandomVariable]) -> None:
        self._products = value

    def initialize(self):
        for product in self._products:
            product.initialize()

    def sample_products(self, day: int, field: int) -> typing.List[str]:

        # sample from all random variables:
        products = []
        for product in self._products:
            time_index = convert_index(day, "time/day", product.get_scale("time"))
            products.append(product.get_realization((time_index, field)))
        return products

class PPMCalendar(base.Component):
    """
    Implementation of an application calendar. Here, the term `application calendar` refers to an application window, a tank content and any restrictions regarding applications.

    INPUTS
    TargetCrops: Target crops of the application calendar.
    ApplicationWindow: Application window of the application calendar. This describes a random variable for the application date.
    InCropBuffer: An in-crop buffer used during application. This describes a random variable for the in-crop buffer.
    InFieldMargin: An margin without crops within fields. This describes a random variable for the margin.
    MinimumAppliedArea: The minimum applied area considered. This describes a random variable for the minimum applied area.
    Tank: Tank content of the application calendar.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(PPMCalendar, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "TargetCrops",
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._targetCrops = None
        self._applicationWindow = None
        self._inCropBuffer = None
        self._inFieldMargin = None
        self._minimumAppliedArea = None
        self._tank = None
        self._fieldTimeIndices = set()

    @property
    def ApplicationWindow(self) -> RandomVariable:
        return self._applicationWindow

    @ApplicationWindow.setter
    def ApplicationWindow(self, value: RandomVariable) -> None:
        self._applicationWindow = value

    @property
    def InCropBuffer(self) -> RandomVariable:
        return self._inCropBuffer

    @InCropBuffer.setter
    def InCropBuffer(self, value: RandomVariable) -> None:
        self._inCropBuffer = value

    @property
    def InFieldMargin(self) -> RandomVariable:
        return self._inFieldMargin

    @InFieldMargin.setter
    def InFieldMargin(self, value: RandomVariable) -> None:
        self._inFieldMargin = value

    @property
    def MinimumAppliedArea(self) -> RandomVariable:
        return self._minimumAppliedArea

    @MinimumAppliedArea.setter
    def MinimumAppliedArea(self, value: RandomVariable) -> None:
        self._minimumAppliedArea = value

    @property
    def Tank(self) -> Tank:
        return self._tank

    @Tank.setter
    def Tank(self, value: Tank) -> None:
        self._tank = value

    def initialize(self):
        self._targetCrops = self._inputs["TargetCrops"].read().values
        self._applicationWindow.initialize()
        self._inCropBuffer.initialize()
        self._inFieldMargin.initialize()
        self._minimumAppliedArea.initialize()
        self._tank.initialize()

    def was_applied(self, day: int, field: int) -> bool:

        # check if ppm calendar was applied for field and time:
        time_index = convert_index(day, "time/day", self._applicationWindow.get_scale("time"))
        if (time_index, field) not in self._fieldTimeIndices:
            self._fieldTimeIndices.add((time_index, field))
            return False       
        return True

    def can_apply(self, day: int, field: int, applied_geometry: bytes, crop_id: int) -> bool:

        # check crop id:
        if not self._targetCrops:
            raise Exception("Parameters were not initialized!")
        if crop_id not in self._targetCrops:
            return False

        # get crop buffer, field margin and minimum applied area:
        time_index = convert_index(day, "time/day", self._inCropBuffer.get_scale("time"))
        in_crop_buffer = self._inCropBuffer.get_realization((time_index, field))
        time_index = convert_index(day, "time/day", self._inFieldMargin.get_scale("time"))
        in_field_margin = self._inFieldMargin.get_realization((time_index, field))
        time_index = convert_index(day, "time/day", self._minimumAppliedArea.get_scale("time"))
        min_applied_area = self._minimumAppliedArea.get_realization((time_index, field))

        # check area:
        applied_geometry = ogr.CreateGeometryFromWkb(applied_geometry)
        if in_crop_buffer + in_field_margin > 0:
            applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
        if applied_geometry.GetArea() < min_applied_area:
            return False
        return True

    def sample_first_application_date(self, day: int, field: int) -> int:

        # sample application date:
        time_index = convert_index(day, "time/day", self._applicationWindow.get_scale("time"))
        current_year = datetime.date.fromordinal(day).year
        return self._applicationWindow.get_realization((time_index, field), current_year = current_year)

    def sample_products(self, day: int, field: int) -> typing.List[str]:

        # sample from tank:
        return self._tank.sample_products(day, field)

class Application(base.Component):
    """
    Implementation of a single application.

    INPUTS
    Technology: Technology used for the application. This describes a random variable for the technology.
    ApplicationRate: Application rate of the application. This describes a random variable for the application rate.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(Application, self).__init__(name, default_observer, default_store)
        self._technology = None
        self._applicationRate = None

    @property
    def Technology(self) -> RandomVariable:
        return self._technology

    @Technology.setter
    def Technology(self, value: RandomVariable) -> None:
        self._technology = value

    @property
    def ApplicationRate(self) -> RandomVariable:
        return self._applicationRate

    @ApplicationRate.setter
    def ApplicationRate(self, value: RandomVariable) -> None:
        self._applicationRate = value

    def initialize(self):
        self._technology.initialize()
        self._applicationRate.initialize()

    def sample_technology(self, day: int, field: int) -> str:
        time_index = convert_index(day, "time/day", self._technology.get_scale("time"))
        return self._technology.get_realization((time_index, field))

    def sample_application_rate(self, day: int, field: int) -> float:
        time_index = convert_index(day, "time/day", self._applicationRate.get_scale("time"))
        return self._applicationRate.get_realization((time_index, field))

class PPP(base.Component):
    """
    Describes a product and the number of applications.

    INPUTS
    Product: Name of PPP.
    DaysBetweenApplications: Days between applications. Only relevant for multiple applications. This describes a random variable for the days between applications.
    Applications: List of applications.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(PPP, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Product",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._product = None
        self._daysBetweenApplications = None
        self._applications = None

    @property
    def Product(self) -> str:
        if not self._product:
            raise Exception("Parameters were not initialized!")
        return self._product

    @property
    def DaysBetweenApplications(self) -> RandomVariable:
        return self._daysBetweenApplications

    @DaysBetweenApplications.setter
    def DaysBetweenApplications(self, value: RandomVariable) -> None:
        self._daysBetweenApplications = value

    @property
    def Applications(self) -> typing.List[Application]:
        return self._applications

    @Applications.setter
    def Applications(self, value: typing.List[Application]) -> None:
        self._applications = value

    def initialize(self):
        self._product = self._inputs["Product"].read().values
        self._daysBetweenApplications.initialize()
        for appl in self._applications:
            appl.initialize()

    def sample_first_application_rate(self, day: int, field: int) -> float:
        if len(self._applications) == 0:
            raise Exception("No applications were given!")
        return self._applications[0].sample_application_rate(day, field)

    def sample_first_technology(self, day: int, field: int) -> str:
        if len(self._applications) == 0:
            raise Exception("No applications were given!")
        return self._applications[0].sample_technology(day, field)

    def sample_subsequent_application_dates(self, first_application_date: float, day: int, field: int) -> typing.List[float]:
        if len(self._applications) == 0:
            raise Exception("No applications were given!")
        subsequent_application_dates = []
        last_application_date = first_application_date
        for a in range(1, len(self._applications)):
            time_index = convert_index(day, "time/day", self._daysBetweenApplications.get_scale("time"))
            days_between_applications = self._daysBetweenApplications.get_realization((time_index, field))
            subsequent_application_dates.append(last_application_date + days_between_applications)
            day += days_between_applications
            last_application_date += days_between_applications
        return subsequent_application_dates

    def sample_subsequent_application_rates(self, day: int, field: int) -> typing.List[float]:
        if len(self._applications) == 0:
            raise Exception("No applications were given!")
        subsequent_application_rates = []
        for a in range(1, len(self._applications)):
            subsequent_application_rates.append(self._applications[a].sample_application_rate(day, field))
        return subsequent_application_rates
    
    def sample_subsequent_technologies(self, day: int, field: int) -> typing.List[str]:
        if len(self._applications) == 0:
            raise Exception("No applications were given!")
        subsequent_technologies = []
        for a in range(1, len(self._applications)):
            subsequent_technologies.append(self._applications[a].sample_technology(day, field))
        return subsequent_technologies

class XPPPContainer(base.Component):
    """
    Generic container for XPPP.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(XPPPContainer, self).__init__(name, default_observer, default_store)

    def append(self, value: typing.Any) -> None:
        raise NotImplementedError("append was not implemented for XPPPContainer")

class PPPContainer(XPPPContainer):
    """
    A container of PPPs.

    INPUTS
    PPPs: List of PPPs.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(PPPContainer, self).__init__(name, default_observer, default_store)
        self._ppps = []

    @property
    def PPPs(self) -> typing.List[PPP]:
        return self._ppps

    @PPPs.setter
    def PPPs(self, value: typing.List[PPP]) -> None:
        self._ppps = value

    def initialize(self):
        for ppp in self._ppps:
            ppp.initialize()

    def sample_first_application_rate(self, product: str, day: int, field: int) -> float:
        application_rate = None
        for ppp in self._ppps:
            if ppp.Product == product:
                application_rate = ppp.sample_first_application_rate(day, field)
        if not application_rate:
            raise Exception(f"PPP '{product}' was not found!")
        return application_rate

    def sample_first_technology(self, product: str, day: int, field: int) -> str:
        technology = None
        for ppp in self._ppps:
            if ppp.Product == product:
                technology = ppp.sample_first_technology(day, field)
        if not technology:
            raise Exception(f"PPP '{product}' was not found!")
        return technology

    def sample_subsequent_application_dates(self, product: str, first_application_date: float, day: int, field: int) -> typing.List[float]:
        subsequent_application_dates = None
        for ppp in self._ppps:
            if ppp.Product == product:
                subsequent_application_dates = ppp.sample_subsequent_application_dates(first_application_date, day, field)
        if subsequent_application_dates is None:
            raise Exception(f"PPP '{product}' was not found!")
        return subsequent_application_dates

    def sample_subsequent_application_rates(self, product: str, day: int, field: int) -> typing.List[float]:
        subsequent_application_rates = None
        for ppp in self._ppps:
            if ppp.Product == product:
                subsequent_application_rates = ppp.sample_subsequent_application_rates(day, field)
        if subsequent_application_rates is None:
            raise Exception(f"PPP '{product}' was not found!")
        return subsequent_application_rates
    
    def sample_subsequent_technologies(self, product: str, day: int, field: int) -> typing.List[str]:
        subsequent_technologies = None
        for ppp in self._ppps:
            if ppp.Product == product:
                subsequent_technologies = ppp.sample_subsequent_technologies(day, field)
        if subsequent_technologies is None:
            raise Exception(f"PPP '{product}' was not found!")
        return subsequent_technologies

    def append(self, ppp: PPP) -> None:
        self._ppps.append(ppp)

class Technology(base.Component):
    """
    Describes a technology and its properties.

    INPUTS
    Technology: Name of technology.
    DriftReduction: The fraction by which spray-drift is reduced due to technological measures.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(Technology, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Technology",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            )
        ])
        self._technology = None
        self._driftReduction = None

    @property
    def Technology(self) -> str:
        if not self._technology:
            raise Exception("Parameters were not initialized!")
        return self._technology

    @property
    def DriftReduction(self) -> RandomVariable:
        return self._driftReduction

    @DriftReduction.setter
    def DriftReduction(self, value: RandomVariable) -> None:
        self._driftReduction = value

    def initialize(self):
        self._technology = self._inputs["Technology"].read().values
        self._driftReduction.initialize()

    def sample_drift_reduction(self, day: int, field: int) -> str:
        time_index = convert_index(day, "time/day", self._driftReduction.get_scale("time"))
        return self._driftReduction.get_realization((time_index, field))

class TechnologyContainer(XPPPContainer):
    """
    A container of technologies.

    INPUTS
    Technologies: List of technologies.
    """

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(TechnologyContainer, self).__init__(name, default_observer, default_store)
        self._technologies = []

    @property
    def Technologies(self) -> typing.List[Technology]:
        return self._technologies

    @Technologies.setter
    def Technologies(self, value: base.typing.List[Technology]) -> None:
        self._technologies = value

    def initialize(self):
        for tech in self._technologies:
            tech.initialize()

    def sample_drift_reduction(self, technology: str, day: int, field: int) -> float:
        drift_reduction = None
        for tech in self._technologies:
            if tech.Technology == technology:
                drift_reduction = tech.sample_drift_reduction(day, field)
        if drift_reduction is None:
            raise Exception(f"Technology '{technology}' was not found!")
        return drift_reduction

    def append(self, technology: Technology) -> None:
        self._technologies.append(technology)
        