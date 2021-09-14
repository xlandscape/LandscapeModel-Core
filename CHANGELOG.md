# Changelog
This is the changelog for the Landscape Model core. It was automatically created on 2021-09-14.

## [1.6.5] - 2021-09-14

### Added
- `base.functions.run_process()` makes use of new Python dict union operator

### Changed

### Fixed


## [1.6.4] - 2021-09-13

### Added
- `attrib.Unit` support for lists
- Further unit conversion to `attrib.Unit` 

### Changed
- `components.LandscapeScenario` reads physical units from package metadata

### Fixed


## [1.6.3] - 2021-09-09

### Added

### Changed
- `observer.LogFileObserver` uses utf-8 encoding for logfiles

### Fixed


## [1.6.2] - 2021-09-08

### Added

### Changed

### Fixed


## [1.6.1] - 2021-09-03

### Added

### Changed
- updated Python packages
- Updated `components.LandscapeScenarioPreparation` to new metadata format
- Renamed to `components.LandscapeScenario`
- Renamed some parameters in `components.PpmCalendar`
- `components` imports updated to reflect renamed components

### Fixed


## [1.6] - 2021-09-02

### Added

### Changed
- updated runtime environment to Python 3.9.7
- `store.X3dfStore` acknowledges that HDF-stored strings are now returned as bytes
- `components.HydrologyFromTimeSeries` casts exported WKB geometries to bytes
- `components.LandscapeScenario` updated path to Proj4 library
- `components.LandscapeScenario` casts exported WKB geometries to bytes
- `components.PpmCalendar` casts exported WKB geometries to bytes

### Fixed


## [1.5.10] - 2021-08-27

### Added
- `base.documentation.document_component()` support for documentation of unit attribute hint

### Changed

### Fixed


## [1.5.9] - 2021-08-23

### Added
- `base.functions.run_process()` option to run external processes minimized

### Changed

### Fixed


## [1.5.8] - 2021-08-18

### Added
- `base.documentation.document_component()` documentation of data_type attribute hint and default attribute

### Changed
- `base.documentation.document_component()` can now handle sample configurations with component names differing 
    from object name
- `base.documentation.document_component()`: long lines in XML samples are now wrapped to ensure 120 character 
    width

### Fixed


## [1.5.7] - 2021-08-17

### Added
- `base.documentation.document_component()` documentation of `Equals` attribute

### Changed

### Fixed


## [1.5.6] - 2021-08-13

### Added

### Changed

### Fixed
- Handling of omitted `base.Output` attribute hints


## [1.5.5] - 2021-08-05

### Added

### Changed
- renamed `LICENSE.txt` to `LICENSE` 

### Fixed
- spelling error in readme


## [1.5.4] - 2021-07-16

### Added

### Changed
- parsing of raw parameters in `base.functions` 
- `components.DepositionToPecSoil` retrieval of output data type
- `components.MarsWeather` warning if weather file misses parameters

### Fixed
- stripping of raw configuration values in `base.functions` 
- `components.ExportData` data type access


## [1.5.3] - 2021-07-15

### Added
- `base.documentation.write_changelog()` no longer escapes underscores

### Changed
- `base.CheckResult` changelog uses markdown for code elements
- `base.Component` changelog uses markdown for code elements
- `base.DataAttributes` changelog uses markdown for code elements
- `base.DataProvider` changelog uses markdown for code elements
- `base.Extensions` changelog uses markdown for code elements
- `base.Input` changelog uses markdown for code elements
- `base.InputContainer` changelog uses markdown for code elements
- `base.Module` changelog uses markdown for code elements
- `base.Observer` changelog uses markdown for code elements
- `base.Output` changelog uses markdown for code elements
- `base.OutputContainer` changelog uses markdown for code elements
- `base.Store` changelog uses markdown for code elements
- `base.Values` changelog uses markdown for code elements
- `components.CsvReader` changelog uses markdown for code elements
- `components.DeleteFolder` changelog uses markdown for code elements
- `components.DepositionToPecSoil` changelog uses markdown for code elements
- `attrib.Transformable` changelog uses markdown for code elements
- `components.DepositionToReach` changelog uses markdown for code elements
- `components.DoseResponse` changelog uses markdown for code elements
- `store.InMemoryStore` changelog uses markdown for code elements
- `store.SqlLiteStore` changelog uses markdown for code elements
- `store.X3fdStore` changelog uses markdown for code elements
- `components.ExportData` changelog uses markdown for code elements
- `components.ReportingHydrographicMap` changelog uses markdown for code elements
- `components.ReportingHydrographicMap` markdown usage extended
- `components.LandscapeScenarioPreparation` changelog uses markdown for code elements
- `components.MarsWeather` changelog uses markdown for code elements
- `components.PpmCalendar` changelog uses markdown for code elements
- `components.TerRQ` changelog uses markdown for code elements
- `components.UserParameters` changelog uses markdown for code elements
- `base.MCRun` changelog uses markdown for code elements
- `base.Project` changelog uses markdown for code elements
- `base.UserParameters` changelog uses markdown for code elements
- `base.Experiment` changelog uses markdown for code elements
- `base` changelog uses markdown for code elements
- `observer.ConsoleObserver` changelog uses markdown for code elements
- `observer.GraphMLObserver` changelog uses markdown for code elements
- `observer.LogFileObserver` changelog uses markdown for code elements
- `observer` changelog uses markdown for code elements

### Fixed
- `stores` changelog


## [1.5.2] - 2021-07-13

### Added

### Changed

### Fixed


## [1.5.1] - 2021-07-09

### Added
- `base.documentation` methods for documenting scenarios

### Changed
- small changes in `base.Output` changelog
- small changes in `components.CsvReader` changelog
- small changes in `components.MarsWeather` changelog
- small changes in `base.MCRun` changelog

### Fixed


## [1.5] - 2021-07-08

### Added
- properties `roadmap`, `authors` and `acknowledgements` to `base.VersionCollection` 
- `base.Input.description` 
- `base.Module.doc_file` 
- `base.Output` properties `default_attributes`, `description` and `attribute_hints` 
- `base.documentation` methods for documenting components

### Changed
- fixed spelling in `base.VersionCollection` 
- `base.Output` manages default attributes
- `base.Output` output description and hints for attribute descriptions
- usage of specified defaults if no attributes passed in a call to set values
- Iteration over `base.OutputContainer` now returns `Output` objects instead of their names
- `components.CsvReader` iterates over output objects instead of names
- `components.MarsWeather` iterates over output objects instead of names
- `base.MCRun` iterates over output objects instead of names

### Fixed


## [1.4.14] - 2021-07-06

### Added

### Changed
- added semantic descriptions to `EnvironmentalFate` component

### Fixed


## [1.4.13] - 2021-07-05

### Added

### Changed
- added physical units to `MarsWeather` outputs

### Fixed


## [1.4.12] - 2021-06-29

### Added
- `attrib.InList` attribute to check whether a value is within a set of allowed values

### Changed

### Fixed


## [1.4.11] - 2021-06-25

### Added

### Changed
- parsing of XML parameters strips whitespaces in `base.functions` 

### Fixed


## [1.4.10] - 2021-06-24

### Added

### Changed

### Fixed
- automatic documentation error


## [1.4.9] - 2021-06-24

### Added
- `document.py` 
- `base.documentation` 

### Changed
- `base` changelog uses markdown for code elements
- `init.py` spell check exclusions
- `base.functions` changelog uses markdown for code elements
- `components.DepositionToPecSoil` data type access
- `attrib.Class` changelog uses markdown for code elements
- `attrib.Equals` changelog uses markdown for code elements
- `attrib.Ontology` changelog uses markdown for code elements
- `attrib.Scales` changelog uses markdown for code elements
- `attrib.Unit` changelog uses markdown for code elements
- `attrib` changelog uses markdown for code elements
- `components.DepositionToReach` data type access
- `components.DoseResponse` data type access
- renamed `components.EnvironmentalFate` component
- `store.InMemoryStore` data type access
- `store.SqlLiteStore` data type access
- `store.X3dfStore` data type access
- `stores` changelog uses markdown for code elements
- `components.ExportData` data type access
- `components.ReportingHydrographicMap` changelog uses markdown for code elements
- renamed `components.HydrologyFromTimeSeries` component
- `components.LandscapeScenarioPreparation` spell check exclusion
- `components.LandscapeScenario` changelog uses markdown for code elements
- `components.TerRQ` data type access
- `components` imports updated to reflect renamed components
- `base.UserParameters` property names
- `base.UncertaintyAndSensitivityAnalysis` renamed
- `base.UncertaintyAndSensitivityAnalysis` renamed local variables
- `base` updated imports to changed class names

### Fixed


## [1.4.8] - 2021-02-03

### Added

### Changed

### Fixed
- `store.X3dfStore` conversion of MC identifier to integer


## [1.4.7] - 2021-02-03

### Added

### Changed

### Fixed
- `components.LandscapeScenario` added path to proj.db zo fix errors on some systems


## [1.4.6] - 2021-01-19

### Added

### Changed
- `store.X3dfStore` `identifier` argument of initializer
- `store.X3dfStore` parent run no longer randomly sampled
- New system macro `_MC_ID_` 

### Fixed


## [1.4.5] - 2012-12-29

### Added
- `base.functions.reporting()` 
- `components.ReportingHydrographicMap.draw()` static method
- `components.ReportingHydrographicMap.draw()` static method

### Changed
- `components.ReportingHydrographicMap.__init__` `observer` argument renamed

### Fixed
- `components.ExportData` spelling error in inline documentation
- `components.ReportingDistribution` spelling error in documentation


## [1.4.4] - 2012-12-15

### Added
- `components.DeleteFolder` component

### Changed
- `store.SqlLiteStore` manages chunks

### Fixed


## [1.4.3] - 2020-12-14

### Added
- `store.SqlLiteStore.execute()` method
- `components.ExportData` component

### Changed
- `base.functions.convert()` can evaluate values
- `store.SqlLiteStore` got `create` argument for extending existing datasets
- `store.SqlLiteStore.set_values()` can add foreign keys
- `store.SqlLiteStore` manages physical units

### Fixed
- `store.SqlLiteStore` can use existing directory
- `store.SqlLiteStore` uses new version system


## [1.4.2] - 2020-12-07

### Added
- Corrections in `README` 

### Changed
- Changelog description
- Changelog description
- Changelog description
- Changelog description
- Changelog description
- Changelog description
- new `components.HydrologyFromTimeSeries` inputs InflowTimeSeriesPath, ImportInflows
- new `components.HydrologyFromTimeSeries` outputs InflowReaches and Inflow
- `components.HydrologyFromTimeSeries` (optionally) reads inflows from fields
- Changelog description
- `base.McRun` changelog description
- Changelog description

### Fixed


## [1.4.1] - 2020-12-03

### Added
- Changelog in `base.VERSION` 
- `base.VersionCollection` for managing revision history
- Changelog in `base.CheckResult`
- Changelog in `base.Component`
- Changelog in `base.DataAttributes`
- Changelog in `base.DataProvider`
- Changelog in `base.Extensions` 
- Changelog in `base.functions` 
- Changelog in `base.Input`
- Changelog in `base.InputContainer` 
- Changelog in `base.Module` 
- Changelog in `base.Observer` 
- Changelog in `base.Output` 
- Changelog in `base.OutputContainer`
- Changelog in `base.Store` 
- Changelog in `base.Values` 
- Changelog in `components.CsvReader` 
- Changelog in `components.DepositionToPecSoil` 
- Changelog in class `attrib.Class` 
- Changelog in class `attrib.Equals` 
- Changelog in class `attrib.Ontology`
- Changelog in class `attrib.Scales` 
- Changelog in `attrib.Transformable`
- Changelog in class `attrib.Unit` 
- Changelog in `attrib` 
- Changelog in `components.DepositionToReach`
- Changelog in `components.DoseResponse`
- Changelog in `components.EnvironmentalFate`
- Changelog in `store.InMemoryStore` 
- Changelog in `store.SqlLiteStore`
- s`tore.SqlLiteStore.has_dataset()` 
- Changelog in `store.X3dfStore` 
- Changelog in `stores` 
- Changelog in `components.ReportingDistribution` 
- `components.ReportingDistribution` class documentation
- Changelog in `components.ReportingHydrographicMap`
- Changelog in `components.HydrologyFromTimeSeries` 
- Changelog in `components.LandscapeScenarioPreparation` 
- Changelog in `components.LandscapeScenario` 
- Changelog in `components.MarsWeather` 
- Changelog in `components.PpmCalendar` 
- Changelog in `components.TerRQ` 
- `components.TerRQ` class documentation
- Changelog in `components.UserParameters` 
- Changelog in `components` 
- Changelog in `base.MCRun` 
- Changelog in `base.Project` 
- `base.Project.version` 
- Changelog in `base.UserParameters` 
- Changelog in `base.Experiment` 
- Changelog in `base.UncertaintyAndSensitivityAnalysis` 
- Changelog in `base.__init__`
- Changelog in `observer.ConsoleObserver` 
- Changelog in `observer.GraphMLObserver` 
- Changelog in `observer.LogFileObserver` 
- Changelog in `observer.__init__` 

### Changed
- Changed `base.VERSION` to a `base.VersionCollection`, tracking changes in classes
- `base.VersionInfo` completely rewritten to move changelogs nearer to code
- `components.CsvReader` class documentation
- `components.DepositionToPecSoil` class documentation
- Removed unused output `PecSoil 2` from `components.DepositionToPecSoil` 
- Removed class `attrib.VERSION` 
- `components.DepositionToReach` class documentation
- `components.DoseResponse` class documentation
- `components.EnvironmentalFate` class documentation
- `store.InMemoryStore` class documentation
- `store.SqlLiteStore` has now `base.Store` as superclass
- `store.SqlLiteStore` class documentation
- `store.X3dfStore` class documentation
- Removed `stores.VERSION` 
- `components.ReportingHydrographicMap` class documentation
- `components.HydrologyFromTimeSeries` class documentation
- `components.LandscapeScenarioPreparation` class documentation
- `components.LandscapeScenario` class documentation
- `components.MarsWeather` class documentation
- `components.PpmCalendar` class documentation
- `components.UserParameters` class documentation
- Removed `components.VERSION` 
- `base.Experiment.write_info_xml()` uses new `Version` classes
- `observer.ConsoleObserver` class documentation
- `observer.GraphMLObserver` class documentation
- `observer.LogFileObserver` class documentation
- `Removed observer.VERSION` 

### Fixed
- `base.functions.observers_from_xml()` passes lock argument only if needed by observer
- `components.DoseResponse` attrib namespace reference
- `components.TerRQ` attrib namespace reference


## [1.4] - 2020-10-23

### Added
- `components.DoseResponse` component
- `components.ReportingDistribution` component
- `components.ReportingHydrographicMap` component
- `components.TerRQ` component

### Changed
- `components.CascadeToxswa` repackaged as external part
- `components.CmfContinuous` repackaged as external part
- `components.LEffectModel` repackaged as external part
- `components.LP50` repackaged as external part
- `components.RunOffPrzm` repackaged as external part
- `components.StepsRiverNetwork` repackaged as external part
- `components.StreamCom` repackaged as external part
- `components.XSprayDrift` repackaged as external part
- `observer.AnalysisObserver` repackaged as external part
- `observer.ReportingObserver` repackaged as external part

### Fixed


## [1.3.35] - 2020-08-12

### Added
- `base.Store.has_dataset()` to check whether store contains specific data
- `store.X3dfStore.has_dataset()` 

### Changed
- `base.functions.run_process()` manages system environment variables
- `store.X3dfStore` can be initialized using existing data
- `components.MarsWeather` no longer uses a provisional output container
- `base.MCRun` can continue previous simulations
- `base.UncertaintyAndSensitivityAnalysis.create()` regex refactored

### Fixed
- `base.functions.replace_tokens()` treats None values as empty string


## [1.3.34] - 2020-08-04

### Added
- Additional unit conversions in class `attrib.Unit`

### Changed

### Fixed


## [1.3.33] - 2020-07-30

### Added
- `base.DataAttributes.append()` for dynamically adding data attributes
- Quick access to metadata by `base.Values.unit` and `base.Values.scales` 
- `attrib.Class` support of list[bytes], list[float], list[str] and tuple[float]
- Scale attribute checker
- `components.UserParameters.unit` 

### Changed
- `base.Component` refactored
- `base.DataAttributes` refactored
- `base.Extensions` refactored
- `base.Input.read()` passes metadata from provider to `base.Values` object
- `base.InputContainer` refactored
- `components.CsvReader` refactored
- `attrib.Class.check()` returns base.CheckResult instead of tuple
- `attrib.Equals.check()` returns base.CheckResult instead of tuple
- `attrib.Equals` refactored
- `attrib.Ontology.check()` returns base.CheckResult instead of tuple
- `attrib.Transformable.check()` returns base.CheckResult instead of tuple
- `attrib.Unit.check()` returns base.CheckResult instead of tuple
- `components.DepositionToReach` checks input types strictly
- `components.DepositionToReach` checks for physical units
- `components.DepositionToReach` reports physical units to the data store
- `components.DepositionToReach` checks for scales
- `store.InMemoryStore` stores physical unit if specified
- `store.X3dfStore` no longer casts `list[bytes]` to bytes
- `store.X3dfStore` can store and read lists of strings
- `store.X3dfStore` is explicit about its parameters
- `store.X3dfStore` stores physical unit if specified
- `store.X3dfStore.describe()` outputs scales
- `components.HydrologyFromTimeSeries` checks input types strictly
- `components.HydrologyFromTimeSeries` checks for physical units
- `components.HydrologyFromTimeSeries` reports physical units to the data store
- `components.HydrologyFromTimeSeries` checks for scales
- `components.LandscapeScenario` checks input types strictly
- `components.LandscapeScenario` checks for physical units
- `components.LandscapeScenario` reports physical units to the data store
- `components.LandscapeScenario` checks for scales
- `components.MarsWeather` checks input types strictly
- `components.MarsWeather` checks for physical units
- `components.MarsWeather` reports physical unit of average temperature to data store
- `components.MarsWeather` checks for scales
- `components.PpmCalendar` checks input types strictly
- `components.PpmCalendar` checks for physical units
- `components.PpmCalendar` reports physical units to the data store
- `components.PpmCalendar` checks for scales
- `components.UserParameters` reports physical units to the data store
- `observer.GraphMLObserver` refactored

### Fixed
- `base.functions.convert()` crashes with empty lists


## [1.3.29] - 2020-06-15

### Added

### Changed
- `components.LandscapeScenarioPreparation` can calculate flow grids from DEM

### Fixed
- Input slicing in `components.DepositionToPecSoil` 


## [1.3.28] - 2020-06-03

### Added
- `base.Store` class for representing Landscape Model stores
- `components.LandscapeScenarioPreparation` component

### Changed

### Fixed


## [1.3.27] - 2020-05-20

### Added
- `store.SqlLiteStore` 

### Changed
- `base.VersionInfo` refactored
- `components.DepositionToPecSoil` refactored
- Soil depth is now parameter in `components.DepositionToPecSoil` 
- `components.DepositionToReach` specifies scales
- `components.EnvironmentalFate` refactored
- `store.InMemoryStore` `slice` keyword renamed to `slices`
- `store.InMemoryStore` updated
- `store.X3dfStore` acknowledges `scales` keyword for all value types
- `store.X3dfStore` `default` keyword added
- `store.X3dfStore` `slice` keyword renamed to `slices` 
- `components.LandscapeScenario` specifies scales
- `components.MarsWeather` specifies scales
- `components.PpmCalendar` specifies scales
- `components.UserParameters` specifies scales
- `components.UserParameters` expects list of `UserParameters` as values
- `base.MCRun` parses user-defined parameter scales
- `base.UserParameters` refactored
- `base.UncertaintyAndSensitivityAnalysis` refactored

### Fixed


## [1.3.24] - 2020-04-02

### Added
- `base.functions.run_process()` for invoking system processes
- Added `base.Observer.flush()` and `base.Observer.write()` to use observers as streams
- Added `observer.ConsoleObserver.flush()` and `observer.ConsoleObserver.write()` 
- Added `observer.GraphMLObserver.flush()` and `observer.GraphMLObserver.write()` 
- `observer.LogFileObserver` 

### Changed
- `base.Experiment` sets standard and error output to default observer
- `observer.ConsoleObserver` refactored

### Fixed
- `base.functions.chunkSlices()` determining chunk size when dimensions have the same extent


## [1.3.22] - 2020-03-27

### Added

### Changed
- More explanatory error messages in `components.HydrologyFromTimeSeries` 

### Fixed


## [1.3.21] - 2020-03-26

### Added
- `base.OutputContainer.append()` for dynamically adding outputs

### Changed

### Fixed


## [1.3.20] - 2020-03-23

### Added

### Changed
- `base.functions.observers_from_xml()` enables/disables observers also through expression
- `base.functions.convert()` separator of list[str] parameters changed to |
- `base.MCRun` can be enabled/disabled also through expression in configuration

### Fixed


## [1.3.13] - 2020-02-07

### Added

### Changed
- `base.DataProvider` refactored
- Option to disable observers in configuration by `base.functions.observers_from_xml()` 
- `base.Input` refactored
- `base.Output` refactored

### Fixed


## [1.3.5] - 2020-01-08

### Added

### Changed
- `base.CheckResult` refactored
- `base.functions.replaceTokens()` replaces $$-tokens before $-tokens
- `base.functions `refactored
- `base.Module` refactored
- `base.Observer` refactored
- `base.OutputContainer` refactored
- `base.Values` refactored
- `base.MCRun` refactored
- `base.Project` refactored
- `base.Experiment` refactored
- `base.Experiment` project encapsulation and support of versions
- `base.__init__` refactored

### Fixed


## [1.3.3] - 2019-12-15

### Added
- Unit attribute class to check and convert physical units (currently hard-coded)

### Changed

### Fixed


## [1.3.2] - 2019-12-10

### Added

### Changed
- Enforce strict checks in `components.LandscapeScenario` 

### Fixed


## [1.2.40] - 2019-11-21

### Added
- `components.MarsWeather` component

### Changed

### Fixed


## [1.2.37]

### Added
- Ontology attribute checker

### Changed
- Specified X3df file mode in `store.X3dfStore` 
- Ability to open X3df in different modes in `store.X3dfStore` 
- `store.X3dfStore` refactored

### Fixed


## [1.2.36]

### Added

### Changed
- `components.HydrologyFromTimeSeries` provides water body volume and wet surface area
- `components.HydrologyFromTimeSeries` allows specifying time frame

### Fixed


## [1.2.35]

### Added

### Changed
- Class checks in `components.LandscapeScenario` 

### Fixed
- `base.UncertaintyAndSensitivityAnalysis.create()` function parsing improved


## [1.2.34]

### Added

### Changed
- Better exceptions in `components.LandscapeScenario` 

### Fixed


## [1.2.31]

### Added

### Changed
- init script recursive to run entire folders
- `base.UncertaintyAndSensitivityAnalysis.create()` parameter generation possible in sub-directories
- `base.UncertaintyAndSensitivityAnalysis.create()` can process pre-defined lists

### Fixed


## [1.2.28]

### Added

### Changed
- `components.DepositionToReach` outputs reach identifiers
- `components.HydrologyFromTimeSeries` no longer depends on hydrography input

### Fixed


## [1.2.27]

### Added

### Changed
- `ProbabilityFieldApplied` introduced in `components.PpmCalendar` 

### Fixed


## [1.2.25]

### Added

### Changed
- Support of `NoneType` in `store.X3dfStore`
- components.PpmCalendar`.RandomSeed` parameter

### Fixed


## [1.2.20]

### Added
- `components.HydrologyFromTimeSeries` component

### Changed
- `components.DepositionToReach` basic implementation
- Support of dates and times in `store.X3dfStore` 
- `components.LandscapeScenario` distinguishes between supplementary data formats
- `components.LandscapeScenario` can import additional attributes from base geometry shapefile
- `components.PpmCalendar` no longer outputs SprayApplication objects

### Fixed


## [1.2.19]

### Added

### Changed
- `components.LandscapeScenario` ROI extent as meta-datum in package info file

### Fixed


## [1.2.18]

### Added

### Changed
- `components.LandscapeScenario` has new input XML schema and checks layer consistency

### Fixed


## [1.2.17]

### Added
- `base.UncertaintyAndSensitivityAnalysis` class for managing uncertainty and sensitivity analyses

### Changed
- `base.functions.replaceTokens()` accepts non-string values
- `base.UserParameters` understand uncertainty / sensitivity analysis XML attribute
- `base.Experiment` has new macro `_PARAM_DIR_` 
- `base.Experiment` is more flexible in parameter directory

### Fixed


## [1.2.16]

### Added

### Changed
- Slicing enabled for `list[byte]` in `store.X3dfStore`
- `components.PpmCalendar` output refactored

### Fixed


## [1.2.14]

### Added

### Changed

### Fixed
- wrong calculation in `components.DepositionToPecSoil` 


## [1.2.13]

### Added

### Changed
- further implementation of `observer.GraphMLObserver` 

### Fixed


## [1.2.12]

### Added
- `base.Observer.mc_run_started()` for messages about newly started Monte Carlo runs
- `observer.ConsoleObserver.mc_run_started()` 
- `observer.GraphMLObserver` 

### Changed
- `base.MCRun.run()` signals MC run start to observer

### Fixed


## [1.2.7]

### Added

### Changed

### Fixed


## [1.2.6]

### Added

### Changed
- `components.LandscapeScenario` provides absolute paths for directories also

### Fixed


## [1.2.5]

### Added

### Changed
- `components.LandscapeScenario` can provide flexible set of outputs
- `components.PpmCalendar` target land-use / land-cover type input now str

### Fixed


## [1.2.4]

### Added

### Changed

### Fixed


## [1.2.3]

### Added
- Added `base.InputContainer.append()` and `.__contains__()` 
- `components.DepositionToReach` component stub

### Changed

### Fixed
- `base.functions.chunkSlices()` indexing


## [1.2.2]

### Added

### Changed
- `store.X3dfStore` now handles boolean values separately

### Fixed


## [1.2.1]

### Added
- `attrib.Class` checker support of list[int] type
- `base.Project` class for representing Landscape Model scenarios

### Changed
- `base.functions.replaceTokens()` allows macros in source path
- `base.Experiment` expects a global section in the Monte Carlo run configuration
- `base.Experiment` has new macro `_X3DIR_` 

### Fixed


## [1.1.6]

### Added
- `base.VERSION` for describing code changes
- `base.VersionInfo` for describing individual revisions
- Value equality checker
- Changelog through `VersionInfo` class in `attrib` namespace
- Changelog through `VersionInfo` class in `stores` namespace
- Changelog through `VersionInfo` class in `components` namespace
- `base.Experiment.write_info_xml()` for saving runtime information of the experiment
- Changelog through `VersionInfo` class in `base` namespace
- Changelog through `VersionInfo` class in `observer` namespace

### Changed

### Fixed


## [1.1.5]

### Added

### Changed
- `components.DepositionToPecSoil` reports scale information of output to data store
- `components.DepositionToPecSoil` requests storing of maximum value of PEC soil
- `components.EnvironmentalFate` stores metadata of PEC
- `store.X3dfStore` scale information for numpy arrays if provided
- `store.X3dfStore` can calculate maximum for numpy arrays

### Fixed


## [1.1.2]

### Added

### Changed
- `components.EnvironmentalFate` exposure inputs made optional
- `base.MCRun` allows disabling components in configuration
- `base.MCRun` allows disabling links between inputs and outputs

### Fixed


## [1.1.1]

### Added
- `base.CheckResult` class for exchanging observer messages
- `base.Component` class representing Landscape Model components
- `base.DataAttributes` class as a data attribute container
- `base.DataProvider` class for data providers
- `base.Extensions` class as a container for data extensions
- `base.functions` providing helper functions
- `base.Input` class for representing component inputs
- `base.InputContainer` class for collecting the inputs of a component
- `base.Module` class for describing Landscape Model modules
- `base.Observer` class for representing Landscape Model observers
- `base.Output` class for representing component outputs
- `base.OutputContainer` class for collecting outputs of a component
- `base.Values class` for exchanged data values
- `components.CsvReader` component
- `components.DepositionToPecSoil` component
- `attrib.Class` 
- `Transformable` attribute checker
- `attrib` namespace
- `components.EnvironmentalFate` component
- `store.InMemoryStore` 
- `store.X3dfStore` 
- `stores` namespace
- `components.LandscapeScenario` component
- `components.PpmCalendar` component
- `components.UserParameters` component
- `components` namespace
- `base.MCRun` class for managing individual Monte Carlo runs
- `base.UserParameters` class for user-defined parameters
- `base.Experiment` class for managing individual experiments
- `base` namespace
- `observer.ConsoleObserver` 
- `observer` namespace

### Changed
- `components.PpmCalendar` now requires Fields and land-use / land-cover type inputs to be of type list[int]

### Fixed
