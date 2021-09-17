"""
Class definition of a Landscape Module project.
"""
import os
import xml.etree.ElementTree
import base
import typing


class Project:
    """
    A Landscape Module project.
    """
    # CHANGELOG
    base.VERSION.added("1.2.1", "`base.Project` class for representing Landscape Model scenarios")
    base.VERSION.changed("1.3.5", "`base.Project` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Project` ")
    base.VERSION.added("1.4.1", "`base.Project.version` ")
    base.VERSION.changed("1.5.3", "`base.Project` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Project` ")

    def __init__(self, project: str, project_dir: str, prefix: str = ":") -> None:
        self._content = {}
        self._path = os.path.join(project_dir, project)
        # noinspection SpellCheckingInspection
        config = xml.etree.ElementTree.parse(os.path.join(self._path,  "scenario.xproject")).getroot()
        for entry in config.find("Content").findall("Item"):
            self._content[prefix + entry.attrib["name"]] = os.path.join(
                project_dir, project, entry.attrib["target"]
            )
        self._version = config.find("Version").text

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
