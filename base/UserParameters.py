"""
Class definition of the Landscape Model UserParameters class.
"""
import xml.etree.ElementTree
import base
import re
import os
import xmlschema
import yaml


class UserParameters:
    """
    Encapsulates all user-defined parameters.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.UserParameters` class for user-defined parameters")
    base.VERSION.changed("1.2.17", "`base.UserParameters` understand uncertainty / sensitivity analysis XML attribute")
    base.VERSION.changed("1.3.27", "`base.UserParameters` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.UserParameters`")
    base.VERSION.changed("1.4.9", "`base.UserParameters` property names")
    base.VERSION.changed("1.5.3", "`base.UserParameters` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.UserParameters`")
    base.VERSION.changed("1.10.3", "Spell checking in `base.UserParameters`")
    base.VERSION.added("1.12.3", "XML validation to `base.UserParameters`")
    base.VERSION.changed("1.12.3", "`base.UserParameters` handles XML namespaces")
    base.VERSION.changed("1.18.0", "Code refactory in `base.UserParameters`")

    def __init__(self, param_file: str) -> None:
        self._params = {}
        self._source_file = param_file
        ext = os.path.splitext(param_file)[1].lower()
        if ext in (".yaml", ".yml"):
            self._load_from_yaml(param_file)
        else:
            self._load_from_xml(param_file)

    def _load_from_xml(self, xml_file: str) -> None:
        """Loads parameters from an xrun (XML) file."""
        xsd = os.path.abspath(os.path.join(os.path.dirname(base.__file__), "..", "..", "variant", "parameters.xsd"))
        if os.path.exists(xsd):
            xmlschema.XMLSchema(xsd).validate(xml_file)
        else:
            print("WARNING: no parameter schema found, skipping parameter validation")
        config = xml.etree.ElementTree.parse(xml_file)
        for parameter in config.iter():
            if not parameter:
                self.params[re.match("(?:{.*})?(?P<tag>.+)", parameter.tag).group(1)] = parameter.text
        if "uncertainty_sensitivity_analysis_runs" in config.getroot().attrib:
            self._uncertaintyAndSensitivityAnalysis = int(
                config.getroot().attrib["uncertainty_sensitivity_analysis_runs"])
        else:
            self._uncertaintyAndSensitivityAnalysis = None
        if "subdir" in config.getroot().attrib:
            self._subdir = config.getroot().attrib["subdir"]
        else:
            self._subdir = ""

    def _load_from_yaml(self, yaml_file: str) -> None:
        """Loads parameters from a YAML file, flattening the nested structure into a params dict."""
        with open(yaml_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        if data is None:
            data = {}
        self._flatten_yaml(data, self._params)
        # Handle optional top-level keys for uncertainty/sensitivity analysis
        if "uncertainty_sensitivity_analysis_runs" in data:
            self._uncertaintyAndSensitivityAnalysis = int(data["uncertainty_sensitivity_analysis_runs"])
        else:
            self._uncertaintyAndSensitivityAnalysis = None
        if "subdir" in data:
            self._subdir = str(data["subdir"])
        else:
            self._subdir = ""

    @staticmethod
    def _flatten_yaml(data: dict, params: dict) -> None:
        """Recursively flattens a nested YAML dict into a flat key-value dict (leaf values only)."""
        import datetime
        for key, value in data.items():
            if isinstance(value, dict):
                UserParameters._flatten_yaml(value, params)
            elif value is None:
                params[key] = None
            elif isinstance(value, bool):
                # Preserve lowercase 'true'/'false' to match XML convention
                params[key] = "true" if value else "false"
            elif isinstance(value, (datetime.date, datetime.datetime)):
                # Preserve date/datetime as string in the original format
                params[key] = str(value)
            else:
                params[key] = str(value)

    @property
    def params(self) -> dict[str, str]:
        """
        Gets the user-defined parameters.
        :return: A dictionary of the user-defined parameters.
        """
        return self._params

    @property
    def xml(self) -> str:
        """
        Gets the file path of the original parameter file (XML or YAML).
        :return: The file path of the original parameter file.
        """
        return self._source_file

    @property
    def uncertainty_sensitivity_analysis(self) -> int:
        """
        Gets the number of uncertainty or sensitivity analysis runs.
        :return: The number of uncertainty or sensitivity analysis runs.
        """
        return self._uncertaintyAndSensitivityAnalysis

    @property
    def subdir(self) -> str:
        """
        Gets the subdirectory for the uncertainty or sensitivity analysis runs.
        :return: A string containing the subdirectory for the uncertainty or sensitivity analysis runs.
        """
        return self._subdir
