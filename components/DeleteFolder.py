"""
Class definition of the Landscape Model DeleteFolder component.
"""
import base
import shutil


class DeleteFolder(base.Component):
    """
    A generic component that deletes a folder from the file system.

    INPUTS
    Path: A valid path of a folder to be deleted.

    OUTPUTS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.4.4", "components.DeleteFolder component")

    def __init__(self, name, observer, store):
        super(DeleteFolder, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [base.Input("Path", (), self.default_observer)])
        self._outputs = base.OutputContainer(self, [])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing
        """
        shutil.rmtree(self._inputs["Path"].read().values)
        return
