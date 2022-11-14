import datetime
import numpy as np
import random
import base
import attrib
import typing
import xml.etree.ElementTree
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
                "ParametrizationNamespace",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
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
        self._productLabelContainer = None
        self._technologyContainer = None

    @property
    def PPMCalendars(self) -> typing.List[PPMCalendar]:
        return self._ppmCalendars

    @PPMCalendars.setter
    def PPMCalendars(self, value: typing.List[PPMCalendar]) -> None:
        self._ppmCalendars = value

    @property
    def ProductLabels(self) -> ProductLabelContainer:
        return self._productLabelContainer

    @ProductLabels.setter
    def ProductLabels(self, value: ProductLabelContainer) -> None:
        self._productLabelContainer = value

    @property
    def Technologies(self) -> TechnologyContainer:
        return self._technologyContainer

    @Technologies.setter
    def Technologies(self, value: TechnologyContainer) -> None:
        self._technologyContainer = value

    def check_random_variable_scales(self, scales: str) -> None:

        # if scales were not implemented, raise exception:
        if scales not in self.RANDOM_VARIABLE_SCALES:
            raise NotImplementedError(f"XPPP was not implemented for random variable scale '{scales}'!")

    def set_input(self, object: base.Component, config: xml.etree.ElementTree, ids: typing.List[int]) -> None: 
        
        # get type:
        if "type" in config.attrib:
            type = config.attrib["type"]
        else:
            type = "str"

        # create output:
        value_config = copy.copy(config)
        if type == "param/int":
            value_config.attrib["type"] = "int"
        elif type == "param/float":
            value_config.attrib["type"] = "float"
        elif type == "param/str" or type == "param/date" or type == "param/time":
            del value_config.attrib["type"]
        value = base.convert(value_config)
        output = base.Output(f"XPPP/{config.tag.split('}')[1]}_{len(ids)}", self.default_store)
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
        object.inputs[config.tag.split("}")[1]] = output

    def set_random_input(self, object: RandomVariable, config: xml.etree.ElementTree, ids: typing.List[int]) -> None: 

        try:
            scales = config.attrib["scales"]
        except KeyError:
            raise KeyError("Scales have to be specified for all inputs!")
        self.check_random_variable_scales(scales)
        try:
            dist = config.attrib["dist"]
        except KeyError:
            raise KeyError("Distributions has to be specified for all inputs!")
        if dist == "normal":
            distribution = NormalDistribution("NormalDistribution", self.default_observer, self.default_store)
            self.read_inputs(distribution, config, ids)
        elif dist == "uniform":
            distribution = UniformDistribution("UniformDistribution", self.default_observer, self.default_store)
            self.read_inputs(distribution, config, ids)
        elif dist == "uniform_discrete":
            distribution = DiscreteUniformDistribution("DiscreteUniformDistribution", self.default_observer, self.default_store)
            self.read_inputs(distribution, config, ids)
        elif dist == "choice":
            distribution = ChoiceDistribution("ChoiceDistribution", self.default_observer, self.default_store)
            distribution.ChoiceList = []
            config = config[0]
            for item in config:
                choice = Choice("Choice", self.default_observer, self.default_store)
                for input in item:
                    if input.tag.split("}")[1] == "Probability":
                        self.set_input(choice, input, ids)                
                    elif input.tag.split("}")[1] == "ApplicationSequence":
                        appl_seq_list = []
                        self.read_inputs(appl_seq_list, input, ids)
                        appl_seq = ApplicationSequence("ApplicationSequence", self.default_observer, self.default_store)
                        appl_seq.Applications = appl_seq_list
                        choice.Object = appl_seq
                    elif input.tag.split("}")[1] == "Name":
                        param_str = input.text
                        choice.Object = param_str
                    else:
                        raise Exception(f"Invalid tag {input.tag} for choice-object!")
                distribution.ChoiceList.append(choice)
        elif dist == "application_window":
            try:
                format = config.attrib["format"]
            except KeyError:
                raise KeyError("Date format hast to be specified for application windows!")
            distribution = ApplicationWindowDistribution("ApplicationWindowDistribution", self.default_observer, self.default_store, format)
            self.read_inputs(distribution, config, ids)
        else:
            raise Exception("Invalid distribution!")
        object.Scales = scales
        object.Distribution = distribution
        
    def read_inputs(self, parent_object: typing.Any, root: xml.etree.ElementTree, ids: typing.List[int]) -> None:

        # loop over all child nodes:
        for child in root:

            # get type:
            if "type" in child.attrib:
                child_type = child.attrib["type"]
            else:
                child_type = "str"

            # go through all cases:
            if child_type == "class" or child_type == "param/class":
                child_object = globals()[child.tag.split("}")[1]](child.tag, self.default_observer, self.default_store)
                self.read_inputs(child_object, child, ids)
            elif child_type == "list[class]" or child_type == "param/list":
                child_object = []
                self.read_inputs(child_object, child, ids)
            elif child_type == "dict[class]":
                child_object = {}
                self.read_inputs(child_object, child, ids)
            elif child_type == "random":
                child_object = RandomVariable()
                self.set_random_input(child_object, child, ids)
            else:
                self.set_input(parent_object, child, ids)
                continue

            # if this point is reached, child is an object and has to be set manually:
            if isinstance(parent_object, list): 
                parent_object.append(child_object)
            elif isinstance(parent_object, dict) or isinstance(parent_object, ProductLabelContainer) or isinstance(parent_object, TechnologyContainer):                
                parent_object[child.attrib["id"]] = child_object
            else:
                setattr(parent_object, child.tag.split("}")[1], child_object)

    def read_xml(self) -> None:
  
        # start reading xml:
        xml_file = self.inputs["XPPPFilePath"].read().values
        xml_tree = xml.etree.ElementTree.parse(xml_file)
        root = xml_tree.getroot()
        namespace = {"": self.inputs["ParametrizationNamespace"].read().values}

        # create lists and containers:
        self.PPMCalendars = []
        self.ProductLabels = ProductLabelContainer("ProductLabelContainer", self.default_observer, self.default_store)
        self.Technologies = TechnologyContainer("TechnologyContainer", self.default_observer, self.default_store)

        # read lists and containers:
        ids = []
        self.read_inputs(self.PPMCalendars, root.find("PPMCalendars", namespace), ids)
        self.read_inputs(self.ProductLabels, root.find("ProductLabels", namespace), ids)
        self.read_inputs(self.Technologies, root.find("Technologies", namespace), ids)

        # initialize:
        for ppm_cal in self.PPMCalendars:
            ppm_cal.initialize()
        self.ProductLabels.initialize()
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
        field_geometries = self.inputs["FieldGeometries"].read().values

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

                    # check area:
                    if not ppm_calendar.can_apply(crop_ids[field]):
                        continue

                    # sample applications:
                    products, rates, technologies, datetimes, geometries = ppm_calendar.sample_applications(day, field, field_geometries[field], self.ProductLabels)

                    # sample drift reductions:
                    drift_reductions = self.Technologies.sample_drift_reductions(technologies, day, field)

                    # add to results:
                    applied_areas.extend(geometries)
                    applied_fields.extend([field] * len(geometries))
                    application_dates.extend(datetimes)
                    application_rates.extend(rates)
                    technology_drift_reductions.extend(drift_reductions)
                    applied_ppp.extend(products)           

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