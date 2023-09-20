# Changelog

This is the changelog for the Landscape Model core. It was automatically created on 2023-09-20.

## [1.15.9] - 2023-09-20

### Added

- Output `Deposition` of `DepositionToReach` component now also reports reach geometries

- Logic to postpone creation of reference links in `X3dfStore` if needed

- `Hydrography` input to `HydrologyFromTimeSeries` component

### Changed

- Extended Deposition output description of `DepositionToReach` component

- Extended output descriptions of `HydrologyFromTimeSeries` component

- Outputs of `HydrologyFromTimeSeries` component now report reach geometries

- Documentation of outputs for components in core and external components now uses the same code

### Fixed

## [1.15.8] - 2023-09-19

### Added

- Possibility to skip initial attribute checks for `base.Output`

- Documentation of outputs in `HydrologyFromTimeSeries` component

- Documentation of outputs in `MarsWeather` component

- Documentation of outputs in `PpmCalendar` component

- Documentation of outputs in `WaterTemperatureFromAirTemperature` component

- Documentation of outputs for components in core

### Changed

- Changed `space/reach` to a named geometries scale in `X3dfStore`

- Removed ProvisionalOutputs from `ExportData` component

- Target outputs for export in `ExportData` component no longer check attributes

### Fixed

## [1.15.7] - 2023-09-18

### Added

### Changed

- Adapted scenario XML schema to allow `outsourced` XML attribute

- File encoding for reading and writing using the `replace_tokens` function is now UTF-8

### Fixed

## [1.15.6] - 2023-09-18

### Added

- Message to writing of info XML in Experiment regarding un-checked scenario modules

- Input descriptions to `DepositionToReach` component

- Input descriptions to `ExportData` component

- Input descriptions to `HydrologyFromTimeSeries` component

- Input descriptions to `LandscapeScenario` component

- Input descriptions to `MarsWeather` component

- Input descriptions to `PpmCalendar` component

- Input descriptions to `WaterTemperatureFromAirTemperature` component

- User warning regarding non-documented modules during scenario documentation

### Changed

- Updated description of `DepositionToReach` component

- Changed `other/application`, `other/runs` and `other/soil_horizon` to named scales in `XdfStore`

- Removed `space/reach2` as recognized scale from `X3dfStore`

- Updated description of `ExportData` component

- Updated description of `HydrologyFromTimeSeries` component

- Updated description of `LandscapeScenario` component

- Updated description of `MarsWeather` component

- Updated description of `PpmCalendar` component

- Updated description of `WaterTemperatureFromAirTemperature` component

- Updated installation notes in model documentation

### Fixed

## [1.15.5] - 2023-09-14

### Added

- Usage of a fixed path for the versions.json during documentation

### Changed

- Updated scenario XML-schema to optionally include ExternalSources and Acknowledgements

- Made order of elements within scenario XML version changelog arbitrary

- Raise clearer error message if scenario XML does not use the right XML namespace

### Fixed

- Errors when scenario was not tested with current model

## [1.15.4] - 2023-09-14

### Added

### Changed

- String representations of `attrib.Class` is now more readable

- String representations of `attrib.Equals` is now more readable

- String representations of `attrib.Scales` is now more readable

- String representations of `attrib.Transformable` is now more readable

- String representations of `attrib.Unit` is now more readable

- Order of arguments in `UserParameters` component now follows `base.Component` class

- Order of arguments in `UserParameters` component now follows `base.Component` class

- Order of arguments in `UserParameters` component now follows `base.Component` class

- Documentation of core components lists component's inputs and their attributes

### Fixed

## [1.15.3] - 2023-09-13

### Added

- Added option to skip initial attribute checks of a `base.Input`

### Changed

### Fixed

## [1.15.2] - 2023-09-12

### Added

- Creation of repository info during documentation

- Repository info to Python runtime environment

- `external` and `changelog` properties to `base.Module`

### Changed

- Relieved repository checks for external modules

- Extended module information for Python runtime environment

### Fixed

- Fixed resolution of git-paths of submodules

## [1.15.1] - 2023-09-11

### Added

### Changed

- Included types in `DepositionToReach` input attributes

- Skip initial attribute checks for `Values` input of `ExportData` component

- Added scale attribute to `FilePath` input of `MarsWeather` component

### Fixed

- Documentation of scenario respects XML namespace

## [1.15] - 2023-09-11

### Added

- `frontmatter` package to runtime environment

- Scenario XML schema

- Messages if `base.Output` misses descriptions

- Messages if `base.Input` misses attributes

- `base.Module` now allows nesting of modules

- `base.MultiObserver` remembers whether errors, warnings and notes were written during simulation run

- Repository checks during initialization of `base.Experiment` 

- Added message for initialization of component in `base.MCRun`

- XML validation of scenario metadata

- Runtime environment information of core in `base.__init__`

- Functions to check variant parts and to write repository info for documentation

### Changed

- Updated `GDAL` to version 3.4.3

### Fixed

## [1.14.4] - 2023-07-26

### Added

### Changed

- Changed chunk size for lists in `stores.X3dfStore`

### Fixed

- Fixed dimensionality of `Deposition` output in `components.DepositionToReach` component

- Fixed dimensionality of `Deposition` output in `components.HydrologyFromTimeSeries` component

## [1.14.3] - 2023-07-26

### Added

### Changed

- Normalized whitespace for creating documentations

### Fixed

## [1.14.2] - 2023-03-17

### Added

### Changed

### Fixed

## [1.14.1] - 2023-03-17

### Added

### Changed

### Fixed

## [1.14] - 2022-03-25

### Added

- Python packages Shapely and openpyxl to runtime environment

- class `base.ExistingValues` for referencing values already stored

- `components.BeeHave` 

- `components.LandCoverToVegetation` 

- default mappings for land cover to vegetation and vegetation to bee forage

- default dictionary for vegetation classes

### Changed

- `base.Values` now manages geometries of elements

- `attrib.Unit` keeps additional value attributes (offsets and geometries) during conversion

- `stores.X3dfStore` now stores and retrieves geometries of elements

- `components.LandscapeScenario` reports geometries of values also as value attributes

### Fixed

## [1.13.1] - 2022-03-11

### Added

### Changed

- Text wrapping of member documentation in `base.documentation` 

### Fixed

## [1.13] - 2022-03-08

### Added

- Offset property to `base.Values` 

- `stores.X3dfStore` functionality to reference scale 'time/day' with native coordinates

- `components.WaterTemperatureFromAirTemperature` component

### Changed

- `components.MarsWeather` now stores entire timeseries, regardless of simulation period

- Allowed more spellings for enabling/disabling components in `base.MCRun` 

### Fixed

- Spelling error in `base.documentation` 

## [1.12.6] - 2022-03-03

### Added

### Changed

- Updated numpy package to version 1.22.2

- Mitigated weak code warnings in `base.functions` 

- Mitigated weak code warning in `stores.SqlLiteStore` 

- Mitigated weak code warning in `components.LandscapeScenarioPreparation` 

- Refactored documentation of class members into own function in `base.documentation` 

- Mitigated weak code warning in `observer.GraphMLObserver` 

### Fixed

## [1.12.5] - 2022-01-12

### Added

### Changed

- Perform XML schema validation in `components.LandscapeScenario` 

- Enhanced contribution documentation in `base.documentation` 

### Fixed

## [1.12.4] - 2022-01-11

### Added

### Changed

- Increased encapsulation of Jupyter notebook in `init.py` 

- Order of exposure input scales in `components.DoseResponse` 

- `components.DoseResponse` reports offsets of output

- Division warning suppressed in `components.DoseResponse`

- Order of exposure input scales in `components.TerRQ` 

- `components.TerRQ` reports offsets of output

### Fixed

## [1.12.3] - 2022-01-05

### Added

- xmlschema package to Python runtime environment

- XML validation to `base.UserParameters` 

### Changed

- `base.UserParameters` handles XML namespaces

### Fixed

- Removed warning for unused deposition from file `components.DepositionToReach` if path is specified

## [1.12.2] - 2022-01-04

### Added

- Automatic creation of CONTRIBUTING.md in `document.py` 

- Step to merge request instructions in `base.documentation` 

### Changed

- Fixed typos in `stores.X3dfStore` documentation

### Fixed

- Typos in `base.documentation` 

## [1.12.1] - 2022-01-04

### Added

### Changed

- Extended CONTRIBUTING.md in `base.documentation` 

### Fixed

## [1.12] - 2021-12-30

### Added

### Changed

- `components.DepositionToPecSoil` output scale order

- `components.DepositionToPecSoil` reports offset

- `components.EnvironmentalFate` output scale order

- `components.EnvironmentalFate` reports offset

- `stores.X3dfStore` recognizes square-meter scales for offset description

- `components.LandscapeScenario` output scale order

- `components.LandscapeScenario` reports offset

### Fixed

## [1.11] - 2021-12-10

### Added

### Changed

- `components.DepositionToReach` allows predefining deposition in a CSV file

- `stores.X3dfStore` manages storage of offsets

- `components.HydrologyFromTimeSeries` specifies offsets of outputs

- `components.MarsWeather` specifies offsets of outputs

### Fixed

## [1.10.5] - 2021-12-09

### Added

- Handling of covered reaches to `components.DepositionToReach` 

### Changed

- Removed superfluous warning message from `stores.SqlLiteStore` 

### Fixed

## [1.10.4] - 2021-12-08

### Added

### Changed

- Added additional consistency check to `components.LandscapeScenario` 

### Fixed

## [1.10.3] - 2021-12-07

### Added

- Further consistency checks to `HydrologyFromTimeSeries` component

### Changed

- Spell checking in `README` 

- Spell checking in `base.UserParameters` 

- Spell checking in `base.UncertaintyAndSensitivityAnalysis` 

- Spell checking in `base.documentation` 

- Spell checking in `observer.ConsoleObserver` 

### Fixed

## [1.10.2] - 2021-11-29

### Added

### Changed

- Changed generation of index numbers in `stores.SqlLiteStore` to considerably reduce memory usage

### Fixed

## [1.10.1] - 2021-11-29

### Added

### Changed

- `stores.X3dfStore` recognizes additional scales

### Fixed

## [1.10] - 2021-11-18

### Added

- `base.Values` have element names now

- `components.UserParameters` have element names now

- XML-tag for element names in `base.MCRun` configurations

### Changed

- `base.Values` switched to Google-style docstrings

- `attrib.Unit` keeps element names for converted values

- `components.DepositionToReach` reports element names of `Deposition` output

- `components.DepositionToReach` switched to Google-style docstrings

- `stores.X3dfStore` now manages element names for some scales

- `components.HydrologyFromTimeSeries` reports global scale of time span outputs

- `components.HydrologyFromTimeSeries` reports element names of outputs

- `components.LandscapeScenario` reports global scale of metadata outputs

- `components.LandscapeScenario` gained semantics for element identifier attribute

- `components.UserParameters` switched to Google-style docstrings

### Fixed

## [1.9.12] - 2021-11-16

### Added

### Changed

### Fixed

## [1.9.11] - 2021-11-08

### Added

### Changed

- `observer.ConsoleObserver` flushes buffer after every write

- `observer.LogFileObserver` flushes buffer after every write

### Fixed

- Processing of exceptions thrown in non-blocking mode in `base.Experiment` 

## [1.9.10] - 2021-11-05

### Added

### Changed

- `base.Project` can handle outsourced package parts

### Fixed

- `mistune` package downgraded to make Jupyter notebook accessible again

## [1.9.9] - 2021-11-02

### Added

- Option to profile performance of simulation runs in `base.Experiment` 

### Changed

- `observer.LogFileObserver` now uses line-end buffering

### Fixed

## [1.9.8] - 2021-10-27

### Added

### Changed

- Switching of buffering of Python instances called by `functions.run_process` 

### Fixed

## [1.9.7] - 2021-10-26

### Added

### Changed

### Fixed

## [1.9.6] - 2021-10-22

### Added

- Function for template-based documentation of model variants to `base.documentation` 

### Changed

- Replaced GDAL constants by numerical values in `components.LandscapeScenarioPreparation` 

- updated docstring of `ConsoleObserver.__init__` 

### Fixed

## [1.9.5] - 2021-10-21

### Added

- `observer.ConsoleObserver` parameter for less verbose output

- `observer.LogFileObserver` parameter for less verbose output

### Changed

### Fixed

## [1.9.4] - 2021-10-20

### Added

- Some runtime environment files

### Changed

- `attrib.InList` can now check all items in a sequence

### Fixed

- Corrupted runtime environment files

## [1.9.3] - 2021-10-19

### Added

### Changed

### Fixed

- Formatting of generated scenario documentation in `base.documentation` 

## [1.9.2] - 2021-10-18

### Added

- `components.LandscapeScenario` output of base layer EPSG code

### Changed

### Fixed

## [1.9.1] - 2021-10-15

### Added

- Arguments to `documentation.document_variant` to specify variant name and endpoint flexibly

### Changed

- New macro `_MODEL_DIR_` in `base.Experiment` 

- Check if module R instances are sufficiently encapsulated in `base.functions.run_process()` 

### Fixed

## [1.9] - 2021-10-12

### Added

### Changed

- Switched to Google docstring style in `base.VersionCollection` 

- Switched to Google docstring style in `base.VersionInfo` 

- Switched to Google docstring style in `init.py` 

- Switched to Google docstring style in `base.Extension` 

- Switched to Google docstring style in `base.DataAttribute` 

- Switched to Google docstring style in `base.DataAttributes` 

- Switched to Google docstring style in `base.Store` 

- Switched to Google docstring style in `base.Output` 

- Switched to Google docstring style in `base.OutputContainer` 

- Switched to Google docstring style in `base.DataProvider` 

- Switched to Google docstring style in `attrib.Class` 

- Switched to Google docstring style in `attrib.Equals` 

- Switched to Google docstring style in `attrib.InList` 

- Switched to Google docstring style in `attrib.Ontology` 

- Switched to Google docstring style in `attrib.Scales` 

- Switched to Google docstring style in `attrib.Transformable` 

- Switched to Google docstring style in `attrib.Unit` 

- Switched to Google docstring style in `base.Input` 

- Switched to Google docstring style in `base.InputContainer` 

- Switched to Google docstring style in `base.Observer` 

- Switched to Google docstring style in `base.Component` 

- Switched to Google docstring style in `base.Experiment` 

- Switched to Google docstring style in `base.functions` 

- Switched to Google docstring style in `component.CsvReader` 

- Switched to Google docstring style in `component.DepositionToPecSoil` 

- Switched to Google docstring style in `stores.InMemoryStore` 

- Switched to Google docstring style in `stores.SqlLiteStore` 

- Switched to Google docstring style in `stores.X3dfStore` 

- Switched to Google docstring style in `stores.__init__` 

- Switched to Google docstring style in `component.ReportingDistribution` 

- Switched to Google docstring style in `component.ReportingHydrographicMap` 

- Switched to Google docstring style in `component.HydrologyFromTimeSeries` 

- Switched to Google docstring style in `component.LandscapeScenario` 

- Switched to Google docstring style in `component.MarsWeather` 

- Switched to Google docstring style in `component.PpmCalendar` 

- Switched to Google docstring style in `component.__init__` 

- Switched to Google docstring style in `base.documentation` 

- Switched to Google docstring style in `observer.ConsoleObserver` 

- Switched to Google docstring style in `observer.GraphMLObserver` 

- Switched to Google docstring style in `observer.LogFileObserver` 

### Fixed

## [1.8] - 2021-10-11

### Added

### Changed

- Replaced Legacy format strings by f-strings in `base.VersionCollection` 

- Replaced Legacy format strings by f-strings in `init.py` 

- Replaced Legacy format strings by f-strings in `base.Output` 

- Replaced Legacy format strings by f-strings in `base.OutputContainer` 

- Replaced Legacy format strings by f-strings in `attrib.Class` 

- Replaced Legacy format strings by f-strings in `attrib.Equals` 

- Replaced Legacy format strings by f-strings in `attrib.InList` 

- Replaced Legacy format strings by f-strings in `attrib.Scales` 

- Replaced Legacy format strings by f-strings in `attrib.Unit` 

- Replaced Legacy format strings by f-strings in `base.Input` 

- Replaced Legacy format strings by f-strings in `base.InputContainer` 

- Replaced Legacy format strings by f-strings in `base.Experiment` 

- Replaced Legacy format strings by f-strings in `base.functions` 

- Replaced Legacy format strings by f-strings in `components.DepositionToReach` 

- Replaced Legacy format strings by f-strings in `stores.InMemoryStore` 

- Replaced Legacy format strings by f-strings in `stores.SqlLiteStore` 

- Replaced Legacy format strings by f-strings in `stores.X3dfStore` 

- Replaced Legacy format strings by f-strings in `components.ExportData` 

- Replaced Legacy format strings by f-strings in `components.ReportingHydrographicMap` 

- Replaced Legacy format strings by f-strings in `components.HydrologyFromTimeSeries` 

- Replaced Legacy format strings by f-strings in `components.LandscapeScenarioPreparation` 

- Replaced Legacy format strings by f-strings in `components.LandscapeScenario` 

- Replaced Legacy format strings by f-strings in `components.MarsWeather` 

- Replaced Legacy format strings by f-strings in `components.PpmCalendar` 

- Replaced Legacy format strings by f-strings in `base.MCRun` 

- Replaced Legacy format strings by f-strings in `base.UncertaintyAndSensitivityAnalysis` 

- Replaced Legacy format strings by f-strings in `base.documentation` 

- Replaced Legacy format strings by f-strings in `observer.ConsoleObserver` 

- Replaced Legacy format strings by f-strings in `observer.GraphMLObserver` 

- Replaced Legacy format strings by f-strings in `observer.LogFileObserver` 

### Fixed

## [1.7] - 2021-09-17

### Added

- Type hints to `base.VERSION` 

- Type hints to `base.VersionCollection` 

- Type hints to `base.VersionInfo` 

- Type hints to `init.py` 

- `base.Extension` class

- Type hints to `base.Extensions` 

- Type hints to `base.Values` 

- Type hints to `base.CheckResults` 

- `base.DataAttribute` class

- Type hints to `base.DataAttributes` 

- Type hints to `base.Store` 

- Type hints to `base.Output` 

- Type hints to `base.OutputContainer` 

- Type hints to `base.DataProvider` 

- Type hints to `attrib.Class` 

- Type hints to `attrib.Equals` 

- Type hints to `attrib.InList` 

- Type hints to `attrib.Ontology` 

- Type hints to `attrib.Scales` 

- Type hints to `attrib.Transformable` 

- Type hints to `attrib.Unit` 

- Type hints to `base.Input` 

- Type hints to `base.InputContainer` 

- Type hints to `base.Module` 

- Type hints to `base.Observer` 

- Type hints to `base.Component` 

- Type hints to `base.UserParameters` 

- Type hints to `base.Experiment` 

- Type hints to `base.functions` 

- Type hints to `components.CsvReader` 

- Type hints to `components.DeleteFolder` 

- Type hints to `components.DepositionToPecSoil` 

- Type hints to `components.DepositionToReach` 

- Type hints to `components.DoseResponse` 

- Type hints to `components.EnvironmentalFate` 

- Type hints to `stores.InMemoryStore` 

- Type hints to `stores.SqlLiteStore` 

- Type hints to `stores.X3dfStore` 

- Type hints to `components.ExportData` 

- Type hints to `components.ReportingDistribution` 

- Type hints to `components.ReportingHydrographicMap` 

- Type hints to `components.HydrologyFromTimeSeries` 

- Type hints to `components.LandscapeScenarioPreparation` 

- Type hints to `components.LandscapeScenario` 

- Type hints to `components.MarsWeather` 

- Type hints to `components.PpmCalendar` 

- Type hints to `components.SprayApplication` 

- Type hints to `components.TerRQ` 

- Type hints to `components.UserParameters` 

- Type hints to `components.UserParameter` 

- Type hints to `base.MCRun` 

- Type hints to `base.Project` 

- Type hints to `base.UncertaintyAnsSensitivityAnalysis` 

- Import of new classes in `base.__init__` 

- Type hints to `base.documentation` 

- Type hints to `observer.ConsoleObserver` 

- Type hints to `observer.GraphMLObserver` 

- Type hints to `observer.LogFileObserver` 

### Changed

- `attrib.Class` got new base class `base.DataAttribute` 

- Removed support of string-based type definitions in `attrib.Class` in favor for generic types introduced in Python 3.9

- `attrib.Equals` got new base class `base.DataAttribute` 

- `attrib.InList` got new base class `base.DataAttribute` 

- `attrib.Ontology` got new base class `base.DataAttribute` 

- Removed deactivated code in `attrib.Ontology` 

- `attrib.Scales` got new base class `base.DataAttribute` 

- `attrib.Transformable` got new base class `base.DataAttribute` 

- `attrib.Unit` got new base class `base.DataAttribute` 

- None-return instead of NotImplementedError in `base.Observer` methods

- Harmonized init signature of `components.CsvReader` with base class

- Harmonized init signature of `components.DeleteFolder` with base class

- Harmonized init signature of `components.DepositionToPecSoil` with base class

- Harmonized init signature of `components.DepositionToReach` with base class

- Harmonized init signature of `components.DoseResponse` with base class

- Harmonized init signature of `components.EnvironmentalFate` with base class

- Harmonized init signature of `components.ExportData` with base class

- Harmonized init signature of `components.ReportingDistribution` with base class

- Harmonized init signature of `components.ReportingHydrographicMap` with base class

- Harmonized init signature of `components.HydrologyFromTimeSeries` with base class

- Harmonized init signature of `components.LandscapeScenarioPreparation` with base class

- Harmonized init signature of `components.LandscapeScenario` with base class

- Harmonized init signature of `components.MarsWeather` with base class

- Harmonized init signature of `components.PpmCalendar` with base class

- Harmonized init signature of `components.TerRQ` with base class

- Harmonized init signature of `components.UserParameters` with base class

- Order of imports in `base.__init__` 

- Removed unused methods in `observer.GraphMLObserver` 

### Fixed

- Check for slices containing steps in `stores.SqlLiteStore` 

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

- `base.documentation.document_component()` support for the documentation of unit attribute hints

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

- `base.Extensions` changelog uses markdown for code elements

- `base.Values` changelog uses markdown for code elements

- `base.CheckResult` changelog uses markdown for code elements

- `base.DataAttributes` changelog uses markdown for code elements

- `base.Store` changelog uses markdown for code elements

- `base.Output` changelog uses markdown for code elements

- `base.OutputContainer` changelog uses markdown for code elements

- `base.DataProvider` changelog uses markdown for code elements

- `attrib.Transformable` changelog uses markdown for code elements

- `base.Input` changelog uses markdown for code elements

- `base.InputContainer` changelog uses markdown for code elements

- `base.Module` changelog uses markdown for code elements

- `base.Observer` changelog uses markdown for code elements

- `base.Component` changelog uses markdown for code elements

- `base.UserParameters` changelog uses markdown for code elements

- `base.Experiment` changelog uses markdown for code elements

- `components.CsvReader` changelog uses markdown for code elements

- `components.DeleteFolder` changelog uses markdown for code elements

- `components.DepositionToPecSoil` changelog uses markdown for code elements

- `components.DepositionToReach` changelog uses markdown for code elements

- `components.DoseResponse` changelog uses markdown for code elements

- `store.InMemoryStore` changelog uses markdown for code elements

- `store.SqlLiteStore` changelog uses markdown for code elements

- `store.X3fdStore` changelog uses markdown for code elements

- `components.ExportData` changelog uses markdown for code elements

- `components.ReportingDistribution` changelog uses markdown for code elements

- `components.ReportingHydrographicMap` markdown usage extended

- `components.LandscapeScenarioPreparation` changelog uses markdown for code elements

- `components.MarsWeather` changelog uses markdown for code elements

- `components.PpmCalendar` changelog uses markdown for code elements

- `components.TerRQ` changelog uses markdown for code elements

- `components.UserParameters` changelog uses markdown for code elements

- `base.MCRun` changelog uses markdown for code elements

- `base.Project` changelog uses markdown for code elements

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

- `base.Output` properties `default_attributes`, `description` and `attribute_hints` 

- `base.Input.description` 

- `base.Module.doc_file` 

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

- `attrib.Class` changelog uses markdown for code elements

- `attrib.Equals` changelog uses markdown for code elements

- `attrib.Ontology` changelog uses markdown for code elements

- `attrib.Scales` changelog uses markdown for code elements

- `attrib.Unit` changelog uses markdown for code elements

- `attrib` changelog uses markdown for code elements

- `base.UserParameters` property names

- `base.functions` changelog uses markdown for code elements

- `components.DepositionToPecSoil` data type access

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

- New system macro `_MC_ID_` 

- `store.X3dfStore` `identifier` argument of initializer

- `store.X3dfStore` parent run no longer randomly sampled

### Fixed

## [1.4.5] - 2012-12-29

### Added

- `base.functions.reporting()` 

- `components.ReportingDistribution.draw()` static method

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

- Changelog description

- new `components.HydrologyFromTimeSeries` inputs InflowTimeSeriesPath, ImportInflows

- new `components.HydrologyFromTimeSeries` outputs InflowReaches and Inflow

- `components.HydrologyFromTimeSeries` (optionally) reads inflows from fields

- Changelog description

- `base.McRun` changelog description

### Fixed

## [1.4.1] - 2020-12-03

### Added

- Changelog in `base.VERSION` 

- `base.VersionCollection` for managing revision history

- Changelog in `base.Extensions` 

- Changelog in `base.Values` 

- Changelog in `base.CheckResult`

- Changelog in `base.DataAttributes`

- Changelog in `base.Store` 

- Changelog in `base.Output` 

- Changelog in `base.OutputContainer`

- Changelog in `base.DataProvider`

- Changelog in class `attrib.Class` 

- Changelog in class `attrib.Equals` 

- Changelog in class `attrib.Ontology`

- Changelog in class `attrib.Scales` 

- Changelog in `attrib.Transformable`

- Changelog in class `attrib.Unit` 

- Changelog in `attrib` 

- Changelog in `base.Input`

- Changelog in `base.InputContainer` 

- Changelog in `base.Module` 

- Changelog in `base.Observer` 

- Changelog in `base.Component`

- Changelog in `base.UserParameters` 

- Changelog in `base.Experiment` 

- Changelog in `base.functions` 

- Changelog in `components.CsvReader` 

- Changelog in `components.DepositionToPecSoil` 

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

- Changelog in `base.UncertaintyAndSensitivityAnalysis` 

- Changelog in `base.__init__`

- Changelog in `observer.ConsoleObserver` 

- Changelog in `observer.GraphMLObserver` 

- Changelog in `observer.LogFileObserver` 

- Changelog in `observer.__init__` 

### Changed

- Changed `base.VERSION` to a `base.VersionCollection`, tracking changes in classes

- `base.VersionInfo` completely rewritten to move changelogs nearer to code

- Removed class `attrib.VERSION` 

- `base.Experiment.write_info_xml()` uses new `Version` classes

- `components.CsvReader` class documentation

- `components.DepositionToPecSoil` class documentation

- Removed unused output `PecSoil 2` from `components.DepositionToPecSoil` 

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

- Quick access to metadata by `base.Values.unit` and `base.Values.scales` 

- `base.DataAttributes.append()` for dynamically adding data attributes

- `attrib.Class` support of list[bytes], list[float], list[str] and tuple[float]

- Scale attribute checker

- `components.UserParameters.unit` 

### Changed

- `base.Extensions` refactored

- `base.DataAttributes` refactored

- `attrib.Class.check()` returns base.CheckResult instead of tuple

- `attrib.Equals.check()` returns base.CheckResult instead of tuple

- `attrib.Equals` refactored

- `attrib.Ontology.check()` returns base.CheckResult instead of tuple

- `attrib.Transformable.check()` returns base.CheckResult instead of tuple

- `attrib.Unit.check()` returns base.CheckResult instead of tuple

- `base.Input.read()` passes metadata from provider to `base.Values` object

- `base.InputContainer` refactored

- `base.Component` refactored

- `components.CsvReader` refactored

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

- `base.UserParameters` refactored

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

- `base.UncertaintyAndSensitivityAnalysis` refactored

### Fixed

## [1.3.24] - 2020-04-02

### Added

- Added `base.Observer.flush()` and `base.Observer.write()` to use observers as streams

- `base.functions.run_process()` for invoking system processes

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

- `base.Output` refactored

- `base.DataProvider` refactored

- `base.Input` refactored

- Option to disable observers in configuration by `base.functions.observers_from_xml()` 

### Fixed

## [1.3.5] - 2020-01-08

### Added

### Changed

- `base.Values` refactored

- `base.CheckResult` refactored

- `base.OutputContainer` refactored

- `base.Module` refactored

- `base.Observer` refactored

- `base.Experiment` refactored

- `base.Experiment` project encapsulation and support of versions

- `base.functions.replaceTokens()` replaces $$-tokens before $-tokens

- `base.functions `refactored

- `base.MCRun` refactored

- `base.Project` refactored

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

- `base.UncertaintyAndSensitivityAnalysis.create()` parameter generation possible in subdirectories

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

- `base.UserParameters` understand uncertainty / sensitivity analysis XML attribute

- `base.Experiment` has new macro `_PARAM_DIR_` 

- `base.Experiment` is more flexible in parameter directory

- `base.functions.replaceTokens()` accepts non-string values

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

- `base.Experiment` expects a global section in the Monte Carlo run configuration

- `base.Experiment` has new macro `_X3DIR_` 

- `base.functions.replaceTokens()` allows macros in source path

### Fixed

## [1.1.6]

### Added

- `base.VERSION` for describing code changes

- `base.VersionInfo` for describing individual revisions

- Value equality checker

- Changelog through `VersionInfo` class in `attrib` namespace

- `base.Experiment.write_info_xml()` for saving runtime information of the experiment

- Changelog through `VersionInfo` class in `stores` namespace

- Changelog through `VersionInfo` class in `components` namespace

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

- `base.Extensions` class as a container for data extensions

- `base.Values class` for exchanged data values

- `base.CheckResult` class for exchanging observer messages

- `base.DataAttributes` class as a data attribute container

- `base.Output` class for representing component outputs

- `base.OutputContainer` class for collecting outputs of a component

- `base.DataProvider` class for data providers

- `attrib.Class` 

- `Transformable` attribute checker

- `attrib` namespace

- `base.Input` class for representing component inputs

- `base.InputContainer` class for collecting the inputs of a component

- `base.Module` class for describing Landscape Model modules

- `base.Observer` class for representing Landscape Model observers

- `base.Component` class representing Landscape Model components

- `base.UserParameters` class for user-defined parameters

- `base.Experiment` class for managing individual experiments

- `base.functions` providing helper functions

- `components.CsvReader` component

- `components.DepositionToPecSoil` component

- `components.EnvironmentalFate` component

- `store.InMemoryStore` 

- `store.X3dfStore` 

- `stores` namespace

- `components.LandscapeScenario` component

- `components.PpmCalendar` component

- `components.UserParameters` component

- `components` namespace

- `base.MCRun` class for managing individual Monte Carlo runs

- `base` namespace

- `observer.ConsoleObserver` 

- `observer` namespace

### Changed

- `components.PpmCalendar` now requires Fields and land-use / land-cover type inputs to be of type list[int]

### Fixed
