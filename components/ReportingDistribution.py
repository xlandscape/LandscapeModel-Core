"""Class definition of a Landscape Model component generating distribution plots."""
import base
import attrib
import matplotlib.pyplot
import numpy
import os
import typing


class ReportingDistribution(base.Component):
    """
    Draws a distribution of values.
    """
    # CHANGELOG
    base.VERSION.added("1.4.0", "`components.ReportingDistribution` component")
    base.VERSION.added("1.4.1", "Changelog in `components.ReportingDistribution`")
    base.VERSION.added("1.4.1", "`components.ReportingDistribution` class documentation")
    base.VERSION.fixed("1.4.5", "`components.ReportingDistribution` spelling error in documentation")
    base.VERSION.added("1.4.5", "`components.ReportingDistribution.draw()` static method")
    base.VERSION.changed("1.5.3", "`components.ReportingDistribution` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `components.ReportingDistribution`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.ReportingDistribution` with base class")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `component.ReportingDistribution`")
    base.VERSION.changed("1.18.0", "Code refactory in `components.ReportingDistribution`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        """
        Initializes a ReportingDistribution component.

        Args:
            name: The name of the component.
            default_observer: The default observer of the component.
            default_store: The default store of the component.
        """
        super(ReportingDistribution, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(
            self,
            [
                base.Input(
                    "Values",
                    [attrib.Class(numpy.ndarray, 1)],
                    self.default_observer,
                    description="The input values. A NumPy array."
                ),
                base.Input(
                    "XLabel",
                    [attrib.Class(str, 1)],
                    self.default_observer,
                    description="The label of the x-axis. A string."
                ),
                base.Input(
                    "Title",
                    (attrib.Class(str, 1), attrib.Scales("global", 1)),
                    self.default_observer,
                    description="The title of the plot. A string of global scale."
                ),
                base.Input(
                    "XMin",
                    (attrib.Class(float, 1), attrib.Scales("global", 1)),
                    self.default_observer,
                    description="The minimum x-value to display. A float of global sale."
                ),
                base.Input(
                    "XMax",
                    (attrib.Class(float, 1), attrib.Scales("global", 1)),
                    self.default_observer,
                    description="The maximum x-value to display. A float of global sale."
                ),
                base.Input(
                    "OutputFile",
                    (attrib.Class(str, 1), attrib.Scales("global", 1)),
                    self.default_observer,
                    description="A valid file path to write the plot to. A string of global scale."
                )
            ]
        )
        self._outputs = base.OutputContainer(self, [])

    def run(self) -> None:
        """
        Runs the component.

        Returns:
            Nothing.
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

    @staticmethod
    def draw(
            data_store: str,
            values: str,
            x_label: str,
            title: str,
            x_min: float,
            x_max: float,
            output_file: str
    ) -> None:
        """
        Plots the distribution of values.

        Args:
            data_store: The file path where the X3df-store is located.
            values: The name of the dataset containing the values to plot.
            x_label: The label of the x-axis.
            title: The title of the plot.
            x_min: The minimum x-value to display.
            x_max: The maximum x-value to display.
            output_file: A valid path to a file where the plot is written to.

        Returns:
            Nothing.
        """
        base.reporting(
            data_store,
            ReportingDistribution,
            (("XLabel", x_label), ("Title", title), ("OutputFile", output_file), ("XMin", x_min), ("XMax", x_max)),
            (("Values", values),)
        )
