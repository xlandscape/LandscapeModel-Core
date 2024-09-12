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
    base.VERSION.added("1.4.1", "Changelog in `base.UserParameters` ")
    base.VERSION.changed("1.4.9", "`base.UserParameters` property names")
    base.VERSION.changed("1.5.3", "`base.UserParameters` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.UserParameters` ")
    base.VERSION.changed("1.10.3", "Spell checking in `base.UserParameters` ")
    base.VERSION.added("1.12.3", "XML validation to `base.UserParameters` ")
    base.VERSION.changed("1.12.3", "`base.UserParameters` handles XML namespaces")

    def __init__(self, parametrization_file: str) -> None:
        self._params = {}
        self._file = parametrization_file
        self._uncertaintyAndSensitivityAnalysis = None
        self._subdir = ""
        with open(parametrization_file) as f:
            header = f.read(5)
        if header == "<?xml":
            xsd = os.path.abspath(os.path.join(os.path.dirname(base.__file__), "..", "..", "variant", "parameters.xsd"))
            if os.path.exists(xsd):
                xmlschema.XMLSchema(xsd).validate(parametrization_file)
            else:
                print("WARNING: no parameter schema found, skipping parameter validation")
            config = xml.etree.ElementTree.parse(parametrization_file)
            for parameter in config.iter():
                if not parameter:
                    self.params[re.match("(?:{.*})?(?P<tag>.+)", parameter.tag).group(1)] = parameter.text
            if "uncertainty_sensitivity_analysis_runs" in config.getroot().attrib:
                self._uncertaintyAndSensitivityAnalysis = int(
                    config.getroot().attrib["uncertainty_sensitivity_analysis_runs"])
            if "subdir" in config.getroot().attrib:
                self._subdir = config.getroot().attrib["subdir"]
        else:
            print("WARNING: YAML-based xLandscape parameterization currently does not support schema validation")
            print("NOTE: YAML-based xLandscape parameterization does not support uncertainty and sensitivity analyses")
            print("NOTE: YAML-based xLandscape parameterization does not support parameterization subdirectories")
            with open(parametrization_file) as f:
                self._params = yaml.load(f, yaml.BaseLoader)

    @property
    def params(self) -> dict[str, str]:
        """
        Gets the user-defined parameters.
        :return: A dictionary of the user-defined parameters.
        """
        return self._params

    @property
    def file(self) -> str:
        """
        Gets the file path of the original parameterization file.
        :return: The file path of the original XML file.
        """
        return self._file

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
