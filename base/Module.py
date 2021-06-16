"""
Class definition for Landscape Model modules.
"""
import base


class Module:
    """
    Encapsulates a module used by the Landscape Model.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "base.Module class for describing Landscape Model modules")
    base.VERSION.changed("1.3.5", "base.Module refactored")
    base.VERSION.added("1.4.1", "Changelog in base.Module")

    def __init__(self, name, version):
        self._name = name
        self._version = version
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
