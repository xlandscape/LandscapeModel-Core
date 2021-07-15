"""
Class definition of the Landscape Model UserParameters class.
"""
import xml.etree.ElementTree
import base


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

    def __init__(self, xml_file):
        self._params = {}
        config = xml.etree.ElementTree.parse(xml_file).getroot()
        for parameter in config:
            self.params[parameter.tag] = parameter.text
        self._xml = xml_file
        if "uncertainty_sensitivity_analysis_runs" in config.attrib:
            self._uncertaintyAndSensitivityAnalysis = int(config.attrib["uncertainty_sensitivity_analysis_runs"])
        else:
            self._uncertaintyAndSensitivityAnalysis = None
        if "subdir" in config.attrib:
            self._subdir = config.attrib["subdir"]
        else:
            self._subdir = ""
        return

    @property
    def params(self):
        """
        Gets the user-defined parameters.
        :return: A dictionary of the user-defined parameters.
        """
        return self._params

    @property
    def xml(self):
        """
        Gets the file path of the original XML file.
        :return: The file path of the original XML file.
        """
        return self._xml

    @property
    def uncertainty_sensitivity_analysis(self):
        """
        Gets the number of uncertainty or sensitivity analysis runs.
        :return: The number of uncertainty or sensitivity analysis runs.
        """
        return self._uncertaintyAndSensitivityAnalysis

    @property
    def subdir(self):
        """
        Gets the sub-directory for the uncertainty or sensitivity analysis runs.
        :return: A string containing the sub-directory for the uncertainty or sensitivity analysis runs.
        """
        return self._subdir
