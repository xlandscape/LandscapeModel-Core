# Components
This file lists all components that are currently included in the Landscape Model core.
It was automatically created on 2023-09-20.


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

- Class: `numpy.ndarray`
- Unit: `None`
- Scales: `space/base_geometry`
#### Timeseries

- Class: `str`
- Unit: `None`
- Scales: `global`
#### NectarPerClass

- Class: `list[float]`
- Unit: `L/(m²*d)`
- Scales: `global`
#### PollenPerClass

- Class: `list[float]`
- Unit: `g/(m²*d)`
- Scales: `global`
#### SimulationStart

- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
#### SimulationEnd

- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
### Outputs
#### Nectar

- Scales: `space/base_geometry, time/day`
- Unit: `L/(m²*d)`
#### Pollen

- Scales: `space/base_geometry, time/day`
- Unit: `g/(m²*d)`

## BeeHave
    Prepares a BeeHave scenario.

    INPUTS
    ProcessingPath: The working directory for the component.

    OUTPUTS
    None.
    
### Inputs
#### ProcessingPath

- Class: `str`
- Unit: `None`
- Scales: `global`
#### Nectar

- Class: `numpy.ndarray`
- Unit: `L/(m²*d)`
- Scales: `space/base_geometry, time/day`
#### Pollen

- Class: `numpy.ndarray`
- Unit: `g/(m²*d)`
- Scales: `space/base_geometry, time/day`
#### BeeHaveMapCenterPointX

- Class: `float`
- Unit: `m`
- Scales: `global`
#### BeeHaveMapCenterPointY

- Class: `float`
- Unit: `m`
- Scales: `global`
#### SegmentationGridRadii

- Class: `list[float]`
- Unit: `m`
- Scales: `global`
#### SegmentationGridSteps

- Class: `int`
- Unit: `1`
- Scales: `global`
#### SegmentationGridNumberSegmentsPerRadius

- Class: `list[int]`
- Unit: `1`
- Scales: `global`
### Outputs

## CsvReader
    A generic component that reads data from a CSV file.

    INPUTS
    FilePath: A valid path to a CSV file having a header line and commas as separators.

    OUTPUTS
    The outputs of this component are provisional, i.e., they are defined by links from inputs and have to be satisfied
    by data in the CSV file. Output names equal column names in the file.
    
### Inputs
#### FilePath

### Outputs

## DeleteFolder
    A generic component that deletes a folder from the file system.

    INPUTS
    Path: A valid path of a folder to be deleted.

    OUTPUTS
    None.
    
### Inputs
#### Path

### Outputs

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

### Outputs
#### PecSoil


## DepositionToReach
    Calculates the average spray-drift deposition for reaches based on spray-drift depositions reported for base
    geometries. Base geometries are mapped to reaches, whereby the base geometry should represent an average uncovered
    area of the reach. For cases, where the base geometries contain areas of reaches that are actually covered (e.g.,
    underground), the `DepositionToReach` component allows to explicitly state this fact and exclude the reaches from
    reception of spray-drift deposition. The component has also a mode where depositions are load from a CSV file,
    which helps in simulations where spray-drift depositions are not simulated bit are known from other sources.

    OUTPUTS
    Deposition: The substance deposited at the water surface for reaches. A NumPy array of scales time/day, space/reach.
    Values have the same unit as the input deposition.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach.
    
### Inputs
#### Deposition
The rate at which the substance is deposited at the water surface. The values of this input should represent an average over the uncovered area of the reach, but the maximum of the day.
- Class: `numpy.ndarray`
- Unit: `g/ha`
- Scales: `time/day, space/base_geometry`
#### Reaches
The identifiers of individual reaches. This information is used alongside the values of the `Mapping` input to associate individual reaches to their base geometries representing average uncovered reach surfaces.
- Class: `numpy.ndarray`
- Unit: `None`
- Scales: `space/reach`
#### Mapping
Maps base geometries to reaches. Each reach should be represented also as a base geometry showing its average uncovered area if it is at least partially exposed to spray-drift.
- Class: `list[int]`
- Unit: `None`
- Scales: `space/base_geometry`
#### SprayDriftCoverage
The fraction of a reach surface that is not exposed to spray drift. If this value is `0`, the spray-deposition reported for the base geometry is also reported for the reach. If the value is `1`, a deposition of `0` is reported instead. Allowing to set the coverage of reaches to `1` helps in scenarios, where, e.g., the geodata does not differentiate between under- and overground reaches.
- Class: `list[float]`
- Unit: `1`
- Scales: `space/base_geometry`
- InList: `0.0`, `1.0`
#### DepositionInputSource
Specifies from what source the deposition input is retrieved. If set to `DepositionInputFile`, the data is read from the `DepositionInputFile`. In this case, all other inputs are ignored and the deposition reported for each reach is entirely determined by the values in the input file. Reaches not listed there will receive a deposition of `0`. If the `DepositionInputSource` is set to `DepositionInput`, the value of the `DepositionInputFile` input is ignored.
- Unit: `None`
- Scales: `global`
- InList: `DepositionInput`, `DepositionInputFile`
- Class: `str`
#### DepositionInputFile
The path to a CSV file containing predefined depositions in g/ha per reach and day. The CSV file must have an arbitrary header row and data rows consisting of the date of exposure in the format `%Y-%m-%d`, the numerical identifier of the reach that is exposed and the value of deposition as a floating point number in g/ha.
- Unit: `None`
- Scales: `global`
- Class: `str`
### Outputs
#### Deposition
The spray-drift deposition expressed as average rate. The rate depends on the reported average rate for the estimated average surface of a reach exposed to spray-drift, but may be nullified if the reach is completely covered against spray-drift, e.g., is flowing underground.
- Scales: `time/day, space/reach`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days as in the `Deposition` input, `space/reach`: the number of reaches as in the `Reaches` input
- Data_Type: the same as the one of the `Deposition` input
- Chunks: for fast retrieval of timeseries
- Unit: the same as the one of the `Deposition` input
- Element_Names: `time/day`: None, `space/reach`: as specified by the `Reaches` input
- Offset: `time/day`: the same as the ones of the `Deposition` input, `space/reach`: None
- Geometries: `time/day`: None, `space/reach`: the same as the ones of the `Reaches` input

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

- Class: `float`
- Unit: `1`
- Scales: `global`
#### EC50

- Class: `float`
- Unit: `g/ha`
- Scales: `global`
#### Exposure

- Class: `numpy.ndarray`
- Unit: `g/ha`
- Scales: `space_y/1sqm, space_x/1sqm, time/day`
### Outputs
#### Effect


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

- Class: `numpy.ndarray`
- Scales: `space_y/1sqm, space_x/1sqm, time/day`
- Unit: `g/ha`
#### RunOffExposure

- Class: `numpy.ndarray`
- Scales: `space_y/1sqm, space_x/1sqm, time/day`
- Unit: `g/ha`
#### SoilDT50

- Class: `float`
- Scales: `global`
- Unit: `d`
### Outputs
#### Pec


## ExportData
    A generic component that exports Landscape Model data into another data store. Currently, the only supported output
    store are SqlLite databases. The component allows to create a new SqlLite database or append to an existing one. It
    also features the execution of arbitrary SQL code after the export of data.
    
### Inputs
#### TargetStoreType
The type of the target store. Currently, `SqlLite` is the only supported store type.
- Class: `str`
- Scales: `global`
- Unit: `None`
- Equals: `SqlLite`
#### FilePath
The file path of the data store. If `Create` is set to `True`, the store is not allowed to already exist. If set to `False`, however, the store is required to be present on the specified location.
- Class: `str`
- Scales: `global`
- Unit: `None`
#### Values
The datasets to export. This can be virtually any data managed by the Landscape Model as far as the datatype is supported by the `SqlLite` store. Some metadata might become lost during export.
#### Create
Specifies if the data store should be created. If set to `True`, the store is not allowed to already exist, if set to `False`, it has to already exist.
- Class: `bool`
- Scales: `global`
- Unit: `None`
#### ForeignKey
An optional input that specifies foreign keys for each dimension. This value is appended to the table definition of the dataset and commonly looks like something similar to ``|`space/base_geometry`(`CascadeToxswa/hydrography_id`)``.
- Class: `list[str]`
- Scales: `global`
- Unit: `None`
#### Sql
An optional SQL statement that is executed after the export. This can, for instance, be used to create views in a SqlLite database.
- Class: `str`
- Scales: `global`
- Unit: `None`
### Outputs

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

- Class: `numpy.ndarray`
#### XLabel

- Class: `str`
#### Title

- Class: `str`
- Scales: `global`
#### XMin

- Class: `float`
- Scales: `global`
#### XMax

- Class: `float`
- Scales: `global`
#### OutputFile

- Class: `str`
- Scales: `global`
### Outputs

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

- Class: `list[bytes]`
- Scales: `space/base_geometry`
#### HydrographicReachIds

- Class: `list[int]`
- Scales: `space/base_geometry`
#### SimulationStart

- Class: `datetime.date`
- Scales: `global`
#### DisplayedTime

- Class: `datetime.datetime`
- Scales: `global`
#### Values

- Class: `numpy.ndarray`
#### ValuesReachIds

- Class: `list[int]`
- Scales: `space/reach`
#### Title

- Class: `str`
- Scales: `global`
#### OutputFile

- Class: `str`
- Scales: `global`
#### DisplayedUnit

- Class: `str`
- Scales: `global`
#### ScaleMaxValue

- Class: `float`
- Scales: `global`
#### ScaleMinValue

- Class: `float`
- Scales: `global`
#### ValuesNormalization

- Class: `str`
- Scales: `global`
#### ColorMap

- Class: `list[str]`
- Scales: `global`
### Outputs

## HydrologyFromTimeSeries
    Loads hydrological data from a hydrological scenario. A hydrological scenario is normally part of a scenario
    intended for aquatic simulations and consists of the following elements: a HDF5-file that contains the hydrological
    parameters flow, depth, volume and area (see output description for more details) plus some metadata, and, possibly,
    a folder containing CSV files detailing the lateral inflows of reaches.
    
### Inputs
#### TimeSeries
A valid file path to the input HDF5 data. This data must follow a specific format. See any of the publicly available hydrological scenarios for an example.
- Class: `str`
- Unit: `None`
- Scales: `global`
#### FromTime
The start time of the hydrological data. This specifies the first date for which hydrological data is imported into the Landscape Model. It must lay within the time frame for which data is available. Consult the scenario documentation for this time frame.
- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
#### ToTime
The end time of the hydrological data.This specifies the last date for which hydrological data is imported into the Landscape Model. It must lay within the time frame for which data is available. Consult the scenario documentation for this time frame.
- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
#### InflowTimeSeriesPath
The path where reach-inflows are stored. This path must contain a CSV file for each reach that receives lateral inflows. See any of the publicly available hydrological scenarios to learn about the specific format of the CSV files.
- Class: `str`
- Unit: `None`
- Scales: `global`
#### ImportInflows
Specifies whether lateral inflows from fields are imported. Setting this input to `False` will skip the import of CSV files from the `InflowTimeSeriesPath`. This decreases the processing time of the component, but can only be done if none of the components in the simulation require data on lateral inflows. This input should also be set to `False` if the hydrological scenario does not contain information on lateral inflows, In this case, it will not be possible to run components that require according data.
- Class: `bool`
- Unit: `None`
- Scales: `global`
#### Hydrography
The `Hydrography` input expects the geometries of reaches for which hydrological data is available in Well-Known-Byte notation. It will be used (in the correct order) to augment all outputs with scale `space/reach`.
- Class: `list[bytes]`
- Unit: `None`
- Scales: `space/reach`
### Outputs
#### Flow

- Data Type: `float`
- Scales: `time/hour, space/reach`
- Unit: `m³/d`
- Type: `numpy.ndarray`
- Shape: `time/hour`: the number of hours represented by the time span between the `FromTime` and the `ToTime`, `space/reach`: the number of reaches as stored in the `TimeSeries` input
- Chunks: for fast retrieval of timeseries
- Element_Names: `time/hour`: None, `space/reach`: as specified by the `Reaches` output
- Offset: `time/hour`: as specified by the `FromTime` input, `space/reach`: None
- Geometries: `time/hour`: None, `space/reach`: as specified by the `ReachesGeometries` output
#### Depth

- Data Type: `float`
- Scales: `time/hour, space/reach`
- Unit: `m`
- Type: `numpy.ndarray`
- Shape: `time/hour`: the number of hours represented by the time span between the `FromTime` and the `ToTime`, `space/reach`: the number of reaches as stored in the `TimeSeries` input
- Chunks: for fast retrieval of timeseries
- Element_Names: `time/hour`: None, `space/reach`: as specified by the `Reaches` output
- Offset: `time/hour`: as specified by the `FromTime` input, `space/reach`: None
- Geometries: `time/hour`: None, `space/reach`: as specified by the `ReachesGeometries` output
#### Reaches
This output lists the element names of the reaches as retrieved from the `TimeSeries` input. All outputs that have a scale of `space/reach` report reaches in the order specified by this input, except the `Inflow` output which reports reaches in the order of the `InflowReaches` output.
- Scales: `space/reach`
- Type: `numpy.ndarray`
- Shape: the number of reaches as stored in the `TimeSeries` input
- Element_Names: `space/reach`: as specified by the output itself
- Geometries: `space/reach`: as specified by the `ReachesGeometries` output
#### TimeSeriesStart

- Scales: `global`
#### TimeSeriesEnd

- Scales: `global`
#### Volume

- Data Type: `float`
- Scales: `time/hour, space/reach`
- Unit: `m³`
- Type: `numpy.ndarray`
- Shape: `time/hour`: the number of hours represented by the time span between the `FromTime` and the `ToTime`, `space/reach`: the number of reaches as stored in the `TimeSeries` input
- Chunks: for fast retrieval of timeseries
- Element_Names: `time/hour`: None, `space/reach`: as specified by the `Reaches` output
- Offset: `time/hour`: as specified by the `FromTime` input, `space/reach`: None
- Geometries: `time/hour`: None, `space/reach`: as specified by the `ReachesGeometries` output
#### Area

- Data Type: `float`
- Scales: `time/hour, space/reach`
- Unit: `m²`
- Type: `numpy.ndarray`
- Shape: `time/hour`: the number of hours represented by the time span between the `FromTime` and the `ToTime`, `space/reach`: the number of reaches as stored in the `TimeSeries` input
- Chunks: for fast retrieval of timeseries
- Element_Names: `time/hour`: None, `space/reach`: as specified by the `Reaches` output
- Offset: `time/hour`: as specified by the `FromTime` input, `space/reach`: None
- Geometries: `time/hour`: None, `space/reach`: as specified by the `ReachesGeometries` output
#### InflowReaches
This output lists the element names of reaches as reported by the `Inflow` output. This order may differ from the order of reaches in all other outputs with scale `space/reach`.
- Scales: `space/reach`
- Type: `numpy.ndarray`
- Shape: `space/reach`: the number of reaches for which inflow-data is available
- Element_Names: `space/reach`: as specified by the output itself
- Geometries: `space/reach`: as specified by the `InflowReachesGeometries` output
#### Inflow

- Data Type: `float`
- Scales: `time/hour, space/reach`
- Unit: `m³/d`
- Type: `numpy.ndarray`
- Shape: `time/hour`: the number of hours represented by the time span between the `FromTime` and the `ToTime`, `space/reach`: the number of reaches as stored in the `InflowReaches` input
- Chunks: for fast retrieval of timeseries
- Element_Names: `time/hour`: None, `space/reach`: as specified by the `InflowReaches` output
- Offset: `time/hour`: as specified by the `FromTime` input, `space/reach`: None
- Geometries: `time/hour`: None, `space/reach`: as specified by the output itself
#### ReachesGeometries
This output lists the geometries of reaches as reported by the `Inflow` output. This order may differ from the order of reaches in all other outputs with scale `space/reach`.
- Scales: `space/reach`
- Type: `list`
- Shape: the number of reaches as stored in the `TimeSeries` input
- Element_Names: `space/reach`: as specified by the `Reaches` output
- Geometries: `space/reach`: as specified by the output itself
#### InflowReachesGeometries
This output lists the geometries of the reaches as retrieved from the `Hydrography` input. All outputs that have a scale of `space/reach` report reaches in the order specified by this input, except the `Inflow` output which reports reaches in the order of the `InflowReachesGeometries` output.
- Scales: `space/reach`
- Type: `list`
- Shape: the number of reaches as stored in the `TimeSeries` input
- Element_Names: `space/reach`: as specified by the `Reaches` output
- Geometries: `space/reach`: as specified by the output itself

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

- Class: `list[int]`
- Unit: `None`
- Scales: `space/base_geometry`
#### Mapping

- Class: `str`
- Unit: `None`
- Scales: `global`
#### VegetationClasses

- Class: `str`
- Unit: `None`
- Scales: `global`
### Outputs
#### Vegetation

- Scales: `space/base_geometry`
- Unit: `None`

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

### Outputs

## LandscapeScenario
    Provides geospatial data of landscape scenarios to the Landscape Model. The geospatial data normally consists of a
    set of one or more shapefiles, accompanied by an arbitrary number of GeoTIFFs. The data package also includes an
    XML file named `package.xinfo` that details the contents of the package and provides metainformation about the
    package. It also links individual pieces of information, e.g., individual columns of the shapefiles' attributes, to
    an informal Landscape Model vocabulary. The set of outputs of the `LandscapeScenario` component differs on the kind
    of scenario (e.g., off-field soil scenarios versus aquatic scenarios) and is defined by an XML schema (see input
    descriptions for details). Some outputs are generic and are documented here. For additional outputs, see the
    documentation of the scenario.
    
### Inputs
#### BaseLandscapeGeometries
A valid file path to a package file. The package file is an XML file that contains metadata about the geospatial data of a landscape scenario. Only landscape scenarios with auch a metadata description are compatible with the `LandscapeScenario` component. The package file is commonly name `package.xinfo` and resides alongside the geodata of a landscape scenario. Scenarios normally provide the absolute file path to the package file as a macro to the landscape model. This macro is commonly named `$(:LandscapeScenario)`, a value that should therefore normally be used for configuration of the component.  
The `LandscapeScenario` component allows to import landscape scenarios for a wide range of simulations which differ in their geospatial requirements (e.g., off-field soil simulations compared with aquatic simulations). The `GeoPackageNamespace` input defines the domain of the simulation regarding this requirements. The structure of the XML is described by an XML schema (`package.xsd` in the `model/variant` folder) and the package file itself must make use of the specified namespace and validate against the XML schema.
- Class: `str`
- Unit: `None`
- Scales: `global`
- Ontology: ``
#### GeoPackageNamespace
The XML namespace for the metadata of the landscape scenario. This should be the target namespace of the XML schema (`model/variant/package.xsd`) of this model, e.g., `urn:xAquaticRiskLandscapeScenarioPackageInfo` for an aquatic scenario. Make sure that the scenario's geodata description (`package.xinfo`) makes use of this namespace.
- Class: `str`
- Unit: `None`
- Scales: `global`
### Outputs

## MarsWeather
    Provides MARS weather data from a CSV file to the Landscape Model. The CSV file must have a header and must contain
    the following columns in arbitrary order: DAY, MONTH, YEAR. Each row of the CSV file gives data for one day, and
    which day this is, is specified as the numerical day of month (DAY), month of year (MONTH) and the year (YEAR).
    Values in columns named equal to the component's outputs are parsed and used for the outputs. See the documentation
    of outputs for additional information on the expected values. The CSV file may contain additional columns that are
    not used by the component.
    
### Inputs
#### FilePath
A valid file path to a CSV file containing MARS weather data. See above for the expected format of the CSV file.
- Class: `str`
- Unit: `None`
- Scales: `global`
### Outputs
#### TEMPERATURE_AVG
The mean air temperature. The definition of mean air temperature reflects the one of the JRC MARS meteorological database (https://agri4cast.jrc.ec.europa.eu/dataportal/).
- Scales: `time/day`
- Unit: `°C`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days for which weather data is present in the input file
- Offset: `time/day`: the first date listed in the input file
#### PRECIPITATION
The sum of precipitation. The definition of the sum of precipitation reflects the one of the JRC MARS meteorological database (https://agri4cast.jrc.ec.europa.eu/dataportal/).
- Scales: `time/day`
- Unit: `mm/d`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days for which weather data is present in the input file
- Offset: `time/day`: the first date listed in the input file
#### ET0
The potential evapotranspiration from a crop canopy. The definition of potential evapotranspiration from a crop canopy reflects the one of the JRC MARS meteorological database (https://agri4cast.jrc.ec.europa.eu/dataportal/).
- Scales: `time/day`
- Unit: `mm/d`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days for which weather data is present in the input file
- Offset: `time/day`: the first date listed in the input file
#### WINDSPEED
The mean daily wind speed at 10m. The definition of the mean daily wind speed at 10m reflects the one of the JRC MARS meteorological database (https://agri4cast.jrc.ec.europa.eu/dataportal/).
- Scales: `time/day`
- Unit: `m/s`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days for which weather data is present in the input file
- Offset: `time/day`: the first date listed in the input file
#### RADIATION
The total global radiation. The definition of the total global radiation reflects the one of the JRC MARS meteorological database (https://agri4cast.jrc.ec.europa.eu/dataportal/).
- Scales: `time/day`
- Unit: `kJ/(m²*d)`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days for which weather data is present in the input file
- Offset: `time/day`: the first date listed in the input file

## PpmCalendar
    Creates a calendar for pesticide applications for all or some landscape features of a specific type based on fixed
    values for application rate, technological drift reduction, in-crop buffers and in-field margin. Application dates
    are uniformly sampled from application windows. It is possible to specify application sequences by defining more
    than one application window. Whether a specific landscape feature receives an application is controlled by a
    specified probability.
    
### Inputs
#### SimulationStart
The first day of the simulation. No applications prior to this date will be written into the calendar.
- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
#### SimulationEnd
The last day of the simulation. No applications after this date will be written into the calendar.
- Class: `datetime.date`
- Unit: `None`
- Scales: `global`
#### ApplicationWindows
A definition of application windows. The value must follow the format `MM-DD to MM-DD[, MM-DD to MM-DD...]`, where `MM` is the month of year and `DD` is the day of month. Application dates are sampled within the specified time window for each year in the period from `SimulationStart` to `SimulationEnd` individually. If multiple application windows are specified, a single application will take place in each of the windows, sampled individually.
- Class: `str`
- Unit: `None`
- Scales: `global`
#### Fields
A list of identifiers of individual geometries. This input will be removed in a future version of the `PpmCalendar` component.
- Class: `list[int]`
- Unit: `None`
- Scales: `space/base_geometry`
#### LandUseLandCoverTypes
The land-use and land-cover type of spatial units. This information is used to determine applied landscape elements (i.e., target fields), by only considering base geometries that have a land use/land cover type equal to the `TargetLandUseLandCoverType` input.
- Class: `list[int]`
- Unit: `None`
- Scales: `space/base_geometry`
#### TargetLandUseLandCoverType
The land-use or land-cover type that receives pesticide applications. It filters the base geometries described by the `LandUseLandCoverTypes` input to those that have the according value. Only the filtered landscape elements will be considered for applications, based on a probability defined by the `ProbabilityFieldApplied` input.
- Class: `str`
- Unit: `None`
- Scales: `global`
#### ApplicationRate
The application rate. The `PpmCalendar` component applies the same rate to all applications. If your use-case requires different rates, e.g., within a application sequence, another component has to be used.
- Class: `float`
- Unit: `g/ha`
- Scales: `global`
#### TechnologyDriftReduction
The fraction by which spray-drift is reduced due to technological measures. The technological drift-reduction has to be a value between `0` and `1`, with `0` representing spray-equipment that does not reduce drift-deposition relative to the equipment used for the derivation of regulatory drift-depositions values and `1` resulting in drift-deposition being prevented entirely due to technological measures.
- Class: `float`
- Unit: `1`
- Scales: `global`
#### InCropBuffer
An in-crop buffer used during application. The in-crop buffer is a section along the boundary of the applied landscape feature of the specified width that does not receive applications. The in-crop buffer is geometrically removed from the applied feature to determine the applied area.
- Class: `float`
- Unit: `m`
- Scales: `global`
#### InFieldMargin
A margin without crops within fields. The in-field margin is an additional section between the boundary of the applied landscape feature and the in-crop buffer that is, like the in-crop buffer, does not receive applications, but is also considered to have no crops planted on it. Like the in-crop buffer, it is geometrically removed from the base geometries to derive the geometry of the applied area.
- Class: `float`
- Unit: `m`
- Scales: `global`
#### FieldGeometries
The geometries of individual landscape parts. This input will be removed in a future version of the `PpmCalendar` component.
- Class: `list[bytes]`
- Unit: `None`
- Scales: `space/base_geometry`
#### MinimumAppliedArea
The minimum applied area considered. If the applied area of a landscape feature is, after applying the in-crop buffer and in-field margin is smaller than this threshold, then no application is scheduled for this feature.
- Class: `float`
- Unit: `m²`
- Scales: `global`
#### RandomSeed
An initialization for the random number generator. Setting this input to a value other than `0` seeds the random number generator. This can be useful for debugging or checking results. A value of `0` initializes the random number generator randomly.
- Class: `int`
- Unit: `None`
- Scales: `global`
#### ProbabilityFieldApplied
The probability with which a field is applied, given as a number between `0` and `1`. A landscape feature is excluded entirely from the PPM calendar, if it is not selected for application based on the probability specified here. A value of `0` would result in an empty PPM calendar, a value of `1` in all landscape features being applied, if no other considerations (land use/land cover type filter and minimum area applied) prevent this.
- Class: `float`
- Unit: `1`
- Scales: `global`
### Outputs
#### AppliedFields
The element names of the applied fields. This output should not be interpreted in a way that necessarily the entire field received an application, for the spatial extent of the application see the `AppliedAreas` output, instead. The values of this output link, however, applications to fields, which can be an interesting parameter for statistics or plotting.
- Scales: `other/application`
- Type: `numpy.ndarray`
- Data_Type: `int`
- Shape: `other/application`: the number of applications simulated by the component
#### ApplicationDates
The dates at which applications were conducted. Dates are represented as ordinal numbers, as a result of applying the according function of the `datetime.date` object.
- Scales: `other/application`
- Type: `numpy.ndarray`
- Data_Type: `int`
- Shape: `other/application`: the number of applications simulated by the component
#### ApplicationRates
The application rates for each individual application. See the `ApplicationRate` input for further details.
- Scales: `other/application`
- Type: `numpy.ndarray`
- Data_Type: `numpy.float64`
- Shape: `other/application`: the number of applications simulated by the component
- Unit: the same as that of the `ApplicationRate` input
#### TechnologyDriftReductions
The spray-drift reduction by the spray-equipment, expressed as a fraction between `0` and `1`. See the `TechnologyDriftReduction` input for more details.
- Scales: `other/application`
- Type: `numpy.ndarray`
- Data_Type: `numpy.float64`
- Shape: `other/application`: the number of applications simulated by the component
- Unit: the same as that of the `TechnologyDriftReduction` input
#### AppliedAreas
The geometries of the applied areas, represented in Well-Known-Bytes notation. See the `InCropBuffer` and `InFieldMargin` inputs for further details on how the geometries are derived.
- Scales: `other/application`
- Type: `list`
- Shape: `other/application`: the number of applications simulated by the component

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

- Class: `float`
- Unit: `g/ha`
- Scales: `global`
#### Exposure

- Class: `numpy.ndarray`
- Unit: `g/ha`
- Scales: `space_y/1sqm, space_x/1sqm, time/day`
### Outputs
#### TER

#### RQ


## UserParameters
    Encapsulates a set of user-defined parameters as a Landscape Model component.

    INPUTS
    None.

    OUTPUTS
    As defined by the user parameters passed to the initialization method of the component.
    
### Inputs
### Outputs

## WaterTemperatureFromAirTemperature
    A simple component that takes a series of daily average air temperatures and calculates a series of daily water
    temperatures by averaging the air temperatures of the current and the two preceding days. The water temperatures
    of the first two days in the timeseries are set to the one calculated for the third day.
    
### Inputs
#### AirTemperature
A timeseries of daily average air temperatures. Water temperatures will be output for the temporal extent spanned by the air temperatures.
- Class: `numpy.ndarray`
- Scales: `time/day`
- Unit: `°C`
### Outputs
#### WaterTemperature
A timeseries of daily average water temperatures. The water temperature as estimated as a 3-day moving average of the air temperature.
- Scales: `time/day`
- Unit: `°C`
- Requires Indexing: `True`
- Type: `numpy.ndarray`
- Shape: `time/day`: the number of days reported in the `AirTemperature` input
- Offsets: `time/day`: the first date reported in the `AirTemperature` input