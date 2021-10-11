"""
This file contains functions for automatically documenting parts Landscape Model code.
"""
import datetime
import inspect
import base
import attrib
import xml.etree.ElementTree
import textwrap
import types
import typing


# CHANGELOG
base.VERSION.added("1.4.9", "`base.documentation` ")
base.VERSION.added("1.5.0", "`base.documentation` methods for documenting components")
base.VERSION.added("1.5.1", "`base.documentation` methods for documenting scenarios")
base.VERSION.added("1.5.3", "`base.documentation.write_changelog()` no longer escapes underscores")
base.VERSION.added("1.5.7", "`base.documentation.document_component()` documentation of `Equals` attribute")
base.VERSION.changed(
    "1.5.8",
    """`base.documentation.document_component()` can now handle sample configurations with component names differing 
    from object name"""
)
base.VERSION.changed(
    "1.5.8",
    """`base.documentation.document_component()`: long lines in XML samples are now wrapped to ensure 120 character 
    width"""
)
base.VERSION.added(
    "1.5.8",
    "`base.documentation.document_component()` documentation of data_type attribute hint and default attribute"
)
base.VERSION.added(
    "1.5.10", "`base.documentation.document_component()` support for documentation of unit attribute hint")
base.VERSION.added("1.7.0", "Type hints to `base.documentation` ")
base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.documentation` ")


def write_changelog(name: str, version_history: base.VersionCollection, file_path: str) -> None:
    """
    Writes an updated changelog according to the version history stored along with the code.
    :param name: The name of the documented Landscape Model part.
    :param version_history: The version history containing the individual changes per version.
    :param file_path: The path of file where the changelog is written to.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\n")
        f.write(f"This is the changelog for the {name}. It was automatically created on {datetime.date.today()}.")
        for version in version_history:
            if version.date is None:
                f.write(f"\n\n## [{version}]\n\n")
            else:
                f.write(f"\n\n## [{version}] - {version.date}\n\n")
            f.write("### Added\n")
            for message in version.additions:
                f.write(f"- {message}\n")
            f.write("\n### Changed\n")
            for message in version.changes:
                f.write(f"- {message}\n")
            f.write("\n### Fixed\n")
            for message in version.fixes:
                f.write(f"- {message}\n")


def document_components(components_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the components included in the Landscape Model core.
    :param components_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Components\n")
        f.write("This file lists all components that are currently included in the Landscape Model core.\n")
        f.write(f"It was automatically created on {datetime.date.today()}.\n")
        for name, member in components_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Component):
                f.write(f"\n\n## {name}")
                f.write(member.__doc__)


def document_observers(observers_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the observers included in the Landscape Model core.
    :param observers_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Observers\n")
        f.write("This file lists all observers that are currently included in the Landscape Model core.\n")
        f.write(f"It was automatically created on {datetime.date.today()}.\n")
        for name, member in observers_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Observer):
                f.write(f"\n\n## {name}")
                f.write(member.__doc__)


def document_stores(stores_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the stores included in the Landscape Model core.
    :param stores_module: The module containing the stores.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Stores\n")
        f.write("This file lists all stores that are currently included in the Landscape Model core.\n")
        f.write(f"It was automatically created on {datetime.date.today()}.\n")
        for name, member in stores_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Store):
                f.write(f"\n\n## {name}")
                f.write(member.__doc__)


def document_component(
        component: base.Component,
        file_path: str,
        sample_configuration: str,
        sample_component_name:
        typing.Optional[str] = None
) -> None:
    """
    :param component: The component to document.
    :param file_path: The path of file where the readme is written to.
    :param sample_configuration: The path to a configuration file where the component is configured.
    :param sample_component_name: The name of the component in the sample configuration if it does not equal the
    component name.
    :return: Nothing.
    """
    module_doc = "" if component.module.doc_file is None else f"(see `{component.module.doc_file}` for details)"
    configuration_xml = xml.etree.ElementTree.parse(sample_configuration)
    component_name = component.name if sample_component_name is None else sample_component_name
    sample_configuration = "\n".join(
        textwrap.wrap(
            inspect.cleandoc(
                xml.etree.ElementTree.tostring(
                    configuration_xml.getroot().find("Composition").find(component_name)).decode("utf-8")),
            120,
            replace_whitespace=False
        )
    )
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""## Table of Contents
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
{inspect.cleandoc(component.__doc__)}  
This is an automatically generated documentation based on the available code and in-line documentation. The current
version of this document is from {datetime.date.today()}.  

### Built with
* Landscape Model core version {base.VERSION.latest}
* {component.module.name} version {component.module.version} {module_doc}


## Getting Started
The component can be used in any Landscape Model based on core version {base.VERSION.latest} or newer. See the Landscape
Model core's `README` for general tips on how to add a component to a Landscape Model.

### Prerequisites
A model developer that wants to add the `{component_name}` component to a Landscape Model needs to set up the general 
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation
1. Copy the `{component.name}` component into the `model\\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module={component.__module__}` and 
   `class={type(component).__name__}`. 


## Usage
The following gives a sample configuration of the `{component_name}` component. See [inputs](#inputs) and 
[outputs](#outputs) for further details on the component's interface.
```xml
{sample_configuration}
```

### Inputs
""")
        for component_input in component.inputs:
            f.write(f"#### {component_input.name}\n")
            if component_input.description:
                f.write(f"{inspect.cleandoc(component_input.description)}  \n")
            for attribute in component_input.attributes:
                if isinstance(attribute, attrib.Class):
                    f.write(
                        f"`{component_input.name}` expects its values to be of type `"
                        f"{attribute.type if isinstance(attribute.type, str) else attribute.type.__name__}`.\n")
                elif isinstance(attribute, attrib.Scales):
                    f.write(f"Values have to refer to the `{attribute.scales}` scale.\n")
                elif isinstance(attribute, attrib.Unit):
                    if attribute.unit is None:
                        f.write(f"Values of the `{component_input.name}` input may not have a physical unit.\n")
                    else:
                        f.write(
                            f"The physical unit of the `{component_input.name}` input values is `{attribute.unit}`.\n")
                elif isinstance(attribute, attrib.InList):
                    allowed_values = ", ".join([f"`{x}`" for x in attribute.values])
                    f.write(f"Allowed values are: {allowed_values}.\n")
                elif isinstance(attribute, attrib.Equals):
                    f.write(f"The currently only allowed value is {attribute.value}.\n")
                else:
                    raise TypeError(f"Unsupported attribute type: {type(attribute)}")
            f.write("\n")
        f.write("### Outputs\n")
        for component_output in component.outputs:
            f.write(f"#### {component_output.name}\n")
            if component_output.description:
                f.write(f"{inspect.cleandoc(component_output.description)}  \n")
            for attribute, value in component_output.attribute_hints.items():
                if attribute == "type":
                    f.write(f"Values are expectedly of type `{value if isinstance(value, str) else value.__name__}`.\n")
                elif attribute == "shape":
                    f.write(f"Value representation is in a {len(value)}-dimensional array.\n")
                    for i in range(len(value)):
                        f.write(f"Dimension {i + 1} spans {value[i]}.\n")
                elif attribute == "chunks":
                    f.write(f"Chunking of the array is {value}.\n")
                elif attribute == "data_type":
                    f.write(f"Individual array elements have a type of `{value.__name__}`.\n")
                elif attribute == "unit":
                    f.write(f"Values expectedly have a unit of `{value}`.\n")
                else:
                    raise ValueError(f"Unsupported default attribute: {attribute}")
            for attribute, value in component_output.default_attributes.items():
                if attribute == "data_type":
                    f.write(f"Individual array elements have a type of `{value.__name__}`.\n")
                elif attribute == "scales":
                    f.write(f"The values apply to the following scale: `{value}`.\n")
                elif attribute == "unit":
                    if value is None:
                        f.write("Values have no physical unit.\n")
                    else:
                        f.write(f"The physical unit of the values is `{value}`.\n")
                elif attribute == "default":
                    f.write(f"The default value of the output is `{value}`.\n")
                else:
                    raise ValueError(f"Unsupported default attribute: {attribute}")
        f.write("\n\n## Roadmap\n")
        if len(component.VERSION.roadmap) == 0:
            f.write(f"The `{component.name}` component is stable. No further development takes place at the moment.\n")
        else:
            f.write(f"The following changes will be part of future `{component.name}` versions:\n")
            for item in component.VERSION.roadmap:
                clean_doc = inspect.cleandoc(f"* {item}")
                f.write(f"{clean_doc}\n")
        f.write("""

## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)). Also consult the `CONTRIBUTING` 
document for more information.


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact
""")
        for author in component.VERSION.authors:
            f.write(f"{author}  \n")
        f.write("\n\n## Acknowledgements\n")
        for acknowledgement in component.VERSION.acknowledgements:
            f.write(f"* {acknowledgement}  \n")


def write_contribution_notes(file_path: str) -> None:
    """
    Writes contribution notes for a software project.
    :param file_path: The path of file where the contribution notes are written to.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""# Contributing
Contributions to the project are welcome. Please contact the authors. These contribution notes refer to the general 
Landscape Model contribution guidelines and were written on {datetime.date.today()}. 
""")


def document_scenario(info_file: str, file_path: str) -> None:
    """
    :param info_file: The path of scenario information file.
    :param file_path: The path where the readme file is written to.
    :return: Nothing.
    """
    scenario_info = xml.etree.ElementTree.parse(info_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""## Table of Contents
* [About the project](#about-the-project)
  * [Built With](#built-with)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)


## About the project
{inspect.cleandoc(scenario_info.find('Description').text)}
This is an automatically generated documentation based on the available scenario metadata. The current version of this 
document is from {datetime.date.today()}.

### Built with
The scenario can be used in the following Landscape Models:
""")
        for version in scenario_info.findall("SupportedRuntimeVersions/Version"):
            f.write(f"* {version.attrib['variant']} version {version.attrib['number']} and higher\n\n\n")
        f.write("""## Getting Started
### Prerequisites
Make sure you use the latest version of the Landscape Model.

### Installation
Copy the complete scenario folder unaltered into the `scenario` sub-directory of your model. Reference the scenario
from the model parameterization. For details how to reference the scenario from the user parameterization, see the 
`README` of the model.


## Usage
The scenario adds the following macros to the Landscape Model:
""")
        for item in scenario_info.findall("Content/Item"):
            f.write(f"* `:{item.attrib['name']}` (version {item.attrib['version']})\n")
        f.write("""
### Roadmap
The scenario is final and not further developed. It will be, however, updated to reflect new requirements by the 
Landscape Model core and individual Landscape Model variants.


## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)) and see the `CONTRIBUTING` document.


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact
""")
        for contact in scenario_info.findall("Contacts/Contact"):
            f.write(f"* {contact.text}\n")
        f.write("\n\n## Acknowledgements\n")
        for acknowledgement in scenario_info.findall("Acknowledgements/Acknowledgement"):
            f.write(f"* {acknowledgement.text}\n")


def write_scenario_changelog(info_file: str, file_path: str) -> None:
    """
    Writes an updated scenario changelog according to the version history stored in the scenario info file.
    :param info_file: The path of scenario information file.
    :param file_path: The path of file where the changelog is written to.
    :return: Nothing.
    """
    scenario_info = xml.etree.ElementTree.parse(info_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\nThis list contains all additions, changes and fixes for the scenario.\n")
        f.write(f"It was automatically created on {datetime.date.today()}")
        for version in scenario_info.findall("Changelog/Version"):
            f.write(f"\n\n## [{version.attrib['number']}] - {version.attrib['date']}\n### Added\n")
            for addition in version.findall("Addition"):
                f.write(f"- {addition.text}\n")
            f.write("\n###Changed\n")
            for change in version.findall("Change"):
                f.write(f"- {change.text}\n")
            f.write("\n###Fixed\n")
            for fix in version.findall("Fix"):
                f.write(f"- {fix.text}\n")
