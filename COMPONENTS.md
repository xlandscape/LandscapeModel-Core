# Components
This file lists all components that are currently included in the Landscape Model core.
It was automatically created on 2023-09-14.


## BeeForage
    Simulates nectar and pollen availability to bees based on vegetation and timeseries per vegetation class.

    INPUTS
    Vegetation: Vegetation classes at a scale of space/base_geometry.
    Timeseries: A path to an Excel table containing timeseries detailing pollen and nectar availability per vegetation
    class.
    NectarPerClass: The nectar availability in L/(m²*d) for each bee forage class.
    PollenPerClass: The pollen availability in g/(m²*d) for each bee forage class.
    SimulationStart: The first day of the simulation for which bee forage availability is to be simulated.
    SimulationEnd: The last day of the simulation for which bee forage availability is to be simulated.

    OUTPUTS
    Nectar: The availability of nectar to bees in L/(m²*d) at a scale of space/base_geometry and time/day.
    Pollen: The availability of pollen to bees in g/(m²*d) at a scale of space/base_geometry and time/day.
    
### Inputs
#### Vegetation
  
Class: `numpy.ndarray`  
Unit: `None`  
Scales: `space/base_geometry`
#### Timeseries
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### NectarPerClass
  
Class: `list[float]`  
Unit: `L/(m²*d)`  
Scales: `global`
#### PollenPerClass
  
Class: `list[float]`  
Unit: `g/(m²*d)`  
Scales: `global`
#### SimulationStart
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`
#### SimulationEnd
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`

## BeeHave
    Prepares a BeeHave scenario.

    INPUTS
    ProcessingPath: The working directory for the component.

    OUTPUTS
    None.
    
### Inputs
#### ProcessingPath
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### Nectar
  
Class: `numpy.ndarray`  
Unit: `L/(m²*d)`  
Scales: `space/base_geometry, time/day`
#### Pollen
  
Class: `numpy.ndarray`  
Unit: `g/(m²*d)`  
Scales: `space/base_geometry, time/day`
#### BeeHaveMapCenterPointX
  
Class: `float`  
Unit: `m`  
Scales: `global`
#### BeeHaveMapCenterPointY
  
Class: `float`  
Unit: `m`  
Scales: `global`
#### SegmentationGridRadii
  
Class: `list[float]`  
Unit: `m`  
Scales: `global`
#### SegmentationGridSteps
  
Class: `int`  
Unit: `1`  
Scales: `global`
#### SegmentationGridNumberSegmentsPerRadius
  
Class: `list[int]`  
Unit: `1`  
Scales: `global`

## CsvReader
    A generic component that reads data from a CSV file.

    INPUTS
    FilePath: A valid path to a CSV file having a header line and commas as separators.

    OUTPUTS
    The outputs of this component are provisional, i.e., they are defined by links from inputs and have to be satisfied
    by data in the CSV file. Output names equal column names in the file.
    
### Inputs
#### FilePath


## DeleteFolder
    A generic component that deletes a folder from the file system.

    INPUTS
    Path: A valid path of a folder to be deleted.

    OUTPUTS
    None.
    
### Inputs
#### Path


## DepositionToPecSoil
    Calculates the PEC soil from surface deposition by a simple homogeneous distribution of mass in the topsoil layer.

    INPUTS
    Deposition: The deposition on the soil surface.
    SoilBulkDensity: The density of the soil layer.
    Depth: The depth of the soil layer in which the deposition is distributed equally.

    OUTPUTS
    PecSoil: The homogeneous concentration of substance in soil. A NumPy array with scales time/day, space_x/1sqm,
    space_y/1sqm.
    
### Inputs
#### Deposition

#### SoilBulkDensity

#### Depth


## DepositionToReach
    Calculates the initial environmental fate in reaches for spray-drift depositions.

    INPUTS
    Deposition: The substance deposited at the water surface. A NumPy array of scales time/day, space/base_geometry.
    Values have a unit of g/ha.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach. Values have no unit.
    Mapping: Maps base geometries to reaches. A list[int] of scale space/base_geometry. Values have no unit.
    SprayDriftCoverage: The fraction of a reach surface that is not exposed to spray drift. A list[float] of scale
    space/reach. Values have no unit. Currently, only values of 0 and 1 are supported.
    DepositionInputSource: Specifies from what source the deposition input is retrieved. A string of global scale.
    Allowed values are 'DepositionInput' and 'DepositionInputFile' which refer to the inputs of same names.
    DepositionInputFile: The path to a CSV file containing predefined depositions in g/ha per reach and day. A string
    of global scale.

    OUTPUTS
    Deposition: The substance deposited at the water surface for reaches. A NumPy array of scales time/day, space/reach.
    Values have the same unit as the input deposition.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach.
    
### Inputs
#### Deposition
  
Class: `numpy.ndarray`  
Unit: `g/ha`  
Scales: `time/day, space/base_geometry`
#### Reaches
  
Class: `numpy.ndarray`  
Unit: `None`  
Scales: `space/reach`
#### Mapping
  
Class: `list[int]`  
Unit: `None`  
Scales: `space/base_geometry`
#### SprayDriftCoverage
  
Class: `list[float]`  
Unit: `1`  
Scales: `space/base_geometry`  
InList: `0`, `1`
#### DepositionInputSource
  
Unit: `None`  
Scales: `global`  
InList: `DepositionInput`, `DepositionInputFile`  
Class: `str`
#### DepositionInputFile
  
Unit: `None`  
Scales: `global`  
Class: `str`

## DoseResponse
    Calculates an effect based on a log-logistic dose-response function.

    INPUTS
    SlopeFactor: The slope parameter of the log-logistic function. A float with global scale. Value has unit 1.
    EC50: The concentration of 50 percent effect. A float with global scale. Value has a unit g/ha.
    Exposure: The exposure for which effects are to be calculated. A NumPy array with scales time/day, space_x/1sqm,
    space_y/1sqm. Values have a unit g/ha.

    OUTPUTS
    Effect: The calculated effect. A NumPy array with the same scale as the exposure input. Values have a unit of 1.
    
### Inputs
#### SlopeFactor
  
Class: `float`  
Unit: `1`  
Scales: `global`
#### EC50
  
Class: `float`  
Unit: `g/ha`  
Scales: `global`
#### Exposure
  
Class: `numpy.ndarray`  
Unit: `g/ha`  
Scales: `space_y/1sqm, space_x/1sqm, time/day`

## EnvironmentalFate
    Calculates environmental fate based on a simple half-time degradation.

    INPUTS
    SprayDriftExposure: The exposure due to spray-drift.
    RunOfExposure: The exposure due to run-off.
    SoilDT50: The half-time for substance degradation in soil.

    OUTPUTS
    Pec: The concentration of substance considering exposure and degradation. A NumPy array of scales time/day,
    space_x/1sqm, space_y/1sqm.
    
### Inputs
#### SprayDriftExposure
  
Class: `numpy.ndarray`  
Scales: `space_y/1sqm, space_x/1sqm, time/day`  
Unit: `g/ha`
#### RunOffExposure
  
Class: `numpy.ndarray`  
Scales: `space_y/1sqm, space_x/1sqm, time/day`  
Unit: `g/ha`
#### SoilDT50
  
Class: `float`  
Scales: `global`  
Unit: `d`

## ExportData
    A generic component that exports Landscape Model data into another data store.

    INPUTS
    TargetStoreType: The type of the target store. A string of global scale. Must be "SqlLite". Value has no unit.
    FilePath: The file path of the non-existing data store. A string of global scale. Value has no unit.
    Values: The datasets to export.
    Create: Specifies if the data store should be created. A bool of global scale. Value has no unit.
    ForeignKey: An optional input that specifies foreign keys for each dimension. A list[str] with global scale. Values
    have no unit.
    Sql: An optional SQL statement that is executed after the export. A string with global scale. Value has no unit.

    OUTPUTS
    None.
    
### Inputs
#### TargetStoreType
  
Class: `str`  
Scales: `global`  
Unit: `None`
#### FilePath
  
Class: `str`  
Scales: `global`  
Unit: `None`
#### Values

#### Create
  
Class: `bool`  
Scales: `global`  
Unit: `None`
#### ForeignKey
  
Class: `list[str]`  
Scales: `global`  
Unit: `None`
#### Sql
  
Class: `str`  
Scales: `global`  
Unit: `None`

## ReportingDistribution
    Draws a distribution of values.

    INPUTS
    Values: The input values. A NumPy array.
    XLabel: The label of the x-axis. A string.
    Title: The title of the plot. A string of global scale.
    XMin: The minimum x-value to display. A float of global sale.
    XMax: The maximum x-value to display. A float of global sale.
    OutputFile: A valid file path to write the plot to. A string of global scale.

    OUTPUTS
    None.
    
### Inputs
#### Values
  
Class: `numpy.ndarray`
#### XLabel
  
Class: `str`
#### Title
  
Class: `str`  
Scales: `global`
#### XMin
  
Class: `float`  
Scales: `global`
#### XMax
  
Class: `float`  
Scales: `global`
#### OutputFile
  
Class: `str`  
Scales: `global`

## ReportingHydrographicMap
    Draws a map displaying the distribution of values in a hydrographic network.

    INPUTS
    Hydrography: The hydrographic network geometries. A list[bytes] of scale space/base_geometry.
    HydrographicReachIds: The identifiers of reaches according to the hydrography. A list[int] of scale
    space/base_geometry.
    SimulationStart: The first day of the simulation. A `datetime.date` of global scale.
    DisplayedTime: The time displayed in the map. A `datetime.date` of global scale.
    Values: The values to map onto the hydrographic network. A NumPy array.
    ValuesReachIds: The reach identifiers according to the values. A list[int] of scale space/reach.
    Title: The title of the plot. A string of global scale.
    OutputFile: A valid path to a file where the plot is written to. A string of global scale.
    DisplayedUnit: The unit in which values should be displayed. A string of global scale.
    ScaleMaxValue: The maximum value to which the legend is scaled. A float of global scale.
    ScaleMinValue: The minimum value to which the legend is scaled. A float of global scale.
    ValuesNormalization: The normalization applied to the values. A string of global scale.
    ColorMap: The color map used for displaying the values. A list[str] with global scale.

    OUTPUTS
    None.
    
### Inputs
#### Hydrography
  
Class: `list[bytes]`  
Scales: `space/base_geometry`
#### HydrographicReachIds
  
Class: `list[int]`  
Scales: `space/base_geometry`
#### SimulationStart
  
Class: `datetime.date`  
Scales: `global`
#### DisplayedTime
  
Class: `datetime.datetime`  
Scales: `global`
#### Values
  
Class: `numpy.ndarray`
#### ValuesReachIds
  
Class: `list[int]`  
Scales: `space/reach`
#### Title
  
Class: `str`  
Scales: `global`
#### OutputFile
  
Class: `str`  
Scales: `global`
#### DisplayedUnit
  
Class: `str`  
Scales: `global`
#### ScaleMaxValue
  
Class: `float`  
Scales: `global`
#### ScaleMinValue
  
Class: `float`  
Scales: `global`
#### ValuesNormalization
  
Class: `str`  
Scales: `global`
#### ColorMap
  
Class: `list[str]`  
Scales: `global`

## HydrologyFromTimeSeries
    Loads hydrological data from an HDF5 file.

    INPUTS
    TimeSeries: A valid file path to the input HDF5 data. A string of global scale. Value has no unit.
    FromTime: The start time of the requested hydrology. A `datetime.date` of global scale. Value has no unit.
    ToTime: The end time of the requested hydrology. A `datetime.date` of global scale. Value has no unit.
    InflowTimeSeriesPath: The path where reach-inflows are stored. A string of global scale. Value has no unit.
    ImportInflows: Specifies whether reach inflows from fields are imported. A bool of global scale. Value has no unit.

    OUTPUTS
    Flow: The water flow. A NumPy array of scales time/hour, space/reach. Values have a unit of m³/d.
    Depth: The water depth. A NumPy array of scales time/hour, space/reach. Values have a unit m.
    Reaches: The numeric identifier of reaches. A list[int] of scale space/reach.
    TimeSeriesStart: The start time of the hydrological data. A datetime.datetime of global scale. Value has no unit.
    TimeSeriesEnd: The end time of the hydrological data. A datetime.datetime of global scale. Value has no unit.
    Volume: The water volume. A NumPy array of scales time/hour, space/reach. Values have a unit of m³.
    Area: The water surface area. A NumPy array of scales time/hour, space/reach. Values have a unit of m².
    InflowReaches: Identifier that receive inflows from fields. A NumPy array of scale space/reach2. Values have no
    unit.
    Inflow: Inflows into reaches from fields. A NumPy array of scale time/hour, space/reach2. Values have a unit of
    m³/d.
    
### Inputs
#### TimeSeries
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### FromTime
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`
#### ToTime
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`
#### InflowTimeSeriesPath
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### ImportInflows
  
Class: `bool`  
Unit: `None`  
Scales: `global`

## LandCoverToVegetation
    Translates land cover into vegetation information using a simple lookup-table approach.

    INPUTS
    LandCover: A list of integer identifiers that detail the land use / land cover type of individual elements at scale
    space/base_geometry. Identifiers have no units.
    Mapping: A file path to an Excel workbook that contains information on how to map land cover classes into
    vegetation classes.
    VegetationClasses: A JSON file containing defined vegetation classes and their numerical code.

    OUTPUTS
    Vegetation: A list of vegetation classes at a space/base_geometry scale.
    
### Inputs
#### LandCover
  
Class: `list[int]`  
Unit: `None`  
Scales: `space/base_geometry`
#### Mapping
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### VegetationClasses
  
Class: `str`  
Unit: `None`  
Scales: `global`

## LandscapeScenarioPreparation
    A component that prepares landscape scenarios ingested by the LandscapeScenario component from geo-files.

    INPUTS
    OutputPath: The path where to write the landscape scenario to.
    LandscapeScenarioVersion: The version of the landscape scenario.
    LandscapeScenarioDescription: A description of the landscape scenario.
    TargetFieldLandUseLandCoverType: The identifier of the target land-use / land-cover type.
    BaseLandscapeGeometries: The base landscape geometries.
    FeatureIdAttribute: The name of the feature ID attribute.
    DEM: A digital elevation model.

    OUTPUTS
    None.
    
### Inputs
#### OutputPath

#### LandscapeScenarioVersion

#### LandscapeScenarioDescription

#### TargetFieldLandUseLandCoverType

#### HabitatLUseLandCoverTypes

#### BaseLandscapeGeometries

#### FeatureIdAttribute

#### FeatureLandUsLandCoverTypeAttribute

#### DEM


## LandscapeScenario
    Provides landscape scenarios to the Landscape Model.

    INPUTS
    BaseLandscapeGeometries: A valid file path to a package file. A string of global scale. Value has no unit.
    No ontological description is associated with the input.

    OUTPUTS
    The outputs of this component are provisional, i.e., they are defined by links from inputs and have to be satisfied
    by data in the CSV file. Outputs are Crs, Extent, and information specified in the package information file of the
    landscape scenario.
    
### Inputs
#### BaseLandscapeGeometries
  
Class: `str`  
Unit: `None`  
Scales: `global`  
Ontology: ``
#### GeoPackageNamespace
  
Class: `str`  
Unit: `None`  
Scales: `global`

## MarsWeather
    Provides MARS weather data from a CSV fle to the Landscape Model.

    INPUTS
    FilePath: A valid file path to a CSV file containing MARS weather data. A string of global scale. Value has no unit.
    FirstDate: The first date of the requested weather information. A `datetime.date` of global scale. The value has no
    unit.
    LastDate: The last date of the requested weather information. A `datetime.date` of global scale. The value has no
    unit.

    OUTPUTS
    TEMPERATURE_AVG: The average temperature. A NumPy array of scale time/day. Values have a unit of °C.
    
### Inputs
#### FilePath
  
Class: `str`  
Unit: `None`  
Scales: `global`

## PpmCalendar
    Encapsulates the PpmCalendar as a Landscape Model component.

    INPUTS
    SimulationStart: The first day of the simulation. A `datetime.date` of global scale. Value has no unit.
    SimulationEnd: The last day of the simulation. A `datetime.date` of global scale. Value has no unit.
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
    AppliedAreas: The geometries of the applied areas. A list[bytes] of scale other/application. The values have no
    unit.
    
### Inputs
#### SimulationStart
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`
#### SimulationEnd
  
Class: `datetime.date`  
Unit: `None`  
Scales: `global`
#### ApplicationWindows
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### Fields
  
Class: `list[int]`  
Unit: `None`  
Scales: `space/base_geometry`
#### LandUseLandCoverTypes
  
Class: `list[int]`  
Unit: `None`  
Scales: `space/base_geometry`
#### TargetLandUseLandCoverType
  
Class: `str`  
Unit: `None`  
Scales: `global`
#### ApplicationRate
  
Class: `float`  
Unit: `g/ha`  
Scales: `global`
#### TechnologyDriftReduction
  
Class: `float`  
Unit: `1`  
Scales: `global`
#### InCropBuffer
  
Class: `float`  
Unit: `m`  
Scales: `global`
#### InFieldMargin
  
Class: `float`  
Unit: `m`  
Scales: `global`
#### FieldGeometries
  
Class: `list[bytes]`  
Unit: `None`  
Scales: `space/base_geometry`
#### MinimumAppliedArea
  
Class: `float`  
Unit: `m²`  
Scales: `global`
#### RandomSeed
  
Class: `int`  
Unit: `None`  
Scales: `global`
#### ProbabilityFieldApplied
  
Class: `float`  
Unit: `1`  
Scales: `global`

## TerRQ
    Calculates the TER and the RQ.

    INPUTS
    Threshold: The threshold applied. A float of global scale. Value has a unit of g/ha.
    Exposure: The exposure considered. A NumPy array of scales time/day, space_x/1sqm, space_y/1sqm. Values have a unit
    of g/ha.

    OUTPUTS
    TER: The calculated TER. A NumPy array of the same scales as the exposure input. Values have a unit of 1.
    RQ: The calculated RQ. A NumPy array of the same scales as the exposure input. Values have a unit of 1.
    
### Inputs
#### Threshold
  
Class: `float`  
Unit: `g/ha`  
Scales: `global`
#### Exposure
  
Class: `numpy.ndarray`  
Unit: `g/ha`  
Scales: `space_y/1sqm, space_x/1sqm, time/day`

## UserParameters
    Encapsulates a set of user-defined parameters as a Landscape Model component.

    INPUTS
    None.

    OUTPUTS
    As defined by the user parameters passed to the initialization method of the component.
    
### Inputs

## WaterTemperatureFromAirTemperature
    A simple component that takes a series of daily average air temperatures and calculates a series of daily water
    temperatures by averaging the air temperatures of the current and the two preceding days. The water temperatures
    of the first two days are set to the one calculated for the third day.

    INPUTS
    AirTemperature: A timeseries of daily average air temperatures.

    OUTPUTS
    WaterTemperature: A timeseries of daily average water temperatures.
    
### Inputs
#### AirTemperature
  
Class: `numpy.ndarray`  
Scales: `time/day`  
Unit: `°C`