"""
Class definition of the Landscape Model UncertaintyAndSensitivityAnalysis class.
"""
import os
import re
import numpy as np
import xml.etree.ElementTree
import base


class UncertaintyAndSensitivityAnalysis:
    """
    Provides functionality to conduct uncertainty and sensitivity analyses.
    """
    # CHANGELOG
    base.VERSION.added(
        "1.2.17", "`base.UncertaintyAndSensitivityAnalysis` class for managing uncertainty and sensitivity analyses")
    base.VERSION.changed(
        "1.2.31", "`base.UncertaintyAndSensitivityAnalysis.create()` parameter generation possible in sub-directories")
    base.VERSION.changed("1.2.31", "`base.UncertaintyAndSensitivityAnalysis.create()` can process pre-defined lists")
    base.VERSION.fixed("1.2.35", "`base.UncertaintyAndSensitivityAnalysis.create()` function parsing improved")
    base.VERSION.changed("1.3.27", "`base.UncertaintyAndSensitivityAnalysis` refactored")
    base.VERSION.changed("1.3.35", "`base.UncertaintyAndSensitivityAnalysis.create()` regex refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.UncertaintyAndSensitivityAnalysis` ")
    base.VERSION.changed("1.4.9", "`base.UncertaintyAndSensitivityAnalysis` renamed")
    base.VERSION.changed("1.4.9", "`base.UncertaintyAndSensitivityAnalysis` renamed local variables")

    def __init__(self, parameters: base.UserParameters) -> None:
        if parameters.uncertainty_sensitivity_analysis is None:
            raise ValueError("No uncertainty/sensitivity analysis runs specified in user parameters")
        self._params = parameters

    def create(self) -> None:
        """
        Creates a set of uncertainty or sensitivity analysis runs.
        :return: Nothing.
        """
        output_dir = os.path.dirname(self._params.xml)
        for uncertaintyAndSensitivityAnalysis in range(self._params.uncertainty_sensitivity_analysis):
            uncertainty_analysis_name = self._params.params["SimID"] + "-" + str(uncertaintyAndSensitivityAnalysis + 1)
            # noinspection SpellCheckingInspection
            destination = os.path.join(output_dir, self._params.subdir, uncertainty_analysis_name + ".xrun")
            if os.path.exists(destination):
                raise FileExistsError(
                    "Cannot create uncertainty/sensitivity analysis parameterization: file " +
                    destination + " already exists")
            if not os.path.exists(os.path.dirname(destination)):
                os.makedirs(os.path.dirname(destination))
            parameters_element = xml.etree.ElementTree.Element("Parameters")
            for param, value in self._params.params.items():
                if param == "SimID":
                    xml.etree.ElementTree.SubElement(parameters_element, param).text = uncertainty_analysis_name
                else:
                    match = re.search(r"\$\[(?P<a>[a-z]+)\((?P<b>.+)\)]", value)
                    if match is not None:
                        f = value[match.regs[1][0]:match.regs[1][1]]
                        p = value[match.regs[2][0]:match.regs[2][1]].split(", ")
                        if f == "list":
                            xml.etree.ElementTree.SubElement(
                                parameters_element, param).text = p[uncertaintyAndSensitivityAnalysis]
                        elif f == "normal":
                            xml.etree.ElementTree.SubElement(parameters_element, param).text = str(
                                round(np.random.normal(float(p[0]), float(p[1]), 1)[0], 4)
                            )
                        else:
                            raise ValueError("Unknown function: " + f)                        
                    else:
                        xml.etree.ElementTree.SubElement(parameters_element, param).text = str(value)
            xml.etree.ElementTree.ElementTree(parameters_element).write(
                destination,
                encoding="utf-8",
                xml_declaration=True
            )
