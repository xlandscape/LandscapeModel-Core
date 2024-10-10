import datetime
import numpy as np
import random
import os
import base
import attrib
import typing
import xml.etree.ElementTree
from .products import *
from .distributions import *
from .classes import *
from .types import *
from .parser import *

class xCropProtection(base.Component):
    """
    xCropProtection is a Landscape Model component for simulating applications of plant protection products on fields 
    with a given landscape. The simulation is done on a daily-fieldwise resolution. On each day and field in the 
    during the given simulation period, the module checks if there are applications of plant protection products 
    should be conducted. If so, exact application dates and rates are determined. The user has the option to use
    deterministic values or sample from a random distribution. 

    xCropProtection currently supports the input scales `global` and `time/day, space/base_geometry`.  
    xCropProtection currently supports the random variable scales `global`, `time/day`, `time/year`, `time/day, space/base_geometry` and `time/year, space/base_geometry`.
    """

    # RELEASES
    VERSION = base.VersionCollection(
        base.VersionInfo("1.0.0", None),
    )
    
    # CHANGELOG
    base.VERSION.added("1.16.5", "xCropProtection component")
    base.VERSION.changed("1.16.5", "Bound xCropProtection version to core version")
    VERSION.added("1.0.0", "First release of `xCropProtection`")

    RANDOM_TYPES = ("xCropProtection.NormalDistribution", "xCropProtection.UniformDistribution", "xCropProtection.DiscreteUniformDistribution", "xCropProtection.ChoiceDistribution")
    TIME_SPAN_TYPES = ("xCropProtection.TimeSpan", "xCropProtection.MonthDaySpan", "xCropProtection.MonthDayTimeSpan", "xCropProtection.DateSpan")
    LIST_TIME_SPAN_TYPES = ("list[xCropProtection.TimeSpan]", "list[xCropProtection.MonthDaySpan]", "list[xCropProtection.MonthDayTimeSpan]", "list[xCropProtection.DateSpan]")
    RANDOM_VARIABLE_SCALES = ("global", "time/day", "time/year", "time/day, space/base_geometry", "time/year, space/base_geometry")

    def __init__(self, 
        name: str, 
        default_observer: base.Observer, 
        default_store: typing.Optional[base.Store]
    ) -> None:
        super(xCropProtection, self).__init__(name, default_observer, default_store)
        self._module = base.Module("xCropProtection", "1.0", r"module\README.md", None, None) 
        self._inputs = base.InputContainer(self, [
            base.Input(
                "ParametrizationNamespace",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
            base.Input(
                "xCropProtectionFilePath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The path to the XML-parametrization of xCropProtection. A `str` of global scale. Value has no unit."""
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
                "OutputApplicationType",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The output type of the simulation: either product or active substance."""
            ),
            base.Input(
                "ProductDatabase",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""Path to the database containing product-active substance relationships."""
            ),
            base.Input(
                "MinimumAppliedArea",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""If a field's area is smaller than this value after applying the InCropBuffer and InFieldMargin values, no application will occur."""
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
            ),
            base.Input(
                "XMLPath",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer,
                description="""The path to the folder containing the XML file automatically generated if the input file type 
                    is Excel. This value is not set by the user and defaults to the run\SimID directory."""
            )
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("ApplicationDates", default_store, self,
                description="Application dates. A numpy-array of scale other/application."),
            base.Output("ApplicationRates", default_store, self, 
                description="Application rates. A numpy-array of scale other/application."),
            base.Output("AppliedPPP", default_store, self, 
                description="Applied products/substances. A list[str] of scale other/application."),
            base.Output("AppliedAreas", default_store, self, 
                description="Applied geometries. A list[bytes] of scale other/application."),
            base.Output("AppliedFields", default_store, self, 
                description="Applied fields. A numpy-array of scale other/application."),
            base.Output("TechnologyDriftReductions", default_store, self, 
                description="Drift reductions. A numpy-array of scale other/application.")
        ])
        self._ppmCalendars = None
        self._technologies = None

    @property
    def PPMCalendars(self) -> typing.List[PPMCalendar]:
        return self._ppmCalendars

    @PPMCalendars.setter
    def PPMCalendars(self, value: typing.List[PPMCalendar]) -> None:
        self._ppmCalendars = value

    @property
    def Technologies(self) -> typing.List[Technology]:
        return self._technologies

    @Technologies.setter
    def Technologies(self, value: typing.List[Technology]) -> None:
        self._technologies = value

    def check_random_variable_scales(self, scales: str) -> None:

        # if scales were not implemented, raise exception:
        if scales not in self.RANDOM_VARIABLE_SCALES:
            raise NotImplementedError(f"xCropProtection was not implemented for random variable scale '{scales}'!")

    def convert(self, config: xml.etree.ElementTree) -> typing.Any: 
        
        # set unit and scales:
        unit = None
        if "unit" in config.attrib:
            unit = config.attrib["unit"]
        scales = None
        if "scales" in config.attrib and (config.attrib["scales"] != "other/products" or config.attrib["scales"] != "other/active_substances"):
            scales = config.attrib["scales"]

        # get type:
        type = None
        if "type" in config.attrib:
            type = config.attrib["type"]

        if type not in self.RANDOM_TYPES: 

            # get starting indices (only relevant on time scales):
            sim_start_date = self.inputs["SimulationStart"].read().values
            index_start = 0
            if scales == "time/day":
                index_start = sim_start_date.toordinal()
            elif scales == "time/year":
                index_start = sim_start_date.year
            
            # get value (convert to dict):
            if type in self.TIME_SPAN_TYPES:
                del config.attrib["type"]
            elif type in self.LIST_TIME_SPAN_TYPES:
                config.attrib["type"] = "list[str]"
            raw_value = base.convert(config)
            values = {}
            if not isinstance(raw_value, list) or scales == None or scales == "global" or (scales == "other/products" or scales == "other/active_substances"):
                values[(index_start,)] = raw_value
            elif isinstance(raw_value, list):
                for i in range(len(raw_value)):
                    values[(index_start + i,)] = raw_value[i]
            else:
                raise NotImplementedError(f"Combination of scales {scales} and type {type} not implemented!")                

            # format values if necessary:
            if type == "xCropProtection.TimeSpan" or type == "list[xCropProtection.TimeSpan]":
                for key, value in values.items():
                    if value == "":
                        values[key] == None
                    else:
                        dates = value.split(" to ")
                        dates = (datetime.datetime.strptime(dates[0], "%H:%M"), datetime.datetime.strptime(dates[1], "%H:%M"))
                        values[key] = TimeSpan(Time(dates[0].hour, dates[0].minute), Time(dates[1].hour, dates[1].minute))
            elif type == "xCropProtection.MonthDaySpan" or type == "list[xCropProtection.MonthDaySpan]":
                for key, value in values.items():
                    if value == "":
                        values[key] == None
                    else:
                        dates = value.split(" to ")
                        dates = (datetime.datetime.strptime(dates[0], "%m-%d"), datetime.datetime.strptime(dates[1], "%m-%d"))
                        values[key] = MonthDaySpan(MonthDay(dates[0].month, dates[0].day), MonthDay(dates[1].month, dates[1].day))
            elif type == "xCropProtection.MonthDayTimeSpan" or type == "list[xCropProtection.MonthDayTimeSpan]":
                for key, value in values.items():
                    if value == "":
                        values[key] == None
                    else:
                        dates = value.split(" to ")
                        dates = (datetime.datetime.strptime(dates[0], "%m-%d %H:%M"), datetime.datetime.strptime(dates[1], "%m-%d %H:%M"))
                        values[key] = MonthDayTimeSpan(MonthDayTime(dates[0].month, dates[0].day, dates[0].hour, dates[0].minute), MonthDayTime(dates[1].month, dates[1].day, dates[1].hour, dates[1].minute))
            elif type == "xCropProtection.DateSpan" or type == "list[xCropProtection.DateSpan]":
                for key, value in values.items():
                    if value == "":
                        values[key] == None
                    else:
                        dates = value.split(" to ")
                        dates = (datetime.datetime.strptime(dates[0], "%Y-%m-%d"), datetime.datetime.strptime(dates[1], "%Y-%m-%d"))
                        values[key] = DateSpan(Date(dates[0].year, dates[0].month, dates[0].day), Date(dates[1].year, dates[1].month, dates[1].day))

            # get type for variable:
            if not type:
                type = "str"
            if "list" in type:
                type = type[5:-1]

            # return constant:
            return ConstantVariable(unit, scales, type, values)
        
        else:

            # create distribution and read inputs:
            if type == "xCropProtection.NormalDistribution":
                distribution = NormalDistribution()
                self.set_inputs(distribution, config)
            elif type == "xCropProtection.UniformDistribution":
                distribution = UniformDistribution()
                self.set_inputs(distribution, config)
            elif type == "xCropProtection.DiscreteUniformDistribution":
                distribution = DiscreteUniformDistribution()
                self.set_inputs(distribution, config)
            elif type == "xCropProtection.ChoiceDistribution":
                distribution = ChoiceDistribution()
                distribution.ChoiceList = []
                for child_config in config:
                    choice = Choice()
                    choice.Probability = float(child_config.attrib["probability"])
                    if "type" in child_config.attrib: # child describes random or some simple type
                        if child_config.attrib["type"] == "random":
                            child_object = self.convert(child_config)
                        else:
                            child_object = self.convert(child_config)
                    elif len(list(child_config)) == 0: # child describes string
                        child_object = self.convert(child_config)
                    elif child_config.tag.split("}")[1] in globals(): # child describes object
                        child_object = globals()[child_config.tag.split("}")[1]]()
                        self.set_inputs(child_object, child_config)
                    else: # child describes list
                        child_object = []
                        self.set_inputs(child_object, child_config)
                    choice.Object = child_object
                    distribution.ChoiceList.append(choice)

            # return random variable:
            return RandomVariable(unit, scales, type, distribution)

    def set_inputs(self, parent_object: typing.Any, root: xml.etree.ElementTree) -> None:

        # loop over all child nodes:
        for child_config in root:

            # get child object:
            if "type" in child_config.attrib: # child describes random or some simple type
                if child_config.attrib["type"] == "random":
                    child_object = self.convert(child_config)
                else:
                    child_object = self.convert(child_config)
            elif len(list(child_config)) == 0: # child describes string
                child_object = self.convert(child_config)
            elif child_config.tag.split("}")[1] in globals(): # child describes object
                child_object = globals()[child_config.tag.split("}")[1]]()
                self.set_inputs(child_object, child_config)
            else: # child describes list of objects (handled as constant variables)
                child_object_scale = "global"
                if str(child_config.tag).endswith("ApplicationRates") and "scales" in child_config.attrib:
                    child_object_scale = child_config.attrib["scales"]

                child_object = []
                self.set_inputs(child_object, child_config)
                child_object = ConstantVariable(None, child_object_scale, None, {(0,): child_object})

            # assign child object to parent object:
            if isinstance(parent_object, list): 
                parent_object.append(child_object)
            else:
                setattr(parent_object, child_config.tag.split("}")[1], child_object)
        
    def convert_types(self) -> None:

        # convert TemporalValidity if needed:
        for ppm_calendar in self.PPMCalendars:
            if ppm_calendar.TemporalValidity.Type == "str":
                for key, value in ppm_calendar.TemporalValidity.Value.items():
                    if value == "always":
                        ppm_calendar.TemporalValidity.Value[key] = DateSpan(Date(1, 1, 1), Date(9999, 12, 31))

    def set_min_applied_area(self) -> None:
        try:
            min_app_area = float(self.inputs["MinimumAppliedArea"].read().values)
        except:
            raise TypeError(f"The MinimumAppliedArea value provided is not numeric.")
        
        if min_app_area < 0:
            self.default_observer.write_message(2, f"Negative MinimumAppliedArea values are not allowed. The value has been set to 0.")
            min_app_area = 0

        # Set each calendar's minimum applied area
        for ppm_calendar in self.PPMCalendars:
            ppm_calendar.MinAppliedArea = min_app_area
            

    def replace_includes(self, root: xml.etree.ElementTree, namespace: typing.Dict[str, str], dir: str) -> None:

        # replace ppmcalendars if needed:
        node = root.find("PPMCalendars", namespace)
        for child_config in node:
            if "include" in child_config.attrib:
                file = os.path.join(dir, child_config.attrib["include"])
                new_child_config = xml.etree.ElementTree.parse(file).getroot()
                node.insert(0, new_child_config)
                node.remove(child_config)

        # replace technologies if needed:
        node = root.find("Technologies", namespace)
        if "include" in node.attrib:
            file = os.path.join(dir, node.attrib["include"])
            new_node = xml.etree.ElementTree.parse(file).getroot()
            root.insert(0, new_node)
            root.remove(node)

    def read_xml(self) -> None:
        # start reading xml:
        input_file = self.inputs["xCropProtectionFilePath"].read().values
        namespace = {"": self.inputs["ParametrizationNamespace"].read().values}
  
        xml_tree = None
        if input_file.endswith('.xlsx'):
            # Set output file name and location
            output_file = self.inputs["XMLPath"].read().values + '\\' + os.path.basename(input_file) + '.xml'

            # Generate the xCropProtection xml file
            ExcelParser(str(input_file), namespace).parse_excel(output_file)

            # Read the resulting xml file
            xml_tree = xml.etree.ElementTree.parse(output_file)
        elif input_file.endswith('.xml'):
            xml_tree = xml.etree.ElementTree.parse(input_file)
        else:
            raise TypeError(f"The input file type must be either Excel (.xlsx) or XML (.xml).")
        
        root = xml_tree.getroot()

        # replace includes if needed:
        self.replace_includes(root, namespace, os.path.dirname(input_file))

        # create lists and containers:
        self.PPMCalendars = []
        self.Technologies = []

        # read lists and containers:
        self.set_inputs(self.PPMCalendars, root.find("PPMCalendars", namespace))
        self.set_inputs(self.Technologies, root.find("Technologies", namespace))

        # convert types if needed:
        self.convert_types()
        # set the minimum applied area for each calendar
        self.set_min_applied_area()

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

        # set output type and check that the type is valid
        output_type = str.lower(self.inputs["OutputApplicationType"].read().values)
        if output_type != "product" and output_type != "active substance":
            raise ValueError(f"Invalid output type of '{output_type}'. Valid output types are [product,active substance].")
               
        # define results:
        applied_areas = []
        applied_fields = []
        application_dates = []
        application_rates = []
        technology_drift_reductions = []
        applied_ppp = []
        applied_as = []
        as_application_rates = []

        # read fields, crop ids and geometries:
        fields = self.inputs["Fields"].read().values
        crop_ids = self.inputs["LandUseLandCoverTypes"].read().values
        field_geometries = self.inputs["FieldGeometries"].read().values

        prod_db = ProductDB(self.inputs["ProductDatabase"].read().values)
        prod_db.initialize_db()

        self.default_observer.write_message(5, f"Simulation started.")
        
        # loop over each each day
        for day in range(sim_start, sim_end + 1):
            
            # loop over each field
            for field in range(len(fields)):
                
                # loop over each ppm calendar:
                for ppm_calendar in self.PPMCalendars:

                    # check validity and crop:
                    if not ppm_calendar.is_valid(day, field) or not ppm_calendar.can_apply_on_crop(day, field, crop_ids[field]) or not ppm_calendar.can_apply_on_field(day, field, fields[field]):
                        continue

                    # sample applications:
                    applications = ppm_calendar.sample_applications(day, field, field_geometries[field])

                    # sample drift reductions and add to results:
                    for appl in applications:
                        prods, appl_rates, tech, appl_dt, appl_geom, appl_type = appl

                        # Modify length of outputs based on number of products or active substances
                        len_modifier = len(prods)

                        if appl_type == "other/active_substances" and output_type == "active substance":
                            # Result of sampling applications is active substance names
                            applied_as.extend(prods)
                            as_application_rates.extend(appl_rates)
                        elif appl_type == "other/products" and output_type == "active substance":
                            # query DB for active substances and concentrations, need to convert from product to a.s.
                            active_substances, concentrations = prod_db.sample_active_substances(prods, appl_rates)
                            
                            len_modifier = len(active_substances)
                            applied_as.extend(active_substances)
                            as_application_rates.extend(concentrations)
                        elif not (appl_type == "other/products" and output_type == "product"):
                            prod_db.close_db()
                            raise ValueError(f"Invalid Input-Output combination of {appl_type} and {output_type}.")

                        for technology in self.Technologies:
                            if technology.TechnologyName.get((day, field), "time/day, space/base_geometry") == tech:
                                drift_red = technology.sample_drift_reduction(day, field)

                        applied_areas.extend([appl_geom] * len_modifier)
                        applied_fields.extend([fields[field]] * len_modifier)
                        application_dates.extend([appl_dt] * len_modifier)
                        application_rates.extend(appl_rates)
                        technology_drift_reductions.extend([drift_red] * len_modifier)
                        applied_ppp.extend(prods)                 

        prod_db.close_db()

        self.default_observer.write_message(5, f"Simulation finished!")

        # convert results to numpy:
        applied_fields = np.array(applied_fields, dtype=np.int)
        application_dates = np.array(application_dates, dtype=int)
        application_rates = np.array(application_rates)
        as_application_rates = np.array(as_application_rates)
        technology_drift_reductions = np.array(technology_drift_reductions)

        # set outputs:
        self.outputs["AppliedFields"].set_values(applied_fields, scales="other/application")
        self.outputs["ApplicationDates"].set_values(application_dates, scales="other/application")
        self.outputs["TechnologyDriftReductions"].set_values(technology_drift_reductions, scales="other/application")
        self.outputs["AppliedAreas"].set_values(applied_areas, scales="other/application")
        if output_type == "product":
            self.outputs["AppliedPPP"].set_values(applied_ppp, scales="other/application")
            self.outputs["ApplicationRates"].set_values(application_rates, scales="other/application")
        elif output_type == "active substance":
            self.outputs["AppliedPPP"].set_values(applied_as, scales="other/application")
            self.outputs["ApplicationRates"].set_values(as_application_rates, scales="other/application")
