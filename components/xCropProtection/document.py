import re
import sys
import os
import textwrap
import inspect
import xml.etree.ElementTree
from components import xCropProtection
from base import documentation


# parameters:
PARAMETERS = {
    "TemporalValidity": {
        "attributes": {
            "type": "none|list[xCropProtection.MonthDaySpan]|list[xCropProtection.DateSpan]",
            "unit": "none",
            "scales": "time/simulation|time/day|time/year",
        },
        "description": "Temporal validity of the PPM-calendar (format: 'mm-dd to mm-dd' or 'yyyy-mm-dd to yyyy-mm-dd'). Set 'always' if the PPM-calendar should be applied over the whole simulation.",
    },
    "TargetCrops": {
        "attributes": {
            "type": "int, list[int]",
            "unit": "none",
            "scales": "global|time/day|time/year",
        },
        "description": "Target crops of the PPM-calendar. Either use 'TargetCrops' or 'TargetFields' within a parametrization of a PPM-calendar.",       
    },
    "TargetFields": {
        "attributes": {
            "type": "int, list[int]",
            "unit": "none",
            "scales": "global|time/day|time/year",
        },
        "description": "Target fields of the PPM-calendar. Either use 'TargetCrops' or 'TargetFields' within a parametrization of a PPM-calendar.",       
    },
    "Products": {
        "attributes": {
            "type": "none|list[str]",
            "unit": "none",
            "scales": "other/products|other/active_substances",
        },
        "description": "List of products that should be applied during a single application.",        
    },
    "ApplicationRate": {
        "attributes": {
            "type": "float|xCropProtection.NormalDistribution|xCropProtection.UniformDistribution",
            "unit": "g/ha",
            "scales": "global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry",
        },
        "description": "Application rate of product that should be applied during a single application.",   
    },
    "ApplicationWindow": {
        "attributes": {
            "type": "xCropProtection.MonthDaySpan",
            "unit": "none",
            "scales": "global|time/day|time/year",
        },
        "description": "Application window of a single application (format: mm-dd to mm-dd).",       
    },
    "Technology": {
        "attributes": {
            "type": "none",
            "unit": "none",
            "scales": "global",
        },
        "description": "Technology used during a single application. The user should make sure that there is a corresponding parametrization within 'Technologies'.",                
    },
    "InCropBuffer": {
        "attributes": {
            "type": "float|xCropProtection.NormalDistribution|xCropProtection.UniformDistribution",
            "unit": "m",
            "scales": "global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry",
        },
        "description": "Additional non-spray-buffer within the cropped field.",                
    },
    "InFieldMargin": {
        "attributes": {
            "type": "float|xCropProtection.NormalDistribution|xCropProtection.UniformDistribution",
            "unit": "m",
            "scales": "global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry",
        },
        "description": "Additional non-crop-margin within the field.",                        
    },
    "MinimumAppliedArea": {
        "attributes": {
            "type": "float|xCropProtection.NormalDistribution|xCropProtection.UniformDistribution",
            "unit": "m²",
            "scales": "global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry",
        },
        "description": "Minimum area of a field for a single application.",                
    },
    "TechnologyName": {
        "attributes": {
            "type": "none",
            "unit": "none",
            "scales": "global",
        },
        "description": "Technology name.",                
    },
    "DriftReduction": {
        "attributes": {
            "type": "float|xCropProtection.NormalDistribution|xCropProtection.UniformDistribution",
            "unit": "1",
            "scales": "global|time/day|time/year|time/day, space/base_geometry|time/year, space/base_geometry",
        },
        "description": "Drift reduction of a technology.",                
    }
}
                    
def document_parameters(name: str, file_path: str):
    with open(file_path, "a", encoding="utf-8") as f: 
        f.write(f"## {name}\n")
        for param in PARAMETERS:
            param_name = param
            type = PARAMETERS[param]["attributes"]["type"].split("|")
            type = " or ".join(["`" + x + "`" for x in type])
            unit = PARAMETERS[param]["attributes"]["unit"].split("|")
            unit = " or ".join(["`" + x + "`" for x in unit])
            scales = PARAMETERS[param]["attributes"]["scales"].split("|")
            scales = " or ".join(["`" + x + "`" for x in scales])
            description = PARAMETERS[param]["description"]
            f.write(f"""### {param_name} 
{description}\n
Type(s): {type}\n
Unit: {unit}\n
Scale(s): {scales}
""")
        
# examples:
EXAMPLES = [
    {
        "title": "Basic parametrization",
        "description": "The following gives a basic sample parametrization of the `xCropProtection` component:",
        "example": """<xCropProtection>
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
</xCropProtection>"""
    },
    {
        "title": "Multiple applications",
        "description": "The following gives a sample parametrization of the `xCropProtection` component for multiple applications:",
        "example": """<ApplicationSequence>
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
</ApplicationSequence>"""
    },
    {
        "title": "Tank mixes",
        "description": "The following gives a sample parametrization of the `xCropProtection` component for tank mixes",
        "example": """<Tank>
    <Products scales="other/products">
        ExampleProduct1 ExampleProduct2
    </Products>
    <ApplicationRates scales="other/products">
        <ApplicationRate type="float" unit="g/ha" scales="global">1000</ApplicationRate>
        <ApplicationRate type="float" unit="g/ha" scales="global">750</ApplicationRate>
    </ApplicationRates>
</Tank>"""
    },
    {
        "title": "Choices between application sequences",
        "description": "The following gives a sample parametrization of the `xCropProtection` component for random choices over multiple application sequences:",
        "example": """<Indication type="xCropProtection.ChoiceDistribution" scales="global">
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
</Indication>"""
    },
    {
        "title": "Multiple indications",
        "description": "The following gives a sample parametrization of the `xCropProtection` component for multiple indications:",
        "example": """<Indications>
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
</Indications>"""
    },
    {
        "title": "Deterministic and random variables", 
        "description": "Numeric variables can be parametrized either deterministically or by describing the underlying random distribution. Currently, users can choose between normal or (continuous and discrete) uniform distribution. The following gives sample parametrizations for numeric variables:",
        "example": """<DeterministicVariable type="float">5.0</DeterministicVariable>
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
</RandomVariable>"""
    },
    {
        "title": "Choice distribution", 
        "description": "Some variables can be parametrized such that one of the elements is randomly selected according to their probability during simulation (i.e. an element is randomly sampled from a discrete set). The following gives a sample parametrization for the choice distribution:",
        "example": """<Choices type="xCropProtection.ChoiceDistribution">
    <Choice probability="0.25">...</Choice>
    <Choice probability="0.25">...</Choice>
    <Choice probability="0.5">...</Choice>
</Choices>"""
    },
    {
        "title": "Date-time-windows",
        "description": "There are variables that describe date-time-windows. Exact dates/times are sampled during simulation. The following gives sample parametrizations for date-time-windows:",
        "example": """<TimeWindow type="xCropProtection.TimeSpan">00:00 to 23:59</TimeWindow>
<DateWindow type="xCropProtection.MonthDaySpan">01-01 to 31-12</DateWindow>
<DateWindow type="xCropProtection.DateSpan">2023-01-01 to 2023-31-12</DateWindow>
<DateTimeWindow type="xCropProtection.MonthDayTimeSpan">01-01 00:00 to 31-12 23:59</DateTimeWindow>"""
    },
]

def document_examples(file_path: str):
    with open(file_path, "a", encoding="utf-8") as f: 
        for example in EXAMPLES:
            title = example["title"]
            sample_description = example["description"]
            sample_parametrization = example["example"]
            f.write(f"""## {title}  
{sample_description}
```xml
{sample_parametrization}
````  
""")

# def document_class(name: str, class_name: str, file_path: str):
#     doc = globals()[class_name].__doc__
#     description = re.search(r"(?<=    ).*(?=\n\n    INPUTS)", doc).group(0)
#     inputs = re.search(r"(?<=INPUTS\n    )(.|\n)*?(?=(\n    OUTPUTS|$))", doc).group(0)
#     inputs = inputs.split("    ")
#     inputs = inputs[:-1]
#     inputs = ["* " + input.strip() for input in inputs]
#     with open(file_path, "a", encoding="utf-8") as f:
#         f.write(f"""#### {name}
# {description} This class is parametrized with the following inputs:
# """)    
#         inputs = "  \n".join(inputs)
#         f.write(inputs + "  \n\n")

# def document_xml(name: str, sample_xml_path: str, file_path: str):
#     sample_xml = xml.etree.ElementTree.parse(sample_xml_path)
#     sample_parametrization = "\n".join(
#         textwrap.wrap(
#             inspect.cleandoc(
#                 xml.etree.ElementTree.tostring(
#                     sample_xml.getroot()).decode("utf-8")),
#             120,
#             replace_whitespace=False
#             )
#         )
#     with open(file_path, "a", encoding="utf-8") as f: 
#         f.write(f"""## {name}  
# The following gives a sample parametrization of the `xCropProtection` component.  
# ```xml
# {sample_parametrization}
# ````  
# """)

readme_path = os.path.join("model", "core", "components", "xCropProtection", "README.md")
mc_xml_path = os.path.join("model", "variant", "mc.xml")

documentation.document_component(
    xCropProtection("xCropProtection", None, None),
    readme_path,
    mc_xml_path
)
document_parameters("Parameters", readme_path)
document_examples(readme_path)
