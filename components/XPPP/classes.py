from asyncio import proactor_events
from multiprocessing.sharedctypes import Value
import math
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
        self._inputs = base.InputContainer(self, [
            base.Input(
                "Products",
                (attrib.Class(list[str], 1), attrib.Unit(None, 1), attrib.Scales("other/products", 1)),
                self.default_observer
            )
        ])
        self._products = None
        self._applicationRates = None

    @property
    def ApplicationRates(self) -> typing.List[RandomVariable]:
        return self._applicationRates

    @ApplicationRates.setter
    def ApplicationRates(self, value: typing.List[RandomVariable]) -> None:
        self._applicationRates = value

    def initialize(self):
        self._products = self._inputs["Products"].read().values
        for appl_rate in self._applicationRates:
            appl_rate.initialize()

    def sample_application_rates(self, day: int, field: int) -> typing.List[float]:

        # sample application rates:
        application_rates = []
        for appl_rate in self._applicationRates:
            time_index = convert_index(day, "time/day", appl_rate.get_scale("time"))
            application_rates.append(appl_rate.get_realization((time_index, field)))
        return application_rates

    def sample_tank(self, day: int, field: int) -> typing.Tuple[typing.List[str], typing.List[float]]:

        # sample tank:
        products = self._products
        application_rates = self.sample_application_rates(day, field)

        return products, application_rates

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
        self._applicationWindow = None
        self._inCropBuffer = None
        self._inFieldMargin = None
        self._minimumAppliedArea = None
        self._tank = None
        self._technology = None
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

    @property
    def Technology(self) -> RandomVariable:
        return self._technology

    @Technology.setter
    def Technology(self, value: RandomVariable) -> None:
        self._technology = value

    def initialize(self):
        self._applicationWindow.initialize()
        self._inCropBuffer.initialize()
        self._inFieldMargin.initialize()
        self._minimumAppliedArea.initialize()
        self._tank.initialize()
        self._technology.initialize()

    def was_applied(self, day: int, field: int) -> bool:

        # check if application was realized for field and year:
        time_index = convert_index(day, "time/day", "time/year")
        if (time_index, field) not in self._fieldTimeIndices:
            return False       
        return True

    def can_apply(self, day: int, field: int, field_geometry: bytes) -> bool:

        # get crop buffer, field margin and minimum applied area:
        time_index = convert_index(day, "time/day", self._inCropBuffer.get_scale("time"))
        in_crop_buffer = self._inCropBuffer.get_realization((time_index, field))
        time_index = convert_index(day, "time/day", self._inFieldMargin.get_scale("time"))
        in_field_margin = self._inFieldMargin.get_realization((time_index, field))
        time_index = convert_index(day, "time/day", self._minimumAppliedArea.get_scale("time"))
        min_applied_area = self._minimumAppliedArea.get_realization((time_index, field))

        # check area:
        applied_geometry = ogr.CreateGeometryFromWkb(field_geometry)
        if in_crop_buffer + in_field_margin > 0:
            applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
        if applied_geometry.GetArea() < min_applied_area:
            return False
        return True

    def sample_tank(self, day: int, field: int) -> typing.Tuple[typing.List[str], typing.List[float]]:
        return self._tank.sample_tank(day, field)

    def sample_technology(self, day: int, field: int) -> str:
        time_index = convert_index(day, "time/day", self._technology.get_scale("time"))
        return self._technology.get_realization((time_index, field))

    def sample_application_datetime(self, day: int, field: int) -> float:
        time_index = convert_index(day, "time/day", self._applicationWindow.get_scale("time"))
        current_year = datetime.date.fromordinal(day).year
        return self._applicationWindow.get_realization((time_index, field), current_year = current_year)

    def sample_application(self, day: int, field: int, field_geometry: bytes, product_labels: "ProductLabelContainer") -> typing.Tuple[typing.List[str], typing.List[float], str, float, bytes]:

        # sample products, technology, application rate and date/time:
        products, application_rates = self.sample_tank(day, field)
        technology = self.sample_technology(day, field)
        application_datetime = self.sample_application_datetime(day, field)

        # get applied geometry:
        time_index = convert_index(day, "time/day", self._inCropBuffer.get_scale("time"))
        in_crop_buffer = self._inCropBuffer.get_realization((time_index, field))
        time_index = convert_index(day, "time/day", self._inFieldMargin.get_scale("time"))
        in_field_margin = self._inFieldMargin.get_realization((time_index, field))
        applied_geometry = ogr.CreateGeometryFromWkb(field_geometry)
        if in_crop_buffer + in_field_margin > 0:
            applied_geometry = applied_geometry.Buffer(-in_crop_buffer - in_field_margin)
        applied_geometry = bytes(applied_geometry.ExportToWkb())
    
        # remember application:
        time_index = convert_index(day, "time/day", "time/year")
        self._fieldTimeIndices.add((time_index, field))

        # check application with label restrictions:
        product_labels.check_application_time(day, field, products, application_datetime)
        product_labels.check_application_rates(day, field, products, application_rates)
        product_labels.check_in_crop_buffer(day, field, products, in_crop_buffer + in_field_margin)

        return products, application_rates, technology, application_datetime, applied_geometry

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
        self._applications = None

    @property
    def Applications(self) -> typing.List[Application]:
        return self._applications

    @Applications.setter
    def Applications(self, value: typing.List[Application]) -> None:
        self._applications = value

    def initialize(self):
        self._targetCrops = self._inputs["TargetCrops"].read().values
        for appl in self._applications:
            appl.initialize()

    def can_apply(self, crop_id: int) -> bool:

        # check crop id:
        if crop_id not in self._targetCrops:
            return False
        return True

    def sample_applications(self, day: int, field: int, field_geometry: bytes, product_labels: "ProductLabelContainer") -> typing.Tuple[typing.List[str], typing.List[float], typing.List[str], typing.List[float], typing.List[bytes]]:

        # sample applications
        products = []
        application_rates = []
        technologies = []
        application_datetimes = []
        applied_geometries = []
        for appl in self._applications:
            if appl.was_applied(day, field) or not appl.can_apply(day, field, field_geometry):
                continue
            prods, rates, tech, datetime, geom = appl.sample_application(day, field, field_geometry, product_labels)
            products.extend(prods)
            application_rates.extend(rates)
            technologies.extend([tech] * len(prods))
            application_datetimes.extend([datetime] * len(prods))
            applied_geometries.extend([geom] * len(prods))

        # check applications with label restrictions:
        product_labels.check_no_of_applications(field, products, application_datetimes)
        product_labels.check_days_between_applications(field, products, application_datetimes)

        return products, application_rates, technologies, application_datetimes, applied_geometries

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

    def __setitem__(self, key: str, value: typing.Any) -> None:
        raise NotImplementedError("append was not implemented for XPPPContainer")

class ProductLabel(base.Component):
    """
    Describes a product.

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
        super(ProductLabel, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "ApplicationTimeStart",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "ApplicationTimeEnd",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MaxNoOfApplications",
                (attrib.Class(int, 1), attrib.Unit("1", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MinInCropBuffer",
                (attrib.Class(float, 1), attrib.Unit("m", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MinDaysBetweenApplications",
                (attrib.Class(int, 1), attrib.Unit("d", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "MaxApplicationRate",
                (attrib.Class(float, 1), attrib.Unit("g/ha", 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
        ])
        self._applicationTimeStart = None
        self._applicationTimeEnd = None
        self._maxNoOfApplications = None
        self._minInCropBuffer = None
        self._minDaysBetweenApplications = None
        self._maxApplicationRate = None

    @property
    def Product(self) -> str:
        return self._product

    def initialize(self):
        self._applicationTimeStart = datetime.datetime.strptime(self._inputs["ApplicationTimeStart"].read().values, "%H:%M").time()
        self._applicationTimeStart = self._applicationTimeStart.hour / 24 + self._applicationTimeStart.minute / (24 * 60)
        self._applicationTimeEnd = datetime.datetime.strptime(self._inputs["ApplicationTimeEnd"].read().values, "%H:%M").time()
        self._applicationTimeEnd = self._applicationTimeEnd.hour / 24 + self._applicationTimeEnd.minute / (24 * 60)
        self._maxNoOfApplications = self._inputs["MaxNoOfApplications"].read().values
        self._minInCropBuffer = self._inputs["MinInCropBuffer"].read().values
        self._minDaysBetweenApplications = self._inputs["MinDaysBetweenApplications"].read().values
        self._maxApplicationRate = self._inputs["MaxApplicationRate"].read().values

    def application_rate_ok(self, day: int, field: int, application_rate: float) -> None:
        if application_rate > self._maxApplicationRate:
            return False
        return True

    def no_of_applications_ok(self, field: int, application_datetimes: typing.List[float]) -> None:
        if len(application_datetimes) > self._maxNoOfApplications:
            return False
        return True

    def days_between_applications_ok(self, field: int, application_datetimes: typing.List[float]) -> None:
        if len(application_datetimes) == 1:
            return
        min_days_between_applications = math.ceil(min([application_datetimes[i] - application_datetimes[i-1] for i in range(1, len(application_datetimes))]))
        if min_days_between_applications > self._minDaysBetweenApplications:
            return False
        return True

    def application_time_ok(self, day: int, field: int, application_datetime: float) -> None:
        application_time = application_datetime - int(application_datetime)
        if application_time < self._applicationTimeStart or application_time > self._applicationTimeEnd:
            return False
        return True

    def in_crop_buffer_ok(self, day: int, field: int, in_crop_buffer: float) -> None:
        if in_crop_buffer < self._minInCropBuffer:
            return False
        return True

class ProductLabelContainer(XPPPContainer):
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
        super(ProductLabelContainer, self).__init__(name, default_observer, default_store)
        self._productLabels = {}

    @property
    def ProductLabels(self) -> typing.Dict[str, ProductLabel]:
        return self._productLabels

    @ProductLabels.setter
    def ProductLabels(self, value: typing.Dict[str, ProductLabel]) -> None:
        self._productLabels = value

    def initialize(self):
        for label in self._productLabels.values():
            label.initialize()
        
    def check_application_rates(self, day: int, field: int, products: typing.List[str], application_rates: typing.List[float]) -> None:
        for idx, product in enumerate(products):
            if not self._productLabels[product].application_rate_ok(day, field, application_rates[idx]):
                self.default_observer.write_message(2, f"Max. application rate violated for product {product} on day {day} and field {field}!")

    def check_no_of_applications(self, field: int, products: typing.List[str], application_datetimes: typing.List[float]) -> None:
        unique_products = set(products)
        for product in unique_products:
            appl_datetimes = [application_datetimes[p] for p in range(len(products)) if product == products[p]]
            if not self._productLabels[product].no_of_applications_ok(field, appl_datetimes):
                self.default_observer.write_message(2, f"Max. number of applications violated for product {product} on field {field}!")

    def check_days_between_applications(self, field: int, products: typing.List[str], application_datetimes: typing.List[float]) -> None:
        unique_products = set(products)
        for product in unique_products:
            appl_datetimes = [application_datetimes[p] for p in range(len(products)) if product == products[p]]
            if not self._productLabels[product].days_between_applications_ok(field, appl_datetimes):
                self.default_observer.write_message(2, f"Min. days between applications violated for product {product} on field {field}!")

    def check_application_time(self, day: int, field: int, products: typing.List[str], application_datetime: float) -> None:
        for idx, product in enumerate(products):
            if not self._productLabels[product].application_time_ok(day, field, application_datetime):
                self.default_observer.write_message(2, f"Timing restrictions violated for product {product} on day {day} and field {field}!")

    def check_in_crop_buffer(self, day: int, field: int, products: typing.List[str], in_crop_buffer: float) -> None:
        for idx, product in enumerate(products):
            if not self._productLabels[product].in_crop_buffer_ok(day, field, in_crop_buffer):
                self.default_observer.write_message(2, f"Crop buffer restrictions violated for product {product} on day {day} and field {field}!")

    def __setitem__(self, key: str, product_label: ProductLabel) -> None:
        self._productLabels[key] = product_label

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
        self._driftReduction = None

    @property
    def DriftReduction(self) -> RandomVariable:
        return self._driftReduction

    @DriftReduction.setter
    def DriftReduction(self, value: RandomVariable) -> None:
        self._driftReduction = value

    def initialize(self):
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
        self._technologies = {}

    @property
    def Technologies(self) -> typing.Dict[str, Technology]:
        return self._technologies

    @Technologies.setter
    def Technologies(self, value: base.typing.Dict[str, Technology]) -> None:
        self._technologies = value

    def initialize(self):
        for tech in self._technologies.values():
            tech.initialize()

    def sample_drift_reductions(self, technologies: typing.List[str], day: int, field: int) -> typing.List[float]:
        drift_reductions = []
        for tech in technologies:
            drift_reductions.append(self._technologies[tech].sample_drift_reduction(day, field))
        return drift_reductions

    def __setitem__(self, key: str, technology: Technology) -> None:
        self._technologies[key] = technology
        