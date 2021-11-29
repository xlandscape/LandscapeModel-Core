"""
Class definition of a Landscape Model component generating distribution plots.
"""
import base
import attrib
import matplotlib.pyplot
import numpy
import os


class ReportingDistribution(base.Component):
    """
    Draws a distribution of values.

    INPUTS
    Values: The input values. A NumPy array.
    XLabel: The label of the x-axis. A string.
    Title: The title of the plot. A string of global scale.
    XMin: The minimum x-value to display. A float of global sale.
    XMax: The maximum x-value to display. A float of global sale.
    OutputFile: A valid file path to write the plot to. A string of global scale.

    OUTPUTS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.ReportingDistribution` component")
    base.VERSION.added("1.4.1", "Changelog in `components.ReportingDistribution` ")
    base.VERSION.added("1.4.1", "`components.ReportingDistribution` class documentation")
    base.VERSION.fixed("1.4.5", "`components.ReportingDistribution` spelling error in documentation")
    base.VERSION.added("1.4.5", "`components.ReportingHydrographicMap.draw()` static method")
    base.VERSION.changed("1.5.3", "`components.ReportingHydrographicMap` changelog uses markdown for code elements")

    def __init__(self, name, observer, store):
        super(ReportingDistribution, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input("Values", [attrib.Class(numpy.ndarray, 1)], self.default_observer),
                base.Input("XLabel", [attrib.Class(str, 1)], self.default_observer),
                base.Input("Title", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input("XMin", (attrib.Class(float, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input("XMax", (attrib.Class(float, 1), attrib.Scales("global", 1)), self.default_observer),
                base.Input("OutputFile", (attrib.Class(str, 1), attrib.Scales("global", 1)), self.default_observer)
            ]
        )
        self._outputs = base.OutputContainer(self, [])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        values = self._inputs["Values"].read().values
        fig = matplotlib.pyplot.figure(figsize=(10, 10))
        ax = fig.add_subplot(111)
        ax.scatter(numpy.sort(values.flatten()), [i / values.size for i in range(values.size)])
        ax.set_xlim(self._inputs["XMin"].read().values, self._inputs["XMax"].read().values)
        ax.set_xlabel(self._inputs["XLabel"].read().values)
        ax.set_ylabel("Fraction")
        ax.set_title(self._inputs["Title"].read().values)
        output_file = self._inputs["OutputFile"].read().values
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        matplotlib.pyplot.savefig(output_file)
        return

    @staticmethod
    def draw(data_store, values, x_label, title, x_min, x_max, output_file):
        """
        Plots the distribution of values.
        :param data_store: The file path where the X3df store is located.
        :param values: The name of the dataset containing the values to plot.
        :param x_label: The label of the x-axis.
        :param title: The title of the plot.
        :param x_min: The minimum x-value to display.
        :param x_max: The maximum x-value to display.
        :param output_file: A valid path to a file where the plot is written to.
        :returns: Nothing.
        """
        base.reporting(
            data_store,
            ReportingDistribution,
            (("XLabel", x_label), ("Title", title), ("OutputFile", output_file), ("XMin", x_min), ("XMax", x_max)),
            (("Values", values),)
        )
        return
