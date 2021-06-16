 Table of Contents
* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Sample `__start__.bat`](#sample-__start__bat)
  * [Parameterization Template](#parameterization-template)
  * [Experiment Configuration Template](#experiment-configuration-template)
  * [Monte Carlo Run Configuration Template](#monte-carlo-run-configuration-template)
  * [Sample `kernel.json` for a Jupyter R Kernel](#sample-kerneljson-for-a-jupyter-r-kernel)
  * [Sample `notebook.bat`](#sample-notebookbat)
  * [Macros](#macros)
  * [Available System Macros](#available-system-macros)
  * [Referencing Components, Observer and Stores](#referencing-components-observer-and-stores)
  * [Specifying Component Inputs](#specifying-component-inputs)
  * [Semantic Description of Values](#semantic-description-of-values)
  * [Available Components from Core](#available-components-from-core)
  * [Available Observers from Core](#available-observers-from-core)
  * [Available Stores from Core](#available-stores-from-core)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project
The Landscape Model core classes represent the system level of a landscape model and are used by different model
variants like XOffFieldSoil or XAquatic. Users may refer to one of these model variants to see how they can be used
to conduct simulation runs. This documentation is intended for developers that like to derive a new model variant
from the core classes. 

### Built with
The Landscape Model core is implemented in Python 3.8.
* [Python](https://www.python.org)


## Getting Started
The Landscape Model core contains class definitions representing important functional elements of a Landscape Model
like components, modules, inputs, outputs, Monte Carlo runs, experiments, etc. It also contains some components and
observers that have in-line modules. Extending this set of classes by components, observers and scenarios allows to
build a wide range of Landscape Model variants that share the same conceptual foundation. The process to build such a 
new model variant is described here. The folder structure is organized in such a way that the new model variant will
be xcopy-deployable.

### Prerequisites
* To test the model variant, a Windows 64-bit version is used.
* The most recent version of the Landscape Model core and all components, observers and scenarios that should be
  included in the initial model variant release are downloaded and extracted so that they can be copied to the 
  according folders of the model variant later.   

### Installation
 1. Create a folder for the model variant. This folder will be further on called `%VARIANT_PATH%`.
 2. Create a folder `%VARIANT_PATH%\model`. This folder will be populated with the code base and configuration of the
    model variant.
 3. Create a folder `%VARIANT_PATH%\model\variant`. All variant-specific parts of the model (components, observers,
    configuration, scripts, etc.), that is, everything except the Landscape Model core, wil be placed here later.
 4. Create a folder `%VARIANT_PATH%\run`. This folder will be used as default working folder of the model later on.
    Simulation and analysis results, all simulation data and temporary files will be written to this folder.
 5. Create a folder `%VARIANT_PATH%\scenario`. This folder will be used to collect all scenarios that will be initially
    available to the model user.
 6. Copy the entire Landscape Model core to `%VARIANT_PATH%\model\core`. The core does also contain the `init.py`
    which is the main entry point for the simulation.
 7. Make sure that the user parameterization can be passed conveniently to the `init.py`. This depends on your general
    setup, but for a xcopy-deployable version of your model you might want to create a `__start__.bat` in the
    `%VARIANT_PATH%`. See this [sample of an startup batch](#sample-__start__bat).
 8. Provide a parameterization template to the user so that becomes clear which parameters are available and required
    for your model. Add inline documentation (XML comments) to the parameterization file to help the user fill out the
    parameterization. The template file must have an `.xrun` file ending and should be placed in the 
    `%VARIANT_PATH%`. See the [parameterization template](#parameterization-template) as an example.
 9. Create an experiment configuration file `%VARIANT_PATH%\model\variant\experiment.xml` that configures experiments
    conducted by your model in a general manner (e.g., processing directories, number of Monte Carlo runs).
    Everything that potentially changes between Monte Carlo runs (e.g., composition, initial values) is not specified
    here but in the Monte Carlo run configuration. See the
    [experiment configuration template](#experiment-configuration-template) for an example of how to prepare an
    experiment configuration.
10. Create a Monte Carlo run configuration file `%VARIANT_PATH%\model\variant\mc.xml` that configures Monte Carlo runs
    of the simulation. This file contains the composition of a simulation run, that is, it defines the components that
    are run during simulation. It also specifies how input and output values of these components are linked. See the
    [Monte Carlo run configuration template](#monte-carlo-run-configuration-template) for an example of how to prepare a
    Monte Carlo run configuration.
11. Provide a `%VARIANT_PATH%\README.md` file, preferably similar in structure to the one here, along with the model
    variant. This will help users in understanding, getting started, using and contributing to your model.
12. Provide a `%VARIANT_PATH%\LICENSE.txt` along with your model. Please respect the licenses of the parts included into
    your model when deciding for a license. The Landscape Model core itself is given under a [CC0 license](#license).
13. Provide a `%VARIANT_PATH%\CHANGELOG.md`, similar in structure to the `CHANGELOG` provided with the Landscape Model
    core. The changelog should show the version history of your model, including all important, and clearly indicate
    what the current version is.
14. Provide a `%VARIANT_PATH%\CONTRIBUTING.md` that details how others can contribute to the future development of your
    model.
15. Copy all scenarios that you like to initially provide with your model to the `%VARIANT_PATH%\scenario` folder. The
    folder name of the scenario is used to reference the scenario in the parameterization file. See the `README` of each
    scenario of additional information on its usage.
16. Copy all additional components and observers used by your model into the `%VARIANT_PATH%\model\variant` folder. 
    These model parts can then be [referenced by the model configuration](#referencing-components-observer-and-stores).
    See the `README` files of the individual components and observers for further information on their usage.
17. If you like to provide the user with a Jupyter notebook infrastructure, create a folder `%VARIANT_PATH%\analysis`.
    This folder will contain Jupyter notebooks provided to and created by the user.
18. If you like to provide additional kernels to the Jupyter notebook, place them in sub-folders under 
    `%VARIANT_PATH%\model\variant\jupyter`.
19. Make sure that the runtime environments used by additional kernels are xcopy-portable, are contained in your model
    package, contain all required  packages and are linked properly in the `kernel.json` file. See the [sample 
    `kernel.json` for a Jupyter R kernel](#sample-kerneljson-for-a-jupyter-r-kernel) as an example.
20. Create a batch file, e.g. using [this sample](#sample-notebookbat) to give users easy access to the Landscape Model
    Jupyter notebook.
21. Place Jupyter notebooks that you like to ship with your model under `%VARIANT_PATH%\analysis`.


## Usage

### Sample `__start__.bat`
The following batch file located in the `%VARIANT_PATH%` simply passes its arguments to the `init.py` of the Landscape
Model. It allows the user of your model to drag and drop one or multiple parameterization files on the batch file and 
start the model. 
```batch
@ echo off
"%~dp0\model\core\bin\Python38\python.exe" "%~dp0\model\core\init.py" %*
pause
```

### Parameterization Template
The following shows the simplest possible user parameterization. Only the two mandatory parameters `<Project>`,
specifying which scenario to use, and `SimID`, defining the unique name of the next simulation run, ae present.
Further parameters can be added and are then available in the configuration by macros. The parameterization provided
to the user should be inline documented properly using XML comments.
```xml
<?xml version="1.0" encoding="utf-8"?>
<Parameters>
    <Project>scenario/???</Project>
    <SimID>Test Run</SimID>
</Parameters>
```

### Experiment Configuration Template
The following code shows a simple Landscape Model experiment configuration. Paths are specified so that the model is
xcopy-deployable using the folder structure created during [installation](#installation). Model runs wil consist of
one Monte Carlo run and will not run Mont Carlo runs in parallel if the number of Monte Carlo runs is increased. You 
might want to adjust these settings or even provide the number of Monte Carlo runs as a user parameter. See under
[macros](#macros) how to do so.

The configuration defines two observers, one that will output all messages processed by the Landscape Model to the
console and another one that writes the same messages to an `experiment.log` logfile in the `log` sub-folder of the
simulation run. See the [available system macros](#available-system-macros) to see how to interpret the paths given
in th configuration and how to adapt them to your needs. See the section about 
[referencing components, observers and stores](#referencing-components-observer-and-stores) to find out how to add 
additional observers.
```xml
<?xml version="1.0" encoding="utf-8"?>
<Experiment>
  <General>
    <MCRunTemplate>$(_X3DIR_)/../../variant/mc.xml</MCRunTemplate>
    <MCBaseDir>$(_EXP_DIR_)\mcs</MCBaseDir>
    <NumberMC>1</NumberMC>
    <NumberParallelProcesses>1</NumberParallelProcesses>
    <ExperimentDir>$(_EXP_BASE_DIR_)\$(SimID)</ExperimentDir>
  </General>
  <Observers>
    <Observer module="observer" class="ConsoleObserver"/>
    <Observer module="observer" class="LogFileObserver">
      <LogFile>$(_EXP_DIR_)\log\experiment.log</LogFile>
    </Observer>
  </Observers>
</Experiment>
```

### Monte Carlo Run Configuration Template
The following code shows a simple Landscape Model Monte Carlo run configuration. Paths are specified so that the model
is xcopy-deployable using the folder structure created during [installation](#installation).

The configuration defines two observers, one that will output all messages processed by the Landscape Model to the
console and another one that writes the same messages to an `experiment.log` logfile in the `log` sub-folder of the
simulation run. See the [available system macros](#available-system-macros) to see how to interpret the paths given
in th configuration and [macros](#macros) to learn about macros in general. See the section about 
[observers](#available-observers-from-core) to find out which observers ar available. Please note that observers for
the experiment as a whole and for Monte Carlo runs specifically are independent, allowing for a variety of advanced 
message processing. 

Each Monte Carlo run will, according to the configuration, use its own `X3df` store, an HDF5-based container for multi-
dimensional arrays. This is the default store used in Landscape Model runs, but you can have a look under 
[stores](#available-stores-from-core) for other available options.

The configuration defines two global parameters, `<SimulationStart>` and `<SimulationEnd`. See the section about
[macros](#macros) to see the impact of these definitions.

The `<composition>` section of the configuration specifies the components that are part of the model. Components can be
either [available components from core](#available-components-from-core) or additional components provided with the
model variant. How components are referenced is detailed under 
[referencing components, observer and stores](#referencing-components-observer-and-stores). Components are run in 
sequence in the order given in the configuration. Input values of components are [specified either in the configuration
or as the output of another component](#specifying-component-inputs). Each value can be [enriched with semantic 
descriptions](#semantic-description-of-values).

In the template configuration, two components are defined: an `<LULC>` component that reads in a landscape scenario
and provides it to other components in the Landscape Model, and a `<PPM>` component that simulates farmer actions in
the fields specified by the landscape scenario. 
```xml
<?xml version="1.0" encoding="utf-8"?>
<MCRun>
    <Observers>
        <Observer module="observer" class="ConsoleObserver"/>
        <Observer module="observer" class="LogFileObserver">
            <LogFile>$(_EXP_BASE_DIR_)\$(SimID)\log\mc_$(_MC_NAME_).log</LogFile>
        </Observer>
    </Observers>
    <Store module="stores" class="X3dfStore">
        <File_Path>$(_MCS_BASE_DIR_)\$(_MC_NAME_)\store</File_Path>
        <Observer>
            <ObserverReference/>
        </Observer>
    </Store>
    <Global>
        <SimulationStart>2015-03-01</SimulationStart>
        <SimulationEnd>2015-03-01</SimulationEnd>
    </Global>
    <Composition>
        <LULC module="components" class="Lulc">
            <BaseLandscapeGeometries>$(:LandscapeScenario)</BaseLandscapeGeometries>
        </LULC>
        <PPM module="components" class="PpmCalendar">
            <SimulationStart type="date">$(SimulationStart)</SimulationStart>
            <SimulationEnd type="date">$(SimulationEnd)</SimulationEnd>
            <ApplicationWindows>03-01 to 03-01</ApplicationWindows>
            <Fields>
                <FromOutput component="LULC" output="FeatureIds"/>
            </Fields>
            <Lulc>
                <FromOutput component="LULC" output="LulcTypeIds"/>
            </Lulc>
            <TargetLulcType>
                <FromOutput component="LULC" output="target_lulc_type"/>
            </TargetLulcType>
            <ApplicationRate type="float" unit="g/ha">100</ApplicationRate>
            <TechnologyDriftReduction type="float" unit="1">0</TechnologyDriftReduction>
            <InCropBuffer type="float" unit="m">0</InCropBuffer>
            <InFieldMargin type="float" unit="m">0</InFieldMargin>
            <FieldGeometries>
                <FromOutput component="LULC" output="Geometries"/>
            </FieldGeometries>
            <MinimumAppliedArea type="float" unit="m²">10</MinimumAppliedArea>
            <RandomSeed type="int">0</RandomSeed>
            <ProbabilityFieldApplied type="float" unit="1">1</ProbabilityFieldApplied>
        </PPM>
    </Composition>
</MCRun>
```

### Sample `kernel.json` for a Jupyter R Kernel
The following `kernel.json` file shows how a xcopy-deployable R instance (in this case the one used by the 
`AnalysisObserver`) can be used from within the Landscape Model Jupyter notebook.
```json
{
  "argv": [
    "model/variant/AnalysisObserver/R-3.5.1/bin/x64/R",
    "--slave",
    "-e",
    "IRkernel::main()",
    "--args",
    "{connection_file}"
  ],
  "display_name": "R",
  "language": "R"
}
```

### Sample `notebook.bat`
The following batch file located in the `%VARIANT_PATH%` launches the Landscape Model Jupyter notebook so that users
can explore pre-prepared notebooks or can create them on their own. 
```batch
@ echo off
"%~dp0\model\core\bin\Python38\python.exe" "%~dp0\model\core\init.py" notebook
pause
```

### Macros
Macros provide a flexible way to share text strings between configuration and parameterization files. The basic pattern
of a macro is `$(<MacroName>)` where __<MacroName>__ is the specific name of the macro. Whenever a parameterization or
configuration file is written with support of macros, all macro patterns are replaced by the specific current text 
value of the macro. This allows to specify values once and reuse them at various places, helping to make the 
configuration more consistent. For instance, many components require the simulation start as input, but making sure 
that is set equally among components is cumbersome and prone to error. Macros allow to specify the simulation start 
ones and using the macro on all places where the datum is needed. Another purpose of the macros is to externalize  
parameters, for instance to define parameters that can be set by the user or the scenario developer.

Values of macros are set in several places. The following list gives an overview over these places in precedence order.
That is, if the same macro is set in more than one place, subsequent settings will not overwrite the first setting
according to the order of the list. Macro names are case-sensitive and may consist of any characters but should not 
contain any control characters of parameterization or configuration files, basically XML control characters. The same
applies to macro values. As latter are inserted as text in place of the macro, certain characters may break the
parameterization or configuration file.
* Some macros are set by the Landscape Model core itself. These macros start and end with an underscore and are in
  __uppercase__: `$(_MACRO_NAME_)`. See the list of [available system macros](#available-system-macros) for the specific
  set of available macros. System macros are comparable to environment variable and provide paths and identifiers used
  by the Landscape Model.
* The Monte Carlo run configuration contains a section `<Global>`. This section can contain an arbitrary number of macro
  definitions of the form `<MacroName>Value</MacroName>`. Values specified this way can be reused in the configuration
  by placing a macro `$(MacroName)` in the according places. Please note that all macros, including the globals, 
  currently operate on a text level so that any semantic specification has to take place where the macro is used and not
  in the `<Global>` section.
* Every entry under `<Parameters>` in the `.xrun` user parameterization also follows the form 
  `<MacroName>Value</MacroName>` and functions exactly the same as the global macros. This way, the model developer can
  decide for a set of parameters that should be exposed at the user level (i.e., in the parameterization file) and can
  then be used as macro in the configuration files. This is a simple but flexible and effective way to scale the 
  degree of complexity in exchange to more degrees of freedom in parameterization that is exposed to the model user.
* Scenarios also provide macro values. The according macros follow the pattern `$(:MacroName)`. What macros are set by
  a scenario is defined by the scenario developer, but mainly will the scenario macros contain absolute paths to the
  individual parts of a scenario. The list of macros set by a scenario is given in the individual scenario
  documentations.

### Available System Macros
The following list gives an overview of the system macros set by the Landscape Model in alphabetical order. 
`%VARIANT_PATH%` is the path where the model resides (see [installation](#installation)). 
* `_EXP_BASE_DIR_` - The base working directory of the model, e.g., `%VARIANT_PATH%\run`. The default value is to use
  the `run` sub-folder, but if there are reasons to use another folder, this can be changed in the `init.py` of the
  Landscape Model core.
* `_EXP_DIR_` - The working directory of an individual experiment, e.g., `%VARIANT_PATH%\run\Test Run`. The value of 
  this path is specified in the experiment configuration as `<ExperimentDir>` under `<General>`. Usually, it is 
  specified there as `$(_EXP_BASE_DIR_)\$(SimID)`, that is, as a sub-directory of the base working directory (see above)
  with the
  name of the experiment as specified by a macro `SimID` which is set in the user parameterization.
* `_MC_ID_` - The numerical identifier of the Monte Carlo run.
* `_MC_NAME_` - The name of the individual Monte Carlo run. It is a random combination of 16 uppercase letters and 
  digits prepended by `X3`. The generation of this name is hard-coded in the `Experiment.py` of the Landscape Model 
  core.
* `_MCS_BASE_DIR_` - The base working directory of the individual Monte Carlo runs for an experiment, e.g., 
  `%VARIANT_PATH%\run\Test Run\mcs`. This path is specified in the experiment configuration as `<MCBaseDir>` under 
  `<General>`. A usual definition is `$(_EXP_DIR_)\mcs`, that is, a sub-folder `mcs` in the working directory of the
  experiment (see above). 
* `_PARAM_DIR_` - The directory where the parameterization file resides, e.g., `%VARIANT_PATH%`. This path depends on
  the parameterization file that the user passes to the `__start__.bat`, if this is the process of invoking the model. 
* `_PROJECT_DIR_` - The directory from where paths to scenario information are resolved. By default, this is the same as
   the `_PARAM_DIR_`, but it can be overridden through the `init.py` of the Landscape Model core.  
* `_SCENARIO_DIR_` - The directory where scenario data is stored, e.g., `%VARIANT_PATH%\scenario\Scenario 1`. The value
  of this macro is commonly set as a combination of the `_PROJECT_DIR_` with the `$(Project)` macro that is set in the
  user parameterization.
* `_X3_DIR_` - The directory where the Landscape Model core is located, e.g., `%VARIANT_PATH%\model\core\base`. This is
  usually set automatically by the Landscape Model according to the path where code files were loaded from. However,
  this directory can be overridden by setting an environment variable `X3DIR` which is useful in complex debugging cases
  where code is loaded via file system junctions. This macro is usually not used in configuration files.

### Referencing Components, Observer and Stores
One of the important task of the configuration files is to specify the composition of the model. This is done by adding
blocks for components, observers and stores at the according places in the configuration files.

To add a component to the model, add a block in the `<Composition>` section of the Monte Carlo run configuration, e.g.:
```xml
<LULC module="components" class="Lulc">
    <BaseLandscapeGeometries>$(:LandscapeScenario)</BaseLandscapeGeometries>
</LULC>
``` 
Components are processed in the order of occurrence in the configuration file. Make sure that dependencies are met by 
placing dependent components behind components that provide the required values. The name of the added component block,
`<LULC>` in the example, specifies how the component is further on referenced. This name must be unique within the
composition. The `module` attribute specifies where the Landscape Model can find the component. It has to be set to
`"components"` if any of the [available components from core](#available-components-from-core) is referenced. If it is
a component that is placed under `%VARIANT_PATH%\model\variant`, then the path name of the component within this folder
has to be filled in. See the `README` of components for further information. The `class` attribute specifies the name
of the required Python class, that is loaded from the just defined path. Again, see the according documentations 
([available components from core](#available-components-from-core) and `README` of components) for further details.
Components require [specifying inputs](#specifying-component-inputs).
 
Observers can be specified in two places: the `<Observers>` section in the experiment configuration and the 
`<Observers>` section in the Monte Carlo run configuration, e.g.,
```xml
<Observer module="observer" class="ConsoleObserver"/>
```
Each observer definition has to be within an `<Observer>` tag, tha is, unlike components, observers are not assigned
individual names. There may be an arbitrary number of observers and all receive the same messages in the order given.  
`module` for any of the [available observers from core](#available-observers-from-core) is `"observers"`, for observers
under `%VARIANT_PATH%\model\variant` see according `README` files. Documentations also detail available classes.
Observers may require additional parameterization, see documentations for details.

A single store is configured in the Monte Carlo run configuration under `<Store>`, e.g.,
```xml
<Store module="stores" class="X3dfStore">
    <File_Path>$(_MCS_BASE_DIR_)\$(_MC_NAME_)\store</File_Path>
    <Observer>
        <ObserverReference/>
    </Observer>
</Store>
```
`module` for any of the [available stores from core](#available-stores-from-core) is `"stores"`, for stores under 
`%VARIANT_PATH%\model\variant` see according `README` files. Documentations also detail available classes. Stores may
require additional parameterization, see documentations for details. The store has also its own (single) observer, but
it is also possible to use a special `<ObserverReference>` tag to reference the (multiple) observers defined under
`<Observers>`.

### Specifying Component Inputs
Input values of components must be available the time when the component is run. There are two principal ways to achieve
this using the Landscape Model Monte Carlo run configuration: either by linking the input to an output of another 
component in the composition or by specifying values directly within the configuration.

The linking of a component input to a component output ensures consistency within the model and allows passing arbitrary
large datasets. Its general form is shown in the next code block. There is a `<Component1>` that, in this example, has
no inputs. It has, however, an output named `"Output1"`, a fact that should be retrieved from the component 
documentation. Another component, named `"Component2"` here, has an input named `"Input2"`, a fact that should be 
documented in the component's documentation. To use the values of `"Output1"` as input values for `"Input2"`, a 
`<FromOutput>` element is used, within the Monte Carlo runs composition configuration, as the XML value of `<Input2>`. 
The attribute `"component"` of this XML element refers to the (user-specified) name of a component defined previously in
the composition, here `"Component1"`. See the section about
[referencing components](#referencing-components-observer-and-stores) for more information about component names. The 
`"output"` attribute contains the name of the linked output. What outputs a component offers can be seen 
[here for the available components from core](#available-components-from-core) and in the `README` files of all other 
components. 
```xml
<Component1 module="test-components" class="Test"/>
<Component2>
    <Input2>
        <FromOutput component="Component1" output="Output1"/>
    </Input2>
</Component2>
```

Values can also be specified directly in te configuration by their string representations. Naturally, this is more 
feasible for scalar values or small lists and less for large arrays of values. Within the value's string representation,
[macros](#macros) can be used. It is also possible to enrich the value with 
[semantic descriptions](#semantic-description-of-values), e.g., type information, information about physical units or
information about scales to which the value applies. 
```xml
<Component module="test-components" class="Test">
    <Input>Value</Input>
</Component>
```

### Semantic Description of Values
The Landscape Model core is implemented in a way that manages semantic information of values. Inputs can currently 
specify expectations about types, physical units and scales, but other semantic specifications (e.g., using ontological
descriptions) are possible in the future. When values are requested fom the Landscape Model core by an input, they are
checked against these expectations. Not only is a message to the store observer emitted tht indicates whether and how
the values are processed regarding their semantic description but also the Landscape Model core attempts to fulfill
data specifications as informed as possible by applying transformations to the data where necessary and where 
transformation paths are implemented, again transparently indicating this processing by messages to the observer.

It is the duty of the component developer to specify the requirements of input data and, therefore, the components'
documentations are the place where the model developer can find this information. It is also the component that
enriches output values by semantic meaning that can then be used to compare input and output specifications when the
output is linked to an input (see [specifying component inputs](#specifying-component-inputs)).

If input values are, however, specified directly in the Monte Carlo run configuration (see 
[specifying component inputs](#specifying-component-inputs)), it is the task of the model developer to describe this
values in as much detail as is required to make the model work properly. This is done by adding XML attributes to the
according input XML elements. Currently, there are three aspects that can be specified, which are detailed in the 
following list.
1. Type information can be added by a `type` attribute: `<Input type="xyz">Value</Input>`. While there is a wide range
   of types that can be handled by Landscape Model stores, there is only a limited set of types that can be used within
   the `type` attribute:
   * If the `type` attribute is omitted, the given _Value_ is interpreted as character sequence, and the component sees
     an input value of Python type `str`. The string value equals the XML text value but make sure to consider potential
     whitespace handling of XML processor, e.g., when preceding or subsequent whitespace is important.
   * If `type="bool"` and the _Value_ is `true` (case-insensitive), the value is interpreted as `True` and, in all other
     cases, as `False`.
   * If `type="date"`, the _Value_ must be given in the format `"%Y-%m-%d"` ("4 digit Year-2 digit month-2 digit day", 
     e.g., "2021-11-24"). It is then parsed as a Python `datetime.date` and provided as such as input value.
   * If `type="datetime"`, the _Value_ must be given in the format `"%Y-%m-%d %H:%M"` ("4 digit Year-2 digit month-2 
     digit day<space>2 digit hour:2 digit minute", e.g., "2021-11-24 10:21"). It is then parsed as a Python 
     `datetime.datetime` and provided as such as input value.
   * If `type="float"`, the _Value_ is parsed a Python `float` (no localization considered) and passed as such.
   * If `type="int"`, the _Value_ is parsed a Python `nt` (no localization considered) and passed as such.
   * If `type="list[float]"`, the _Value_ must be a space-separated list of floating-point numbers. Each is parsed as a 
     Python `float` (no localization considered), and they are provided in their entirety to the input as a Python 
     `list` (using the same order as given in the text representation). If an empty value is specified, the input sees 
     an empty list.
   * If `type="list[int]"`, the _Value_ must be a space-separated list of integers. Each is parsed as a Python `int`
     and they are provided in their entirety to the input as a Python `list` (using the same order as given in the 
     text representation). If an empty value is specified, the input sees an empty list. 
   * If `type="list[str]"`, the _Value_ must be a list of strings, separated by `|`. Each is parsed as a Python `str`
     and they are provided in their entirety to the input as a Python `list` (using the same order as given in the 
     text representation). If an empty value is specified, the input sees an empty list.
2. Information about physical units can be added through an `unit` attribute: `<Input unit="xyz">Value</Input>`. Any
   unit can be given here, but not all possible transformation paths are defined. See the component's documentations
   for details on the physical units of inputs and outputs. Here are some examples of units used by components:
   * Omitting the specification of a unit is interpreted Landscape Model core as either the unit is not given, or the
     system of physical units does not apply to the value (e.g., categorical values). Some inputs require values to not
     have a unit.
   * For range values that have no other physical dimension (e.g., counts, fractions, etc.), commonly a unit of `"1"` is
     specified. This clearly indicates that, for instance, the value can be multiplied with values having other units
     but does not change the unit of the result.
   * Rates, e.g., `"g/ha"` or `"mg/m²"`.
   * Lengths, e.g., `"m"`.
   * Areas, e.g., `"m²"`.
   * Volumes, e.g., `"m³""`.
   * Flow volumes, e.g., `"m³/d"` or `"m³/s"`.
   * Concentrations, e.g. `"g/m³"` or `"mg/m³"`.
   * Temperatures, e.g., `"°C"`.
   * Densities, e.g., `"g/mol"`.
3. Information about the scales to which values apply can be specified using an `scales` attribute: 
   `<Input scales="xyz">Value</Input>`. Scales are defined per dimension in the format 
   `dimension/scale[, dimension/scale]...`, where for each dimension (e.g., space, time, etc.) a scale is specified.
   Dimensions and scales have to be specified in the order they are organized in the data. However, scales have not 
   often to be explicitly expressed in configurations as most values specified directly in the configuration are valid
   at a `"global"` scale, i.e., for all simulated elements, and an omitted `scales` attribute is interpreted as
   designating exactly that. Normally, only when a list of values is give (see above), the scale is not `"global"` but
   something like, e.g., `"other/species"` if the list describes values for different species. For the linking of a
   component input to a component outputs, however, scales provide important information for data management. See the 
   documentations of individual components for further information on the scales of input and output values.   

### Available Components from Core
For a list of components that are shipped with the Landscape Model core, see the `COMPONENTS` file.

### Available Observers from Core
For a list of observers that are shipped with the Landscape Model core, see the `OBSERVERS` file.

### Available Stores from Core
For a list of stores that are shipped with the Landscape Model core, see the `STORES` file.


## Roadmap
The Landscape Model core is under continuous development. Check for updates regularly and have a look at the `CHANGELOG`
to see what is new.


## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)).


## License
The Landscape Model core is distributed under the CC0 License. See the `LICENSE` file for more information.


## Contact
Thorsten Schad - thorsten.schad@bayer.com
Sascha Bub - sascha.bub.ext@bayer.com


## Acknowledgements
* [colorama](https://pypi.org/project/colorama/)
* [GDAL](https://pypi.org/project/GDAL)
* [h5py](https://www.h5py.org)
* [matplotlib](https://matplotlib.org)
* [NumPy](htps://numpy.org)
* [SciPy](https://www.scipy.org)
