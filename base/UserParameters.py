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
    base.VERSION.added("1.1.1", "base.UserParameters class for user-defined parameters")
    base.VERSION.changed("1.2.17", "base.UserParameters understand uncertainty / sensitivity analysis XML attribute")
    base.VERSION.changed("1.3.27", "base.UserParameters refactored")
    base.VERSION.added("1.4.1", "Changelog in base.UserParameters")

    def __init__(self, xml_file):
        self._params = {}
        config = xml.etree.ElementTree.parse(xml_file).getroot()
        for parameter in config:
            self.params[parameter.tag] = parameter.text
        self._xml = xml_file
        if "uasa" in config.attrib:
            self._uasa = int(config.attrib["uasa"])
        else:
            self._uasa = None
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
    def uasa(self):
        """
        Gets the number of UASA runs.
        :return: The number of UASA runs.
        """
        return self._uasa

    @property
    def subdir(self):
        """
        Gets the sub-directory for the UASA runs.
        :return: A string containing the sub-directory for the UASA runs.
        """
        return self._subdir
