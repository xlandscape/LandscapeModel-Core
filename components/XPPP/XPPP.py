from weakref import KeyedRef
from osgeo import ogr
import datetime
import numpy as np
import random
import base
import components
import attrib
import typing
import xml.etree.ElementTree
import queue
import importlib
import copy
from .distributions import *
from .classes import *

class XPPP(base.Component):
    """
    XPPP is a Landscape Model component for simulating applications of plant protection products on fields with a given 
    landscape. The simulation is done on a daily-fieldwise resolution. On each day and field in the simulation, the 
    module checks if there are products to apply. If so, exact application dates, rates etc. are sampled from the 
    distributions given by the user. To be more specific, the user parameterizes random variables that are realized 
    during the simulation according to their scales.  
    XPPP currently supports the input scales `global` and `time/day, space/base_geometry`.  
    XPPP currently supports the random variable scales `global`, `time/day`, `time/year`, `time/day, space/base_geometry` and `time/year, space/base_geometry`.
    """

    # RELEASES
    VERSION = base.VersionCollection(
        base.VersionInfo("1.0.0", None),
    )
    
    # CHANGELOG
    VERSION.added("1.0.0", "First release of `XPPP` ")

    SCALES = ("global", "time/day, space/base_geometry")
    RANDOM_VARIABLE_SCALES = ("global", "time/day", "time/year", "time/day, space/base_geometry", "time/year, space/base_geometry")

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(XPPP, self).__init__(name, default_observer, default_store)
        self._module = base.Module("XPPP", "1.0", r"module\README.md") 
        self._inputs = base.InputContainer(self, [
            base.Input(
                "XPPPFilePath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The path to the XML-parametrization of XPPP. A `str` of global scale. Value has no unit."""
            ),
            base.Input(
                "SimulationStart",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The first day of the simulation. A `datetime.date` of global scale. Value has no unit."""
            ),
            base.Input(
                "SimulationEnd",
                (attrib.Class(datetime.date, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The last day of the simulation. A `datetime.date` of global scale. Value has no unit."""
            ),
            base.Input(
                "RandomSeed",
                (attrib.Class(int, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""A initialization for the random number generator. An int of global scale. Value has a unit of 1."""
            ),
            base.Input(
                "Fields",
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer,
                description="""A list of identifiers of individual geometries. A list[int] of scale space/base_geometry. Values have no
                    unit."""
            ),
            base.Input(
                "LandUseLandCoverTypes",
                (attrib.Class(list[int], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)), 
                self.default_observer,
                description="""The land-use and land-cover type of spatial units. A list[int] of scale space/base_geometry.
                    Values have no unit."""
            ),
            base.Input(
                "FieldGeometries",
                (attrib.Class(list[bytes], 1), attrib.Unit(None, 1), attrib.Scales("space/base_geometry", 1)),
                self.default_observer,
                description="""The geometries of individual landscape parts. A list[bytes] of scale space/base_geometry. Values
                    have no unit."""
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("AppliedFields", default_store, self, 
                description="Indices of applied fields. A numpy-array of scale other/application."),
            base.Output("ApplicationDates", default_store, self,
                description="Application dates. A numpy-array of scale other/application."),
            base.Output("ApplicationRates", default_store, self, 
                description="Application rates. A numpy-array of scale other/application."),
            base.Output("TechnologyDriftReductions", default_store, self, 
                description="Drift reductions. A numpy-array of scale other/application."),
            base.Output("AppliedAreas", default_store, self, 
                description="Applied geometries. A list[bytes] of scale other/application."),
            base.Output("AppliedPPP", default_store, self, 
                description="Applied products. A list[str] of scale other/application.")
        ])
        self._ppmCalendars = None
        self._pppContainer = None
        self._technologyContainer = None

    @property
    def PPMCalendars(self) -> typing.List[PPMCalendar]:
        return self._ppmCalendars

    @PPMCalendars.setter
    def PPMCalendars(self, value: typing.List[PPMCalendar]) -> None:
        self._ppmCalendars = value

    @property
    def PPPs(self) -> PPPContainer:
        return self._pppContainer

    @PPPs.setter
    def PPPs(self, value: PPPContainer) -> None:
        self._pppContainer = value

    @property
    def Technologies(self) -> TechnologyContainer:
        return self._technologyContainer

    @Technologies.setter
    def Technologies(self, value: TechnologyContainer) -> None:
        self._technologyContainer = value

    def check_scales(self, scales: str) -> None:

        # if scales were not implemented, raise exception:
        if scales not in self.SCALES:
            raise NotImplementedError(f"XPPP was not implemented for input scale '{scales}'!")

    def check_random_variable_scales(self, scales: str) -> None:

        # if scales were not implemented, raise exception:
        if scales not in self.RANDOM_VARIABLE_SCALES:
            raise NotImplementedError(f"XPPP was not implemented for random variable scale '{scales}'!")

    def set_input(self, component: base.Component, config: xml.etree.ElementTree, ids: typing.List[int]) -> None: 
        
        # get type:
        try:
            type = config.attrib["type"]
        except KeyError:
            raise KeyError("Type has to be specified for all inputs!")

        # check scales:
        try:
            self.check_scales(config.attrib["scales"])
        except KeyError:
            raise KeyError("Scales have to specified for all inputs!")

        # create output:
        value_config = copy.copy(config)
        if type == "param/int":
            value_config.attrib["type"] = "int"
        elif type == "param/float":
            value_config.attrib["type"] = "float"
        elif type == "str" or type == "param/str" or type == "param/date" or type == "param/time":
            del value_config.attrib["type"]
        value = base.convert(value_config)
        output = base.Output(f"XPPP/{config.tag}_{len(ids)}", self.default_store)
        ids.append(len(ids))
        try: 
            output.set_values(
                value, 
                scales = config.attrib["scales"],
                unit = config.attrib["unit"] if "unit" in config.attrib else None
            )
        except KeyError:
            raise KeyError("Scales have to be specified for input values!")

        # set input:
        component.inputs[config.tag] = output

        # # create provider:
        # provider = base.DataProvider(output)

        # # get input attributes:
        # input_scales = attrib.Scales(config.attrib["scales"], 1) 
        # input_unit = attrib.Unit(config.attrib["unit"] if "unit" in config.attrib else None, 1)
        # if type == "int" or type == "param/int":
        #     input_type = attrib.Class(int, 1)
        # elif type == "float" or type == "param/float":
        #     input_type = attrib.Class(float, 1)
        # elif type == "str" or type == "param/str":
        #     input_type = attrib.Class(str, 1)
        # elif type == "list[int]":
        #     input_type = attrib.Class(list[int], 1)
        # elif type == "list[float]":
        #     input_type = attrib.Class(list[float], 1)
        # elif type == "list[str]":
        #     input_type = attrib.Class(list[str], 1)
        # elif type == "param/date":
        #     input_type = attrib.Class(str, 1)
        # elif type == "param/time":
        #     input_type = attrib.Class(str, 1)
        # input = base.Input(
        #         config.tag,
        #         (input_type, input_unit, input_scales),
        #         self.default_observer
        #     )

        # # set provider:
        # input.provider = provider
        # return input

    def read_inputs(self, parent_object: typing.Any, root: xml.etree.ElementTree, ids: typing.List[int]) -> None:

        # loop over all child nodes:
        for child in root:

            # get type:
            try:
                child_type = child.attrib["type"]
            except KeyError:
                raise KeyError("Type has to be specified for all inputs!")

            # go through all cases:
            if child_type == "class" or child_type == "param/class":
                child_object = globals()[child.tag](child.tag, self.default_observer, self.default_store)
                self.read_inputs(child_object, child, ids)
            elif child_type == "list[class]" or child_type == "param/list":
                child_object = []
                self.read_inputs(child_object, child, ids)
            elif child_type == "random":
                child_object = RandomVariable() 
                try:
                    scales = child.attrib["scales"]
                except KeyError:
                    raise KeyError("Scales have to be specified for all inputs!")
                self.check_random_variable_scales(scales)
                try:
                    dist = child.attrib["dist"]
                except KeyError:
                    raise KeyError("Distributions has to be specified for all inputs!")
                if dist == "normal":
                    distribution = NormalDistribution("NormalDistribution", self.default_observer, self.default_store)
                if dist == "uniform":
                    distribution = UniformDistribution("UniformDistribution", self.default_observer, self.default_store)
                if dist == "uniform_discrete":
                    distribution = DiscreteUniformDistribution("DiscreteUniformDistribution", self.default_observer, self.default_store)
                if dist == "choice":
                    distribution = ChoiceDistribution("ChoiceDistribution", self.default_observer, self.default_store)
                if dist == "application_window":
                    try:
                        format = child.attrib["format"]
                    except KeyError:
                        raise KeyError("Date format hast to be specified for application windows!")
                    distribution = ApplicationWindowDistribution("ApplicationWindowDistribution", self.default_observer, self.default_store, format)
                self.read_inputs(distribution, child, ids)
                child_object.Scales = scales
                child_object.Distribution = distribution
            else:
                self.set_input(parent_object, child, ids)
                continue

            # if this point is reached, child is an object and has to be set manually:
            if isinstance(parent_object, list) or isinstance(parent_object, XPPPContainer):
                parent_object.append(child_object)
            else:
                setattr(parent_object, child.tag, child_object)

    def read_xml(self) -> None:
  
        # start reading xml:
        xml_file = self.inputs["XPPPFilePath"].read().values
        xml_tree = xml.etree.ElementTree.parse(xml_file)
        root = xml_tree.getroot()

        # create lists and containers:
        self.PPMCalendars = []
        self.PPPs = PPPContainer("PPPContainer", self.default_observer, self.default_store)
        self.Technologies = TechnologyContainer("TechnologyContainer", self.default_observer, self.default_store)

        # read lists and containers:
        ids = []
        self.read_inputs(self.PPMCalendars, root.find("PPMCalendars"), ids)
        self.read_inputs(self.PPPs, root.find("PPPs"), ids)
        self.read_inputs(self.Technologies, root.find("Technologies"), ids)

        # initialize:
        for ppm_cal in self.PPMCalendars:
            ppm_cal.initialize()
        self.PPPs.initialize()
        self.Technologies.initialize()

    def run(self):

        # read xml
        self.read_xml()

        # set random seed
        random_seed = self.inputs["RandomSeed"].read().values
        if random_seed is not None and random_seed != 0:
            random.seed(random_seed)

        # set simulation start and end
        sim_start = self.inputs["SimulationStart"].read().values.toordinal()
        sim_end = self.inputs["SimulationEnd"].read().values.toordinal()

        # define results:
        applied_areas = []
        applied_fields = []
        application_dates = []
        application_rates = []
        technology_drift_reductions = []
        applied_ppp = []

        # read fields, crop ids and geometries:
        fields = self.inputs["Fields"].read().values
        crop_ids = self.inputs["LandUseLandCoverTypes"].read().values
        applied_geometry = self.inputs["FieldGeometries"].read().values

        self.default_observer.write_message(5, f"Simulation started.")
        
        # loop over each each day
        for day in range(sim_start, sim_end + 1):
            
            if (day - sim_start) % 50 == 0:
                current_date = datetime.date.fromordinal(day).strftime("%Y-%m-%d")
                self.default_observer.write_message(5, f"Simulation running for date: {current_date} (day {day - sim_start})")

            # loop over each field
            for field in range(len(fields)):
                
                # loop over each ppm calendar:
                for ppm_calendar in self.PPMCalendars:

                    # check if ppmcalendar was already applied:
                    if ppm_calendar.was_applied(day, field):
                        continue

                    # check area:
                    if not ppm_calendar.can_apply(day, field, applied_geometry[field], crop_ids[field]):
                        continue

                    # sample application date and products:
                    application_date = ppm_calendar.sample_first_application_date(day, field)
                    products = ppm_calendar.sample_products(day, field)
            
                    # loop over each product:
                    for product in products:

                        # sample application rate and technology:
                        application_rate = self.PPPs.sample_first_application_rate(product, day, field)
                        technology = self.PPPs.sample_first_technology(product, day, field)

                        # sample drift reduction:
                        drift_reduction = self.Technologies.sample_drift_reduction(technology, day, field)

                        # add to results:
                        applied_areas.append(applied_geometry[field])
                        applied_fields.append(field)
                        application_dates.append(int(application_date)) # use dates
                        application_rates.append(application_rate)
                        technology_drift_reductions.append(drift_reduction)
                        applied_ppp.append(product)

                        # get subsequent application windows, application rates and technologies:
                        subsequent_application_dates = self.PPPs.sample_subsequent_application_dates(product, application_date, day, field)
                        subsequent_application_rates = self.PPPs.sample_subsequent_application_rates(product, day, field)
                        subsequent_technologys = self.PPPs.sample_subsequent_technologies(product, day, field)

                        # loop over each subsequent application window:
                        for s, sub_appl_date in enumerate(subsequent_application_dates):

                            # sample drift reduction:
                            drift_reduction = self.Technologies.sample_drift_reduction(subsequent_technologys[s], day, field)

                            # add to results:
                            applied_areas.append(applied_geometry[field])
                            applied_fields.append(field)
                            application_dates.append(int(sub_appl_date)) # use dates
                            application_rates.append(subsequent_application_rates[s])
                            technology_drift_reductions.append(drift_reduction)
                            applied_ppp.append(product)

        self.default_observer.write_message(5, f"Simulation finished!")

        # convert results to numpy:
        applied_fields = np.array(applied_fields, dtype=np.int)
        application_dates = np.array(application_dates, dtype=int)
        application_rates = np.array(application_rates)
        technology_drift_reductions = np.array(technology_drift_reductions)

        # set outputs:
        self.outputs["AppliedFields"].set_values(applied_fields, scales="other/application")
        self.outputs["ApplicationDates"].set_values(application_dates, scales="other/application")
        self.outputs["ApplicationRates"].set_values(application_rates, scales="other/application")
        self.outputs["TechnologyDriftReductions"].set_values(technology_drift_reductions, scales="other/application")
        self.outputs["AppliedAreas"].set_values(applied_areas, scales="other/application")
        self.outputs["AppliedPPP"].set_values(applied_ppp, scales="other/application")