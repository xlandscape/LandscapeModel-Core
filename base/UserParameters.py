"""
Class definition of the Landscape Model UserParameters class.
"""
import xml.etree.ElementTree
import base
import re
import os
import xmlschema


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

    def __init__(self, xml_file: str) -> None:
        self._params = {}
        xsd = os.path.abspath(os.path.join(os.path.dirname(base.__file__), "..", "..", "variant", "parameters.xsd"))
        if os.path.exists(xsd):
            xmlschema.XMLSchema(xsd).validate(xml_file)
        else:
            print("WARNING: no parameter schema found, skipping parameter validation")
        config = xml.etree.ElementTree.parse(xml_file)
        for parameter in config.iter():
            if not parameter:
                self.params[re.match("(?:{.*})?(?P<tag>.+)", parameter.tag).group(1)] = parameter.text
        self._xml = xml_file
        if "uncertainty_sensitivity_analysis_runs" in config.getroot().attrib:
            self._uncertaintyAndSensitivityAnalysis = int(
                config.getroot().attrib["uncertainty_sensitivity_analysis_runs"])
        else:
            self._uncertaintyAndSensitivityAnalysis = None
        if "subdir" in config.getroot().attrib:
            self._subdir = config.getroot().attrib["subdir"]
        else:
            self._subdir = ""

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
        Gets the file path of the original XML file.
        :return: The file path of the original XML file.
        """
        return self._xml

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
