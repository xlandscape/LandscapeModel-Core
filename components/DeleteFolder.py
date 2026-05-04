"""
Class definition of the Landscape Model DeleteFolder component.
"""
import attrib
import base
import errno
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
    base.VERSION.added("1.18.1", "Semantic information to inputs of `components.DeleteFolder`")
    base.VERSION.fixed("1.18.2", "Robust deletion of folders in `components.DeleteFolder` when files disappear during cleanup")

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
        folder_path = self._inputs["Path"].read().values
        shutil.rmtree(folder_path, onerror=self._handle_delete_error)

    @staticmethod
    def _handle_delete_error(function: typing.Callable[..., typing.Any], path: str, exc_info: tuple[type, BaseException, typing.Any]) -> None:
        """Ignore missing-path races during recursive deletion and raise all other errors."""
        exception = exc_info[1]
        if isinstance(exception, FileNotFoundError):
            return
        if isinstance(exception, OSError) and exception.errno == errno.ENOENT:
            return
        raise exception
