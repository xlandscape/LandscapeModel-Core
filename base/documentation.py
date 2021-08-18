"""
This file contains functions for automatically documenting parts Landscape Model code.
"""
import datetime
import inspect
import base
import attrib
import xml.etree.ElementTree
import textwrap


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


def write_changelog(name, version_history, file_path):
    """
    Writes an updated changelog according to the version history stored along with the code.
    :param name: The name of the documented Landscape Model part.
    :param version_history: The version history containing the individual changes per version.
    :param file_path: The path of file where the changelog is written to.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\n")
        f.write("This is the changelog for the {}. It was automatically created on {}.".format(
            name,
            datetime.date.today()
        ))
        for version in version_history:
            f.write(
                "\n\n## [{}]{}\n\n".format(version, "" if version.date is None else " - {}".format(version.date)))
            f.write("### Added\n")
            for message in version.additions:
                f.write("- {}\n".format(message))
            f.write("\n### Changed\n")
            for message in version.changes:
                f.write("- {}\n".format(message))
            f.write("\n### Fixed\n")
            for message in version.fixes:
                f.write("- {}\n".format(message))


def document_components(components_module, file_path):
    """
    Documents the components included in the Landscape Model core.
    :param components_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Components\n")
        f.write("This file lists all components that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in components_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Component):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return


def document_observers(observers_module, file_path):
    """
    Documents the observers included in the Landscape Model core.
    :param observers_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Observers\n")
        f.write("This file lists all observers that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in observers_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Observer):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return


def document_stores(stores_module, file_path):
    """
    Documents the stores included in the Landscape Model core.
    :param stores_module: The module containing the stores.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Stores\n")
        f.write("This file lists all stores that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in stores_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Store):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return


def document_component(component, file_path, sample_configuration, sample_component_name=None):
    """
    :param component: The component to document.
    :param file_path: The path of file where the readme is written to.
    :param sample_configuration: The path to a configuration file where the component is configured.
    :param sample_component_name: The name of the component in the sample configuration if it does not equal the
    component name.
    :return: Nothing.
    """
    module_doc = "" if component.module.doc_file is None else "(see `" + component.module.doc_file + "` for details)"
    configuration_xml = xml.etree.ElementTree.parse(sample_configuration)
    component_name = component.name if sample_component_name is None else sample_component_name
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("""## Table of Contents
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
{about}  
This is an automatically generated documentation based on the available code and in-line documentation. The current
version of this document is from {current_date}.  

### Built with
* Landscape Model core version {core_version}
* {module_name} version {module_version} {module_doc_file}


## Getting Started
The component can be used in any Landscape Model based on core version {core_version} or newer. See the Landscape Model
core's `README` for general tips on how to add a component to a Landscape Model.

### Prerequisites
A model developer that wants to add the `{component_name}` component to a Landscape Model needs to set up the general 
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation
1. Copy the `{component_name}` component into the `model\\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module={component_module}` and 
   `class={component_class}`. 


## Usage
The following gives a sample configuration of the `{component_name}` component. See [inputs](#inputs) and 
[outputs](#outputs) for further details on the component's interface.
```xml
{sample_configuration}
```

### Inputs
""".format(
            about=inspect.cleandoc(component.__doc__),
            current_date=datetime.date.today(),
            core_version=base.VERSION.latest,
            module_name=component.module.name,
            module_version=component.module.version,
            module_doc_file=module_doc,
            component_name=component.name,
            component_module=component.__module__,
            component_class=type(component).__name__,
            sample_configuration="\n".join(
                textwrap.wrap(
                    inspect.cleandoc(
                        xml.etree.ElementTree.tostring(
                            configuration_xml.getroot().find("Composition").find(component_name)).decode("utf-8")),
                    120,
                    replace_whitespace=False
                ))
        ))
        for component_input in component.inputs:
            f.write("#### {}\n".format(component_input.name))
            if component_input.description:
                f.write("{}  \n".format(inspect.cleandoc(component_input.description)))
            for attribute in component_input.attributes:
                if type(attribute) is attrib.Class:
                    f.write("`{}` expects its values to be of type `{}`.\n".format(
                        component_input.name,
                        attribute.type if isinstance(attribute.type, str) else attribute.type.__name__
                    ))
                elif type(attribute) is attrib.Scales:
                    f.write("Values have to refer to the `{}` scale.\n".format(attribute.scales))
                elif type(attribute) is attrib.Unit:
                    if attribute.unit is None:
                        f.write("Values of the `{}` input may not have a physical unit.\n".format(component_input.name))
                    else:
                        f.write("The physical unit of the `{}` input values is `{}`.\n".format(
                            component_input.name, attribute.unit))
                elif type(attribute) is attrib.InList:
                    f.write("Allowed values are: {}.\n".format(
                        ", ".join(["`" + str(x) + "`" for x in attribute.values])))
                elif type(attribute) is attrib.Equals:
                    f.write("The currently only allowed value is {}.\n".format(attribute.value))
                else:
                    raise TypeError("Unsupported attribute type: " + str(type(attribute)))
            f.write("\n")
        f.write("### Outputs\n")
        for component_output in component.outputs:
            f.write("#### {}\n".format(component_output.name))
            if component_output.description:
                f.write("{}  \n".format(inspect.cleandoc(component_output.description)))
            for attribute, value in component_output.attribute_hints.items():
                if attribute == "type":
                    f.write("Values are expectedly of type `{}`.\n".format(
                        value if isinstance(value, str) else value.__name__))
                elif attribute == "shape":
                    f.write("Value representation is in a {}-dimensional array.\n".format(len(value)))
                    for i in range(len(value)):
                        f.write("Dimension {} spans {}.\n".format(i + 1, value[i]))
                elif attribute == "chunks":
                    f.write("Chunking of the array is {}.\n".format(value))
                elif attribute == "data_type":
                    f.write("Individual array elements have a type of `{}`.\n".format(value.__name__))
                else:
                    raise ValueError("Unsupported default attribute: " + attribute)
            for attribute, value in component_output.default_attributes.items():
                if attribute == "data_type":
                    f.write("Individual array elements have a type of `{}`.\n".format(value.__name__))
                elif attribute == "scales":
                    f.write("The values apply to the following scale: `{}`.\n".format(value))
                elif attribute == "unit":
                    if value is None:
                        f.write("Values have no physical unit.\n")
                    else:
                        f.write("The physical unit of the values is `{}`.\n".format(value))
                elif attribute == "default":
                    f.write("The default value of the output is `{}`.\n".format(value))
                else:
                    raise ValueError("Unsupported default attribute: " + attribute)
        f.write("\n\n## Roadmap\n")
        if len(component.VERSION.roadmap) == 0:
            f.write("The `{}` component is stable. No further development takes place at the moment.\n".format(
                component.name))
        else:
            f.write("The following changes will be part of future `{}` versions:\n".format(component.name))
            for item in component.VERSION.roadmap:
                f.write(inspect.cleandoc("* " + item) + "\n")
        f.write("""

## Contributing
Contributions are welcome. Please contact the authors (see [Contact](#contact)). Also consult the `CONTRIBUTING` 
document for more information.


## License
Distributed under the CC0 License. See `LICENSE` for more information.


## Contact
""")
        for author in component.VERSION.authors:
            f.write(author + "  \n")
        f.write("\n\n## Acknowledgements\n")
        for acknowledgement in component.VERSION.acknowledgements:
            f.write("* " + acknowledgement + "  \n")
    return


def write_contribution_notes(file_path):
    """
    Writes contribution notes for a software project.
    :param file_path: The path of file where the contribution notes are written to.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("""# Contributing
Contributions to the project are welcome. Please contact the authors.  
These contribution notes refer to the general Landscape Model contribution guidelines and were written on {}. 
""".format(datetime.date.today()))
    return


def document_scenario(info_file, file_path):
    """
    :param info_file: The path of scenario information file.
    :param file_path: The path where the readme file is written to.
    :return: Nothing.
    """
    scenario_info = xml.etree.ElementTree.parse(info_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("""## Table of Contents
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
{about}
This is an automatically generated documentation based on the available scenario metadata. The current version of this 
document is from {current_date}.

### Built with
The scenario can be used in the following Landscape Models:
""".format(about=inspect.cleandoc(scenario_info.find("Description").text), current_date=datetime.date.today()))
        for version in scenario_info.findall("SupportedRuntimeVersions/Version"):
            f.write("* {} version {} and higher\n\n\n".format(version.attrib["variant"], version.attrib["number"]))
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
            f.write("* `:{}` (version {})\n".format(item.attrib["name"], item.attrib["version"]))
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
            f.write("* " + contact.text + "\n")
        f.write("\n\n## Acknowledgements\n")
        for acknowledgement in scenario_info.findall("Acknowledgements/Acknowledgement"):
            f.write("* {}\n".format(acknowledgement.text))
    return


def write_scenario_changelog(info_file, file_path):
    """
    Writes an updated scenario changelog according to the version history stored in the scenario info file.
    :param info_file: The path of scenario information file.
    :param file_path: The path of file where the changelog is written to.
    :return: Nothing.
    """
    scenario_info = xml.etree.ElementTree.parse(info_file)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\nThis list contains all additions, changes and fixes for the scenario.\n")
        f.write("It was automatically created on {}".format(datetime.date.today()))
        for version in scenario_info.findall("Changelog/Version"):
            f.write("\n\n## [{}] - {}\n### Added\n".format(version.attrib["number"], version.attrib["date"]))
            for addition in version.findall("Addition"):
                f.write("- {}\n".format(addition.text))
            f.write("\n###Changed\n")
            for change in version.findall("Change"):
                f.write("- {}\n".format(change.text))
            f.write("\n###Fixed\n")
            for fix in version.findall("Fix"):
                f.write("- {}\n".format(fix.text))
