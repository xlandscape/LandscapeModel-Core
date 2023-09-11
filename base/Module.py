"""
Class definition for Landscape Model modules.
"""
import base
import typing


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
    base.VERSION.added("1.7.0", "Type hints to `base.Module` ")

    def __init__(
            self,
            name: str,
            version: str,
            path: str,
            doc_file: typing.Optional[str],
            module: typing.Optional["Module"]
    ) -> None:
        self._name = name
        self._version = version
        self._path = path
        self._doc_file = doc_file
        self._module = module

    @property
    def name(self) -> str:
        """
        Gets the name of the module as specified by the module author.
        """
        return self._name

    @property
    def version(self) -> str:
        """
        Gets the version of the module as specified by the module author.
        """
        return self._version

    @property
    def path(self) -> str:
        """
        Gets the path of the module.
        """
        return self._path

    @property
    def doc_file(self) -> typing.Optional[str]:
        """
        Gets the path of the additional documentation file, if available.
        """
        return self._doc_file

    @property
    def module(self) -> typing.Optional["Module"]:
        """
        Gets the module of the module.
        """
        return self._module
