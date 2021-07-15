"""
Class definition for Landscape Model modules.
"""
import base


class Module:
    """
    Encapsulates a module used by the Landscape Model.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Module` class for describing Landscape Model modules")
    base.VERSION.changed("1.3.5", "`base.Module` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Module` ")
    base.VERSION.added("1.5.0", "`base.Module.doc_file` ")
    base.VERSION.changed("1.5.3", "`base.Module` changelog uses markdown for code elements")

    def __init__(self, name, version, doc_file=None):
        self._name = name
        self._version = version
        self._doc_file = doc_file
        return

    @property
    def name(self):
        """
        Gets the name of the module as specified by the module author.
        """
        return self._name

    @property
    def version(self):
        """
        Gets the version of the module as specified by the module author.
        """
        return self._version

    @property
    def doc_file(self):
        """
        Gets the path of the additional documentation file, if available.
        """
        return self._doc_file
