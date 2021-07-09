"""
Class definition of the Landscape Model CsvReader component.
"""
import numpy as np
import base


class CsvReader(base.Component):
    """
    A generic component that reads data from a CSV file.

    INPUTS
    FilePath: A valid path to a CSV file having a header line and commas as separators.

    OUTPUTS
    Outputs of this components are provisional, i.e., they are defined by links from inputs and have to be satisfied
    by data in the CSV file. Output names equal column names in the file.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "components.CsvReader component")
    base.VERSION.changed("1.3.33", "components.CsvReader refactored")
    base.VERSION.added("1.4.1", "Changelog in components.CsvReader")
    base.VERSION.changed("1.4.1", "components.CsvReader class documentation")
    base.VERSION.changed("1.5.0", "`components.CsvReader` iterates over output objects instead of names")

    def __init__(self, name, observer, store):
        super(CsvReader, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [base.Input("FilePath", (), self.default_observer)])
        self._outputs = base.ProvisionalOutputs(self, store)
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing
        """
        # noinspection PyTypeChecker
        data = np.genfromtxt(self.inputs["FilePath"].read().values, delimiter=",", dtype=None, names=True)
        for component_output in self.outputs:
            output = self.outputs[component_output.name]
            output.set_values(data[component_output.name])
        return
