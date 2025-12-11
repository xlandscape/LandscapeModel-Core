"""
Class definition of the Landscape Model DeleteFolder component.
"""
import attrib
import base
import shutil
import typing


class DeleteFolder(base.Component):
    """
    A generic component that deletes a folder from the file system.
    """
    # CHANGELOG
    base.VERSION.added("1.4.4", "`components.DeleteFolder` component")
    base.VERSION.changed("1.5.3", "`components.DeleteFolder` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `components.DeleteFolder`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.DeleteFolder` with base class")
    base.VERSION.changed("1.18.0", "Code refactory in `components.DeleteFolder`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(DeleteFolder, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "Path",
                    (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)),
                    self.default_observer,
                    description="A valid path of a folder to be deleted."
                )
            ]
        )
        self._outputs = base.OutputContainer(self, [])

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing
        """
        shutil.rmtree(self._inputs["Path"].read().values)
