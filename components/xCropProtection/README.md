## Table of Contents
* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Inputs](#inputs)
  * [Outputs](#outputs)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project
xCropProtection is a Landscape Model component for simulating applications of plant protection products on fields 
with a given landscape. The simulation is done on a daily-fieldwise resolution. On each day and field in the 
during the given simulation period, the module checks if there are applications of plant protection products 
should be conducted. If so, exact application dates and rates are determined. The user has the option to use
deterministic values or sample from a random distribution. 

xCropProtection currently supports the input scales `global` and `time/day, space/base_geometry`.  
xCropProtection currently supports the random variable scales `global`, `time/day`, `time/year`, `time/day, space/base_geometry` and `time/year, space/base_geometry`.  
This is an automatically generated documentation based on the available code and in-line documentation. The current
version of this document is from 2024-03-06.  

### Built with
* Landscape Model core version 1.14
* xCropProtection version 1.0 (see `module\README.md` for details)


## Getting Started
The component can be used in any Landscape Model based on core version 1.14 or newer. See the Landscape
Model core's `README` for general tips on how to add a component to a Landscape Model.

### Prerequisites
A model developer that wants to add the `xCropProtection` component to a Landscape Model needs to set up the general 
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation
1. Copy the `xCropProtection` component into the `model\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module=components.xCropProtection.xCropProtection` and 
   `class=xCropProtection`. 


## Usage
The following gives a sample configuration of the `xCropProtection` component. See [inputs](#inputs) and 
[outputs](#outputs) for further details on the component's interface.
```xml
<xCropProtection module="components" class="xCropProtection">
<xCropProtectionFilePath
scales="global">$(:xCropProtectionParameters)</xCropProtectionFilePath>
<ParametrizationNamespace
scales="global">urn:xCropProtectionLandscapeScenarioParametrization</ParametrizationNamespace>
<SimulationStart
type="date" scales="global">$(SimulationStart)</SimulationStart>
<SimulationEnd type="date"
scales="global">$(SimulationEnd)</SimulationEnd>
<RandomSeed type="int" scales="global">$(RandomSeed)</RandomSeed>
<Fields>
  <FromOutput component="LandscapeScenario" output="FeatureIds" />
</Fields>
<LandUseLandCoverTypes>
<FromOutput component="LandscapeScenario" output="FeatureTypeIds" />
</LandUseLandCoverTypes>
<FieldGeometries>
<FromOutput component="LandscapeScenario" output="Geometries" />
</FieldGeometries>
  </xCropProtection>
```

### Inputs
#### ParametrizationNamespace
`ParametrizationNamespace` expects its values to be of type `str`.
Values of the `ParametrizationNamespace` input may not have a physical unit.
Values have to refer to the `global` scale.

#### xCropProtectionFilePath
The path to the XML-parametrization of xCropProtection. A `str` of global scale. Value has no unit.
`xCropProtectionFilePath` expects its values to be of type `str`.
Values of the `xCropProtectionFilePath` input may not have a physical unit.
Values have to refer to the `global` scale.

#### SimulationStart
The first day of the simulation. A `datetime.date` of global scale. Value has no unit.
`SimulationStart` expects its values to be of type `date`.
Values of the `SimulationStart` input may not have a physical unit.
Values have to refer to the `global` scale.

#### SimulationEnd
The last day of the simulation. A `datetime.date` of global scale. Value has no unit.
`SimulationEnd` expects its values to be of type `date`.
Values of the `SimulationEnd` input may not have a physical unit.
Values have to refer to the `global` scale.

#### RandomSeed
A initialization for the random number generator. An int of global scale. Value has a unit of 1.
`RandomSeed` expects its values to be of type `int`.
Values of the `RandomSeed` input may not have a physical unit.
Values have to refer to the `global` scale.

#### Fields
A list of identifiers of individual geometries. A list[int] of scale space/base_geometry. Values have no unit.
`Fields` expects its values to be of type `list`.
Values of the `Fields` input may not have a physical unit.
Values have to refer to the `space/base_geometry` scale.

#### LandUseLandCoverTypes
The land-use and land-cover type of spatial units. A list[int] of scale space/base_geometry. Values have no unit.
`LandUseLandCoverTypes` expects its values to be of type `list`.
Values of the `LandUseLandCoverTypes` input may not have a physical unit.
Values have to refer to the `space/base_geometry` scale.

#### FieldGeometries
The geometries of individual landscape parts. A list[bytes] of scale space/base_geometry. Values have no unit.
`FieldGeometries` expects its values to be of type `list`.
Values of the `FieldGeometries` input may not have a physical unit.
Values have to refer to the `space/base_geometry` scale.

### Outputs
#### ApplicationDates
Application dates. A numpy-array of scale other/application.  
#### ApplicationRates
Application rates. A numpy-array of scale other/application.  
#### AppliedPPP
Applied products. A list[str] of scale other/application.  
#### AppliedAreas
Applied geometries. A list[bytes] of scale other/application.  
#### AppliedFields
Applied fields. A numpy-array of scale other/application.  
#### TechnologyDriftReductions
Drift reductions. A numpy-array of scale other/application.  


## Parameters
### TemporalValidity 
Temporal validity of the PPM-calendar (format: 'mm-dd to mm-dd' or 'yyyy-mm-dd to yyyy-mm-dd'). Set 'always' if the PPM-calendar should be applied over the whole simulation.

Type(s): `none` or `list[xCropProtection.MonthDaySpan]` or `list[xCropProtection.DateSpan]`

Unit: `none`

Scale(s): `time/simulation` or `time/day` or `time/year`
### TargetCrops 
Target crops of the PPM-calendar. Either use 'TargetCrops' or 'TargetFields' within a parametrization of a PPM-calendar.

Type(s): `int, list[int]`

Unit: `none`

Scale(s): `global` or `time/day` or `time/year`
### TargetFields 
Target fields of the PPM-calendar. Either use 'TargetCrops' or 'TargetFields' within a parametrization of a PPM-calendar.

Type(s): `int, list[int]`

Unit: `none`

Scale(s): `global` or `time/day` or `time/year`
### Products 
List of products that should be applied during a single application.

Type(s): `none` or `list[str]`

Unit: `none`

Scale(s): `other/products`
### ApplicationRate 
Application rate of product that should be applied during a single application.

Type(s): `float` or `xCropProtection.NormalDistribution` or `xCropProtection.UniformDistribution`

Unit: `g/ha`

Scale(s): `global` or `time/day` or `time/year` or `time/day, space/base_geometry` or `time/year, space/base_geometry`
### ApplicationWindow 
Application window of a single application (format: mm-dd to mm-dd).

Type(s): `xCropProtection.MonthDaySpan`

Unit: `none`

Scale(s): `global` or `time/day` or `time/year`
### Technology 
Technology used during a single application. The user should make sure that there is a corresponding parametrization within 'Technologies'.

Type(s): `none`

Unit: `none`

Scale(s): `global`
### InCropBuffer 
Additional non-spray-buffer within the cropped field.

Type(s): `float` or `xCropProtection.NormalDistribution` or `xCropProtection.UniformDistribution`

Unit: `m`

Scale(s): `global` or `time/day` or `time/year` or `time/day, space/base_geometry` or `time/year, space/base_geometry`
### InFieldMargin 
Additional non-crop-margin within the field.

Type(s): `float` or `xCropProtection.NormalDistribution` or `xCropProtection.UniformDistribution`

Unit: `m`

Scale(s): `global` or `time/day` or `time/year` or `time/day, space/base_geometry` or `time/year, space/base_geometry`
### MinimumAppliedArea 
Minimum area of a field for a single application.

Type(s): `float` or `xCropProtection.NormalDistribution` or `xCropProtection.UniformDistribution`

Unit: `m²`

Scale(s): `global` or `time/day` or `time/year` or `time/day, space/base_geometry` or `time/year, space/base_geometry`
### TechnologyName 
Technology name.

Type(s): `none`

Unit: `none`

Scale(s): `global`
### DriftReduction 
Drift reduction of a technology.

Type(s): `float` or `xCropProtection.NormalDistribution` or `xCropProtection.UniformDistribution`

Unit: `1`

Scale(s): `global` or `time/day` or `time/year` or `time/day, space/base_geometry` or `time/year, space/base_geometry`
## Basic parametrization  
The following gives a basic sample parametrization of the `xCropProtection` component:
```xml
<xCropProtection>
    <PPMCalendars>
        <PPMCalendar>
            <TemporalValidity scales="time/simulation">always</TemporalValidity>        
            <TargetCrops type="int" scales="global">1</TargetCrops>
            <Indications>
                <Indication>
                    <ApplicationSequence>
                        <Application>
                            <Tank>
                                <Products scales="other/products">ExampleProduct</Products>
                                <ApplicationRates scales="other/products">
                                    <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
                                </ApplicationRates>
                            </Tank>
                            <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
                            <Technology scales="global">ExampleTechnology</Technology>
                            <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
                            <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
                            <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
                        </Application>
                    </ApplicationSequence>
                </Indication>
            </Indications>
        </PPMCalendar>
    </PPMCalendars>
    <Technologies>
        <Technology>
            <TechnologyName scales="global">Technology</TechnologyName>
            <DriftReduction type="float" unit="1" scales="global">0</DriftReduction>
        </Technology>
    </Technologies>
</xCropProtection>
````  
## Multiple applications  
The following gives a sample parametrization of the `xCropProtection` component for multiple applications:
```xml
<ApplicationSequence>
    <Application>
        <Tank>
            <Products scales="other/products">
                ExampleProduct
            </Products>
            <ApplicationRates scales="other/products">
                <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
            </ApplicationRates>
        </Tank>
        <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
        <Technology scales="global">ExampleTechnology</Technology>
        <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
        <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
        <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
    </Application>
    <Application>
        <Tank>
            <Products scales="other/products">
                ExampleProduct
            </Products>
            <ApplicationRates scales="other/products">
                <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
            </ApplicationRates>
        </Tank>
        <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-07 to 14-07</ApplicationWindow>
        <Technology scales="global">ExampleTechnology</Technology>
        <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
        <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
        <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
    </Application>
    <Application>
        <Tank>
            <Products scales="other/products">
                ExampleProduct
            </Products>
            <ApplicationRates scales="other/products">
                <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
            </ApplicationRates>
        </Tank>
        <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-08 to 14-08</ApplicationWindow>
        <Technology scales="global">ExampleTechnology</Technology>
        <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
        <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
        <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
    </Application>
</ApplicationSequence>
````  
## Tank mixes  
The following gives a sample parametrization of the `xCropProtection` component for tank mixes
```xml
<Tank>
    <Products scales="other/products">
        ExampleProduct1 ExampleProduct2
    </Products>
    <ApplicationRates scales="other/products">
        <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
        <ApplicationRate type="float" unit="g/ha" scales="global">750</ApplicationRate>
    </ApplicationRates>
</Tank>
````  
## Choices between application sequences  
The following gives a sample parametrization of the `xCropProtection` component for random choices over multiple application sequences:
```xml
<Indication type="xCropProtection.ChoiceDistribution" scales="global">
    <ApplicationSequence probability="0.5">
        <Application>
            <Tank>
                <Products scales="other/products">
                    ExampleProduct1
                </Products>
                <ApplicationRates scales="other/products">
                    <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
                </ApplicationRates>
            </Tank>
            <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
            <Technology scales="global">ExampleTechnology</Technology>
            <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
            <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
            <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
        </Application>
    </ApplicationSequence>
    <ApplicationSequence probability="0.5">
        <Application>
            <Tank>
                <Products scales="other/products">
                    ExampleProduct2
                </Products>
                <ApplicationRates scales="other/products">
                    <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
                </ApplicationRates>
            </Tank>
            <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
            <Technology scales="global">ExampleTechnology</Technology>
            <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
            <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
            <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
        </Application>
    </ApplicationSequence>
</Indication>
````  
## Multiple indications  
The following gives a sample parametrization of the `xCropProtection` component for multiple indications:
```xml
<Indications>
    <Indication>
        <ApplicationSequence>
            <Application>
                <Tank>
                    <Products scales="other/products">
                        ExampleProduct1
                    </Products>
                    <ApplicationRates scales="other/products">
                        <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
                    </ApplicationRates>
                </Tank>
                <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
                <Technology scales="global">ExampleTechnology</Technology>
                <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
                <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
                <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
            </Application>
        </ApplicationSequence>
    </Indication>
    <Indication>
        <ApplicationSequence>
            <Application>
                <Tank>
                    <Products scales="other/products">
                        ExampleProduct2
                    </Products>
                    <ApplicationRates scales="other/products">
                        <ApplicationRate type="float" unit="g/ha" scales="global">750</ApplicationRate>
                    </ApplicationRates>
                </Tank>
                <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-06 to 14-06</ApplicationWindow>
                <Technology scales="global">ExampleTechnology</Technology>
                <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
                <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
                <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
            </Application>
            <Application>
                <Tank>
                    <Products scales="other/products">
                        ExampleProduct2
                    </Products>
                    <ApplicationRates scales="other/products">
                        <ApplicationRate type="float" unit="g/ha" scales="global">750</ApplicationRate>
                    </ApplicationRates>
                </Tank>
                <ApplicationWindow type="xCropProtection.MonthDaySpan" scales="global">01-07 to 14-07</ApplicationWindow>
                <Technology scales="global">ExampleTechnology</Technology>
                <InCropBuffer type="float" unit="m" scales="global">0</InCropBuffer>
                <InFieldMargin type="float" unit="m" scales="global">0</InFieldMargin>
                <MinimumAppliedArea type="float" unit="m²" scales="global">0</MinimumAppliedArea>
            </Application>
        </ApplicationSequence>
    </Indication>
</Indications>
````  
## Deterministic and random variables  
Numeric variables can be parametrized either deterministically or by describing the underlying random distribution. Currently, users can choose between normal or (continuous and discrete) uniform distribution. The following gives sample parametrizations for numeric variables:
```xml
<DeterministicVariable type="float">5.0</DeterministicVariable>
<RandomVariable type="xCropProtection.NormalDistribution">
    <Mean type="float">5.0</Mean>
    <SD type="float">1.0</SD>
</RandomVariable>
<RandomVariable type="xCropProtection.UniformDistribution">
    <Lower type="float">0.0</Lower>
    <Upper type="float">10.0</Upper>
</RandomVariable>
<RandomVariable type="xCropProtection.DiscreteUniformDistribution">
    <Lower type="int">0</Lower>
    <Upper type="int">10</Upper>
</RandomVariable>
````  
## Choice distribution  
Some variables can be parametrized such that one of the elements is randomly selected according to their probability during simulation (i.e. an element is randomly sampled from a discrete set). The following gives a sample parametrization for the choice distribution:
```xml
<Choices type="xCropProtection.ChoiceDistribution">
    <Choice probability="0.25">...</Choice>
    <Choice probability="0.25">...</Choice>
    <Choice probability="0.5">...</Choice>
</Choices>
````  
## Date-time-windows  
There are variables that describe date-time-windows. Exact dates/times are sampled during simulation. The following gives sample parametrizations for date-time-windows:
```xml
<TimeWindow type="xCropProtection.TimeSpan">00:00 to 23:59</TimeWindow>
<DateWindow type="xCropProtection.MonthDaySpan">01-01 to 31-12</DateWindow>
<DateWindow type="xCropProtection.DateSpan">2023-01-01 to 2023-31-12</DateWindow>
<DateTimeWindow type="xCropProtection.MonthDayTimeSpan">01-01 00:00 to 31-12 23:59</DateTimeWindow>
````  

## Roadmap
The `xCropProtection` component is stable. No further development takes place at the moment.


## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)). Also consult the `CONTRIBUTING` 
document for more information.


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact


## Acknowledgements