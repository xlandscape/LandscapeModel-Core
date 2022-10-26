import re
import sys
import os
import base.documentation
import textwrap
import inspect
import xml.etree.ElementTree
sys.path.insert(0, "model/variant")
import XPPP
from .classes import PPMCalendar, ApplicationWindowDistribution, Tank, PPP, Application, Technology
from .distributions import NormalDistribution, UniformDistribution, DiscreteUniformDistribution, ChoiceDistribution

def document_class(name: str, class_name: str, file_path: str):
    doc = globals()[class_name].__doc__
    description = re.search(r"(?<=    ).*(?=\n\n    INPUTS)", doc).group(0)
    inputs = re.search(r"(?<=INPUTS\n    )(.|\n)*?(?=(\n    OUTPUTS|$))", doc).group(0)
    inputs = inputs.split("    ")
    inputs = inputs[:-1]
    inputs = ["* " + input.strip() for input in inputs]
    with open(file_path, "a", encoding="utf-8") as f:
        f.write(f"""#### {name}
{description} This class is parametrized with the following inputs:
""")    
        inputs = "  \n".join(inputs)
        f.write(inputs + "  \n\n")

def document_xml(name: str, sample_xml_path: str, file_path: str):
    parametrization_xml = xml.etree.ElementTree.parse(sample_xml_path)
    sample_parametrization = "\n".join(
        textwrap.wrap(
            inspect.cleandoc(
                xml.etree.ElementTree.tostring(
                    parametrization_xml.getroot()).decode("utf-8")),
            120,
            replace_whitespace=False
            )
        )
    with open(file_path, "a", encoding="utf-8") as f: 
        f.write(f"""## {name}  
The following gives a sample parametrization of the `XPPP` component.  
```xml
{sample_parametrization}
````  
""")

readme_path = os.path.join("model", "variant", "XPPP", "README.md")
mc_xml_path = os.path.join("model", "variant", "mc.xml")
sample_xml_path = os.path.join("model", "variant", "XPPP", "sample.xml")

base.documentation.document_component(
    XPPP.XPPP("XPPP", None, None),
    readme_path,
    mc_xml_path
)
document_xml("Parametrization", sample_xml_path, readme_path)
with open(readme_path, "a", encoding="utf-8") as f: 
    f.write("### Parameters\n")
document_class("PPMCalendar", "PPMCalendar", readme_path)
document_class("ApplicationWindow", "ApplicationWindowDistribution", readme_path)
document_class("Tank", "Tank", readme_path)
document_class("PPP", "PPP", readme_path)
document_class("Application", "Application", readme_path)
document_class("Technology", "Technology", readme_path)
with open(readme_path, "a", encoding="utf-8") as f: 
    f.write("### Random variables\n")
document_class("Normal distribution", "NormalDistribution", readme_path)
document_class("Uniform distribution", "UniformDistribution", readme_path)
document_class("Discrete uniform distribution", "DiscreteUniformDistribution", readme_path)
document_class("Choice distribution", "ChoiceDistribution", readme_path)