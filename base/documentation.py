"""This file contains functions for automatically documenting parts Landscape Model code."""
import builtins
import distutils.version
import datetime
import inspect
import base
import attrib
import xml.etree.ElementTree
import textwrap
import types
import typing
import os
import configparser
import urllib.request
import json

# CHANGELOG
base.VERSION.added("1.4.9", "`base.documentation`")
base.VERSION.added("1.5.0", "`base.documentation` methods for documenting components")
base.VERSION.added("1.5.1", "`base.documentation` methods for documenting scenarios")
base.VERSION.added("1.5.3", "`base.documentation.write_changelog()` no longer escapes underscores")
base.VERSION.added("1.5.7", "`base.documentation.document_component()` documentation of `Equals` attribute")
base.VERSION.changed(
    "1.5.8",
    "`base.documentation.document_component()` can now handle sample configurations with component names differing "
    "from object name"
)
base.VERSION.changed(
    "1.5.8",
    "`base.documentation.document_component()`: long lines in XML samples are now wrapped to ensure 120 character "
    "width"
)
base.VERSION.added(
    "1.5.8",
    "`base.documentation.document_component()` documentation of data_type attribute hint and default attribute"
)
base.VERSION.added(
    "1.5.10", "`base.documentation.document_component()` support for the documentation of unit attribute hints")
base.VERSION.added("1.7.0", "Type hints to `base.documentation`")
base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.documentation`")
base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.documentation`")
base.VERSION.fixed("1.9.3", "Formatting of generated scenario documentation in `base.documentation`")
base.VERSION.added("1.9.6", "Function for template-based documentation of model variants to `base.documentation`")
base.VERSION.added(
    "1.9.1", "Arguments to `documentation.document_variant` to specify variant name and endpoint flexibly")
base.VERSION.changed("1.10.3", "Spell checking in `base.documentation`")
base.VERSION.changed("1.12.1", "Extended CONTRIBUTING.md in `base.documentation`")
base.VERSION.fixed("1.12.2", "Typos in `base.documentation`")
base.VERSION.added("1.12.2", "Step to merge request instructions in `base.documentation`")
base.VERSION.changed("1.12.5", "Enhanced contribution documentation in `base.documentation`")
base.VERSION.changed("1.12.6", "Refactored documentation of class members into own function in `base.documentation`")
base.VERSION.fixed("1.13.0", "Spelling error in `base.documentation`")
base.VERSION.changed("1.13.1", "Text wrapping of member documentation in `base.documentation`")
base.VERSION.changed("1.14.3", "Normalized whitespace for creating documentations")
base.VERSION.added("1.15.0", "Functions to check variant parts and to write repository info for documentation")
base.VERSION.fixed("1.15.1", "Documentation of scenario respects XML namespace")
base.VERSION.fixed("1.15.2", "Fixed resolution of git-paths of submodules")
base.VERSION.changed("1.15.4", "Documentation of core components lists component's inputs and their attributes")
base.VERSION.changed("1.15.6", "Updated installation notes in model documentation")
base.VERSION.added("1.15.6", "User warning regarding non-documented modules during scenario documentation")
base.VERSION.added("1.15.8", "Documentation of outputs for components in core")
base.VERSION.changed(
    "1.15.9", "Documentation of outputs for components in core and external components now uses the same code")


def write_changelog(name: str, version_history: base.VersionCollection, file_path: str) -> None:
    """
    Writes an updated changelog according to the version history stored along with the code.

    Args:
        name: The name of the documented Landscape Model part.
        version_history: The version history containing the individual changes for each version.
        file_path: The path of file where the changelog is written to.

    Returns:
        Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\n\n")
        f.write(f"This is the changelog for the {name}. It was automatically created on {datetime.date.today()}.\n")
        for version in version_history:
            if version.date is None:
                f.write(f"\n## [{version}]\n\n")
            else:
                f.write(f"\n## [{version}] - {version.date}\n\n")
            f.write("### Added\n")
            for message in version.additions:
                formatted_text = "\n".join(textwrap.wrap(message, 120, subsequent_indent="  "))
                f.write(f"\n- {formatted_text}\n")
            f.write("\n### Changed\n")
            for message in version.changes:
                formatted_text = "\n".join(textwrap.wrap(message, 120, subsequent_indent="  "))
                f.write(f"\n- {formatted_text}\n")
            f.write("\n### Fixed\n")
            for message in version.fixes:
                formatted_text = "\n".join(textwrap.wrap(message, 120, subsequent_indent="  "))
                f.write(f"\n- {formatted_text}\n")


def document_components(components_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the components included in the Landscape Model core.

    Args:
        components_module: The module containing the components.
        file_path: The path of the output documentation file.

    Returns:
        Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Components\n\n")
        f.write("This file lists all components that are currently included in the Landscape Model core.\n")
        _document_member(components_module, f)


def _document_member(
        components_module: types.ModuleType, f: typing.TextIO, member_type: typing.Type = base.Component) -> None:
    f.write(f"It was automatically created on {datetime.date.today()}.")
    for name, member in components_module.__dict__.items():
        if inspect.isclass(member) and issubclass(member, member_type):
            f.write(f"\n\n## {name}\n\n")
            f.write(inspect.cleandoc(member.__doc__))
            if issubclass(member, base.Component):
                component = member("_tmp_", base.Observer(), None)
                f.write(f"\n\n### Inputs\n")
                for component_input in component.inputs:
                    component_input_description = "\n".join(
                        textwrap.wrap(
                            component_input.description,
                            120,
                            replace_whitespace=False
                        )
                    ) if component_input.description else ""
                    f.write(f"\n#### {component_input.name}\n\n{component_input_description}\n")
                    for i, attribute in enumerate(component_input.attributes):
                        f.write(f"\n" if i == 0 else "")
                        f.write(f"- {attribute}\n")
                _document_outputs(f, component)


def _document_outputs(f: typing.TextIO, component: base.Component) -> None:
    def _format_type(type_to_format: typing.Type) -> str:
        formatted_string = (
            "`" if type_to_format.__module__ == 'builtins' else f"`{type_to_format.__module__}.")
        return formatted_string + (
                f"{type_to_format.__qualname__}" +
                (
                    f"[{', '.join([x.__qualname__ for x in typing.get_args(type(type_to_format))])}]`"
                    if typing.get_args(type(type_to_format)) else "`"
                )
        )

    f.write(f"\n### Outputs")
    for component_output in component.outputs:
        component_output_description = "\n".join(
            textwrap.wrap(inspect.cleandoc(component_output.description), 120, replace_whitespace=False)
        ) if component_output.description else ""
        f.write(f"\n\n#### {component_output.name}\n\n{component_output_description}")
        f.write("\n" if len(component_output.default_attributes) + len(component_output.attribute_hints) > 0 else "")
        for attribute, value in component_output.default_attributes.items():
            if isinstance(value, builtins.type):
                f.write(f"\n- {attribute.title().replace('_', ' ')}: {_format_type(value)}")
            else:
                f.write(f"\n- {attribute.title().replace('_', ' ')}: `{value}`")
        for attribute, value in component_output.attribute_hints.items():
            if isinstance(value, builtins.type):
                display_value = _format_type(value)
            elif isinstance(value, str):
                display_value = value
            elif isinstance(value, typing.Sequence):
                scales = component_output.default_attributes["scales"].split(", ")
                display_value = ", ".join(
                    [
                        f"`{scales[i]}`: {_format_type(v) if isinstance(v, builtins.type) else v}"
                        for i, v in enumerate(value) if value
                    ]
                )
            else:
                display_value = f"`{value}`"
            formatted_text = "\n".join(
                textwrap.wrap(f"- {attribute.title()}: {display_value}", 120, subsequent_indent="  ")
            )
            f.write(f"\n{formatted_text}")


def document_observers(observers_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the observers included in the Landscape Model core.

    Args:
        observers_module: The module containing the components.
        file_path: The path of the output documentation file.

    Returns:
        Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Observers\n\n")
        f.write("This file lists all observers that are currently included in the Landscape Model core.\n")
        _document_member(observers_module, f, base.Observer)


def document_stores(stores_module: types.ModuleType, file_path: str) -> None:
    """
    Documents the stores included in the Landscape Model core.

    Args:
        stores_module: The module containing the stores.
        file_path: The path of the output documentation file.

    Returns:
        Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Stores\n\n")
        f.write("This file lists all stores that are currently included in the Landscape Model core.\n")
        _document_member(stores_module, f, base.Store)


def document_component(
        component: base.Component,
        file_path: str,
        sample_configuration: str,
        sample_component_name:
        typing.Optional[str] = None
) -> None:
    """
    Documents an individual Landscape Model component.
    
    Args:
        component: The component to document.
        file_path: The path of file where the readme is written to.
        sample_configuration: The path to a configuration file where the component is configured.
        sample_component_name: The name of the component in the sample configuration if it does not equal the component
            name.
    
    Returns:
        Nothing.
    """
    module_doc = "" if component.module.doc_file is None else f"(see `{component.module.doc_file}` for details)"
    configuration_xml = xml.etree.ElementTree.parse(sample_configuration)
    component_name = component.name if sample_component_name is None else sample_component_name
    sample_configuration = "\n".join(
        textwrap.wrap(
            inspect.cleandoc(
                xml.etree.ElementTree.tostring(
                    configuration_xml.getroot().find("Composition").find(component_name)
                ).decode()
            ),
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

A model developer that wants to add the `{component.name}` component to a Landscape Model needs to set up the general
structure for a Landscape Model first. See the Landscape Model core's `README` for details on how to do so.

### Installation

1. Copy the `{component.name}` component into the `model\\variant` sub-folder.
2. Make use of the component by including it into the model composition using `module={component.__module__}` and
   `class={type(component).__name__}`.

## Usage

The following gives a sample configuration of the `{component.name}` component. See [inputs](#inputs) and
[outputs](#outputs) for further details on the component's interface.

```xml
{sample_configuration}
```

### Inputs

""")
        for component_input in component.inputs:
            f.write(f"#### {component_input.name}\n\n")
            if component_input.description:
                f.write("\n".join(textwrap.wrap(inspect.cleandoc(component_input.description), 120)))
                f.write("\n")
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
        _document_outputs(f, component)
        f.write("\n## Roadmap\n\n")
        if len(component.VERSION.roadmap) == 0:
            f.write(f"The `{component.name}` component is stable. No further development takes place at the moment.\n")
        else:
            f.write(f"The following changes will be part of future `{component.name}` versions:\n\n")
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
            f.write(f"{author}\n")
        f.write("\n## Acknowledgements\n\n")
        for acknowledgement in component.VERSION.acknowledgements:
            f.write(f"* {acknowledgement}\n")


def write_contribution_notes(file_path: str) -> None:
    """
    Writes contribution notes for a software project.

    Args:
        file_path: The path of file where the contribution notes are written to.

    Returns:
        Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(f"""# Contributing

Contributions to the project are welcome. Please contact the authors. These contribution notes refer to the general
Landscape Model contribution guidelines and were written on {datetime.date.today()}.

## Issues

Whenever you identify a bug or like to suggest an enhancement to the code, please file an issue. Stick to the following
checklist when submitting an issue.

1. Check whether a similar issue already exists. If so, please comment on the existing issue instead of creating a new
   one.
2. Identify the most appropriate repository for the issue, that is the repository nearest to the presumed code changes.
   For instance, if you found a bug in the base classes, please submit it in the Landscape Model core repository or an
   enhancement of a specific component in the component's repository. If you are not sure about the most appropriate
   repository, please use the top level repository of the according model variant, e.g., xAquaticRisk or
   xOffFieldSoilRisk.
3. Give the issue a strong, self-explanatory title.
4. Provide any information in the issue's description that is needed to understand the purpose of the issue and allows
   working on it. This includes a rationale, excerpts of log files, screenshots etc. Be concise.
5. If you are going to work on the issue yourself, assign the issue to you. In any other case, assign the issue to the
   repository owner.
6. Assign one of the following labels to the issue: `bug` if the issue is related to exceptions or erroneous runtime
   behavior, `documentation` for issues related with the documentation of functionality and code, `enhancement` for
   code improvements that add to the usability or performance, or `suggestion` for ideas that should be considered part
   of the backlog or require further discussion.
7. In the case of a `bug` issue, you may additionally assign the `highPriority` label if the bug is breaking the normal
   usage of the application.
8. Whenever you start working on an issue, you should assign the label `Work in progress` to it to communicate that the
   issue is actively addressed. Likewise, if you finish work on an issue, the label `work in progress` should be
   removed before closing the issue.
9. If an issue requires additional input or is delayed for future work actions, you can mark it with the label
   `Waiting`.
10. In case another issue is blocking the work on an issue or if two issues are otherwise related, please actively link
    the issues using the according GitLab options.

## Merge requests

The Landscape Model repositories adapt the GitFlow approach for versioning (see
[A successful Git branching model](https://nvie.com/posts/a-successful-git-branching-model/) for a detailed
explanation). Briefly, there is a *master* branch that always contains the latest tested stable version (tagged with a
version number). This branch is protected and only the repository owner can push to it. To contribute to the repository,
please adhere to the following steps:

1. Locally, create a new branch starting at the newest commit of the master branch. You should do all your coding and
   modifications in this feature branch.
2. Develop in your local feature branch until you reach a state that you like to submit. This may encompass multiple
   local commits.
3. Use concise and meaningful commit messages that help to track changes.
4. If the repository gets updated during your development, please merge the new master commit into your feature branch
   and resolve merge conflicts, if any occur.
5. Make sure that all your changes are reflected in the repositories documentation and modify the documentation if
   needed.
6. Do not assign new version numbers. This will be done during the next release of the repository.
7. Test your code extensively!
8. If your code works satisfyingly, push your local feature branch to the GitLab repository.
9. Create then a merge request for your pushed branch (= source branch) into the master branch.
10. Assign the owner of the repository to the merge request.
11. Your changes will be reviewed by the owner of the repository and the merge will be performed, or you may be asked
    for additional modifications of your code.

## Components

If you are requesting a merge containing component code, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The repository can be cloned from GitLab.
- [ ] The component runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.
- [ ] You haven't introduced inputs to the component that are not needed for calculations.

## Model variant

If you are requesting a merge relating to a model variant, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The entire model, including all submodules, can be cloned from GitLab.
- [ ] The model runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.

## Scenario

If you are requesting a merge relating to a scenario, please make sure that the following applies:

- [ ] The commit that is requested to branch is based on the most recent commit on the master branch.
- [ ] The repository can be cloned from GitLab.
- [ ] The component runs successfully without any errors using the most recent model version.
- [ ] You haven't reverted any changes made by other contributors unless there is a good reason to do so.
- [ ] Added data is required, cannot be retrieved by a component and is not redundant.

""")


def document_scenario(info_file: str, file_path: str, xml_namespace: str = "urn:xLandscapeModelScenarioInfo") -> None:
    """
    Documents a Landscape Model scenario.

    Args:
        info_file: The path of scenario information file.
        file_path: The path where the readme file is written to.
        xml_namespace: The default namespace for the scenario metadata.

    Returns:
        Nothing.
    """
    namespace = {"": xml_namespace}
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
{inspect.cleandoc(scenario_info.find('Description', namespace).text)}
This is an automatically generated documentation based on the available scenario metadata. The current version of this 
document is from {datetime.date.today()}.

### Built with
The scenario can be used in the following Landscape Models:
""")
        for version in scenario_info.findall("SupportedRuntimeVersions/Version", namespace):
            f.write(f"* {version.attrib['variant']} version {version.attrib['number']} and higher\n\n\n")
        f.write("""## Getting Started
### Prerequisites
Make sure you use the latest version of the Landscape Model.

### Installation
Copy the complete scenario folder unaltered into the `scenario` subdirectory of your model. Reference the scenario
from the model parameterization. For details how to reference the scenario from the user parameterization, see the 
`README` of the model.


## Usage
The scenario adds the following macros to the Landscape Model:
""")
        for item in scenario_info.findall("Content/Item", namespace):
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
        for contact in scenario_info.findall("Contacts/Contact", namespace):
            f.write(f"* {contact.text}\n")
        f.write("\n\n## Acknowledgements\n")
        for acknowledgement in scenario_info.findall("Acknowledgements/Acknowledgement", namespace):
            f.write(f"* {inspect.cleandoc(acknowledgement.text)}\n")
    raise UserWarning(
        "Geospatial data of the scenario, made available through the LandscapeScenario component, is currently "
        "not documented"
    )


def write_scenario_changelog(
        info_file: str,
        file_path: str,
        xml_namespace: str = "urn:xLandscapeModelScenarioInfo"
) -> None:
    """
    Writes an updated scenario changelog according to the version history stored in the scenario info file.

    Args:
        info_file: The path of scenario information file.
        file_path: The path of file where the changelog is written to.
        xml_namespace: The default namespace for the scenario metadata.

   Returns:
       Nothing.
    """
    scenario_info = xml.etree.ElementTree.parse(info_file)
    namespace = {"": xml_namespace}
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\nThis list contains all additions, changes and fixes for the scenario.\n")
        f.write(f"It was automatically created on {datetime.date.today()}")
        for version in scenario_info.findall("Changelog/Version", namespace):
            f.write(f"\n\n## [{version.attrib['number']}] - {version.attrib['date']}\n### Added\n")
            for addition in version.findall("Addition", namespace):
                f.write(f"- {inspect.cleandoc(addition.text)}\n")
            f.write("\n###Changed\n")
            for change in version.findall("Change", namespace):
                f.write(f"- {inspect.cleandoc(change.text)}\n")
            f.write("\n###Fixed\n")
            for fix in version.findall("Fix", namespace):
                f.write(f"- {inspect.cleandoc(fix.text)}\n")


def document_variant(template_file: str, file_path: str, variant_name: str, repository_endpoint: str) -> None:
    """
    Documents a Landscape Model variant based on a template README.

    Args:
        template_file: The file path to the README template, containing macros.
        file_path: The file path for the final README with resolved macros.
        variant_name: The name of the model variant.
        repository_endpoint: The URI of the main code repository for the variant

    Returns:
        Nothing.
    """
    base.replace_tokens(
        {
            "current_date": str(datetime.date.today()),
            "installation_notes": """#### From zipfile
If someone provides you with a zipped version of $(variant_name), simply extract the archive into a folder on your 
hard drive. Simulation data and temporary files will be written to a sub-folder of this folder, so a fast hard-drive 
with lots of available space is preferable.

#### From GitHub.com using Sourcetree
The newest stable version of $(variant_name) can be found at GitHub.com. You can access the git repository with any git 
client, including command-line and graphical clients. The following is a step-by-step guide to retrieve a copy of 
$(variant_name) using the graphical git client *Sourcetree*.

1. Download *Sourcetree* from the *Atlassian* website: 
   [https://www.sourcetreeapp.com/](https://www.sourcetreeapp.com/).
2. During setup of *Sourcetree*, you can skip the registration of a *Bitbucket* account. It is also not necessary to
   install the *Mercurial* tools. Under *Preferences*, provide your username and email address as they should appear in
   your commits to the git repository. When asked to load an SSH key, select "No".
3. After setting up, take the time to tweak some *Sourcetree* options under *Tools* > *Options*. Important options that
   are suggested to be changed are enabling of *Perform submodule actions recursively* in the *Git* tab and to make sure
   that an embedded git is used by pressing the *Embedded* button in the *Git* tab and confirming the download. The
   submodule recursive actions will make it easier to update the repository later on and the embedded git will make 
   sure that you use a current git version that supports all necessary features.
4. After closing the *Options* dialog, switch to the *Clone* tab to finally clone the repository. Under 
   *Source Path / URL*, type in the $(variant_name) endpoint which is *$(repository_endpoint)*.  After the input field 
   looses focus, *Sourcetree* should indicate that *This is a Git repository*.
5. Under *Destination Path*, specify the folder on your computer where the repository should be cloned into. The *Name*
    field should be automatically filled out and equal the name of the folder where the repository is cloned into. The
    *Local Folder* is fixed to *[Root]*. Under *Advanced Options*, make sure that the *Checkout branch* is set to
    *master* to assure that you clone the latest stable version. **Make sure that the option *Recurse submodules* is
    enabled** to download the entire Landscape Model and not only part of its. Confirm everything by pressing the
    *Clone* button.
6. After cloning is finished, you can find your copy of the Landscape Model variant in the specified folder and can 
    start using it.
            """,
            "variant_name": variant_name,
            "repository_endpoint": repository_endpoint
        },
        template_file,
        file_path
    )


def check_variant_parts(variant_root_dir: str) -> None:
    """
    Checks whether all parts used by the model are documented.

    Args:
        variant_root_dir: The root directory of the model variant.

    Returns:
        None.
    """
    experiment_config = xml.etree.ElementTree.parse(
        os.path.join(variant_root_dir, "..", "..", "variant", "experiment.xml")).getroot()
    mc_config = xml.etree.ElementTree.parse(
        experiment_config.find(
            "General").find("MCRunTemplate").text.replace("$(_X3DIR_)", variant_root_dir)).getroot()
    documented_parts = {(x.attrib["module"], x.attrib["class"]) for x in experiment_config.find("Parts")}
    configured_parts = {
        x for x in (
                {(x.attrib["module"], x.attrib["class"]) for x in experiment_config.findall("Observers/Observer")} |
                {(x.attrib["module"], x.attrib["class"]) for x in mc_config.findall("Observers/Observer")} |
                {(x.attrib["module"], x.attrib["class"]) for x in mc_config.findall("Composition/*")}
        ) if x[0] not in ("observer", "components")
    }
    for part in documented_parts - configured_parts:
        raise ValueError(f"Module {part[0]}, class {part[1]} is documented but not configured")
    for part in configured_parts - documented_parts:
        raise ValueError(f"Module {part[0]}, class {part[1]} is configured but not documented")
    return


def write_repository_info(
        repository_path: str,
        info_file: str,
        target_versions: str,
        part_type: str,
        code_style_compliance: typing.Optional[distutils.version.StrictVersion] = None
) -> None:
    """
    Writes information about the repository into a file.

    Args:
        repository_path: The path of the repository.
        info_file: The file to write the output to.
        target_versions: The JSON file containing the version information.
        part_type: The type of repository.
        code_style_compliance: An indicator for code style compliance.

    Returns:
        None.
    """
    git_path_or_file = os.path.join(repository_path, ".git")
    git_config_file = os.path.join(git_path_or_file, "config")
    git_config = configparser.ConfigParser()
    if os.path.exists(git_config_file):
        git_config.read(git_config_file)
    else:
        with open(git_path_or_file, encoding="ascii") as f:
            git_reference = os.path.join(repository_path, f.read().removeprefix("gitdir: ").rstrip(), "config")
        git_config.read(git_reference)
    repository_info = json.loads(
        urllib.request.urlopen(
            git_config['remote "origin"']["url"].replace(
                "https://github.com/", "https://api.github.com/repos/").removesuffix(".git")).read())
    branch_info = json.loads(urllib.request.urlopen(repository_info["branches_url"].removesuffix("{/branch}")).read())
    branches = [x["name"] for x in branch_info]
    gitflow = (
            ("main" in branches or "master" in branches) and
            "develop" in branches and
            all([
                x in ("main", "master", "develop") or
                x.startswith("feature/") or
                x.startswith("release/") or
                x.startswith("hotfix/") for x in branches
            ])
    )
    with open(target_versions, encoding="utf-8") as f:
        target_versions_info = json.load(f)
    with open(info_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "info_created": str(datetime.date.today()),
                "visibility": repository_info["visibility"],
                "license": repository_info["license"]["spdx_id"],
                "issues_enabled": repository_info["has_issues"],
                "description": repository_info["description"],
                "website": repository_info["homepage"],
                "topics": repository_info["topics"],
                "wiki_enabled": repository_info["has_wiki"],
                "discussions_enabled": repository_info["has_discussions"],
                "projects_enabled": repository_info["has_projects"],
                "default_branch": repository_info["default_branch"],
                "gitflow": gitflow,
                "code_style_compliance": (
                        isinstance(code_style_compliance, distutils.version.StrictVersion) and
                        code_style_compliance >= target_versions_info["code_style"]
                ),
                "latest_changelog_processor": target_versions_info["changelog"],
                "latest_readme_processor": target_versions_info["readme"][part_type],
                "latest_contributing_processor": target_versions_info["contributing"],
                "branch_protection": all(
                    [x["protected"] for x in branch_info if x["name"] == repository_info["default_branch"]])
            },
            f,
            indent=2
        )


def write_latest_version_info(version_file: str) -> None:
    """
    Write information about the latest version to a file.

    Args:
        version_file: The file to write to.

    Returns:
        None.
    """
    with open(version_file, "w", encoding="utf-8") as f:
        json.dump({}, f)
