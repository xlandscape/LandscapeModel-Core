"""
Class definition of a Landscape Module project.
"""
import os
import xml.etree.ElementTree
import base
import typing
import xmlschema


class Project:
    """
    A Landscape Module project.
    """
    # CHANGELOG
    base.VERSION.added("1.2.1", "`base.Project` class for representing Landscape Model scenarios")
    base.VERSION.changed("1.3.5", "`base.Project` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Project`")
    base.VERSION.added("1.4.1", "`base.Project.version`")
    base.VERSION.changed("1.5.3", "`base.Project` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Project`")
    base.VERSION.changed("1.9.10", "`base.Project` can handle outsourced package parts")
    base.VERSION.added("1.15.0", "XML validation of scenario metadata")
    base.VERSION.changed("1.15.5", "Raise clearer error message if scenario XML does not use the right XML namespace")
    base.VERSION.changed("1.18.0", "Code refactory in `base.Project`")

    # noinspection PyTypeChecker
    def __init__(self, project: str, project_dir: str, prefix: str = ":") -> None:
        self._content = {}
        self._path = os.path.join(project_dir, project)
        namespace = {"": "urn:xLandscapeModelScenarioInfo"}
        project_info = os.path.join(self._path, "scenario.xproject")
        if xmlschema.XMLResource(project_info).namespace != "urn:xLandscapeModelScenarioInfo":
            raise ValueError("scenario XML invalid: root element is not in namespace urn:xLandscapeModelScenarioInfo")
        schema = os.path.join(os.path.dirname(base.__file__), "scenario.xsd")
        xmlschema.XMLSchema(schema).validate(project_info)
        config = xml.etree.ElementTree.parse(project_info).getroot()
        for entry in config.find("Content", namespace).findall("Item", namespace):
            file_path = os.path.join(project_dir, project, entry.attrib["target"])
            if "outsourced" in entry.attrib and entry.attrib["outsourced"].lower() == "true":
                if not os.path.exists(file_path):
                    raise FileNotFoundError(
                        f"A part of the scenario '{project}', '{entry.attrib['name']}', is not included in this "
                        f"distribution. You have to download this part separately and place it within the scenario "
                        f"folder, so that {file_path} can be resolved. Make sure that the version number of the "
                        f"missing part is {entry.attrib['version']}, as this is the version with which the scenario "
                        f"was build. Other versions of the part might not work as expected."
                    )
            self._content[prefix + entry.attrib["name"]] = file_path
        self._version = config.find("Version", namespace).text
        self._name = config.find("Name", namespace).text
        self._supported_runtimes = {}
        for runtime in config.findall("SupportedRuntimeVersions/Version", namespace):
            self._supported_runtimes.setdefault(runtime.attrib["variant"], set()).add(runtime.attrib["number"])
        return

    @property
    def content(self) -> dict[str, typing.Any]:
        """
        The content of the project.
        :return: A dictionary of named items that are part of the project.
        """
        return self._content

    @property
    def path(self) -> str:
        """
        The path where the scenario is located.
        """
        return self._path

    @property
    def version(self) -> typing.Optional[str]:
        """
        The version of the scenario.
        """
        return self._version

    @property
    def name(self) -> str:
        """
        The name of the scenario.
        """
        return self._name

    @property
    def supported_runtimes(self) -> dict[str, set[str]]:
        """
        The names of the supported runtimes and the versions of these runtimes.
        """
        return self._supported_runtimes
