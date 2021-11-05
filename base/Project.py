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
    base.VERSION.changed("1.9.10", "`base.Project` can handle outsourced package parts")

    def __init__(self, project: str, project_dir: str, prefix: str = ":") -> None:
        self._content = {}
        self._path = os.path.join(project_dir, project)
        # noinspection SpellCheckingInspection
        config = xml.etree.ElementTree.parse(os.path.join(self._path,  "scenario.xproject")).getroot()
        for entry in config.find("Content").findall("Item"):
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
