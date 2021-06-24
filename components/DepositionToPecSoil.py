"""
Class definition of the DepositionToPecSoil Landscape Model component.
"""
import numpy as np
import base


class DepositionToPecSoil(base.Component):
    """
    Calculates the PEC soil from surface deposition by a simple homogeneous distribution of mass in the top soil layer.

    INPUTS
    Deposition: The deposition on the soil surface.
    SoilBulkDensity: The density of the soil layer.
    Depth: The depth of the soil layer in which the deposition is distributed equally.

    OUTPUTS
    PecSoil: The homogenous concentration of substance in soil. A NumPy array with scales time/day, space_x/1sqm,
    space_y/1sqm.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "components.DepositionToPecSoil component")
    base.VERSION.changed("1.1.5", "components.DepositionToPecSoil reports scale information of output to data store")
    base.VERSION.changed("1.1.5", "components.DepositionToPecSoil requests storing of maximum value of PEC soil")
    base.VERSION.fixed("1.2.14", "wrong calculation in components.DepositionToPecSoil")
    base.VERSION.changed("1.3.27", "components.DepositionToPecSoil refactored")
    base.VERSION.changed("1.3.27", "Soil depth is now parameter in components.DepositionToPecSoil")
    base.VERSION.fixed("1.3.29", "Input slicing in components.DepositionToPecSoil")
    base.VERSION.added("1.4.1", "Changelog in components.DepositionToPecSoil")
    base.VERSION.changed("1.4.1", "components.DepositionToPecSoil class documentation")
    base.VERSION.changed("1.4.1", "Removed unused output PecSoil 2 from components.DepositionToPecSoil")
    base.VERSION.changed("1.4.9", "`components.DepositionToPecSoil` data type access")

    def __init__(self, name, observer, store):
        super(DepositionToPecSoil, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input("Deposition", (), self.default_observer),
            base.Input("SoilBulkDensity", (), self.default_observer),
            base.Input("Depth", (), self.default_observer)
        ])
        self._outputs = base.OutputContainer(self, [base.Output("PecSoil", store, self)])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        data_set_info = self._inputs["Deposition"].describe()
        soil_bulk_density = self.inputs["SoilBulkDensity"].read().values
        depth = self.inputs["SoilBulkDensity"].read().values
        soil_mass = soil_bulk_density * depth * 10  # [kg]
        quotient = soil_mass * 1e4 / 1e3
        chunk_slices = base.chunk_slices(data_set_info["shape"], data_set_info["chunks"])
        self.outputs["PecSoil"].set_values(
            np.ndarray,
            chunks=data_set_info["chunks"],
            shape=data_set_info["shape"],
            data_type=data_set_info["data_type"],
            scales="time/day, space_x/1sqm, space_y/1sqm"
        )
        for chunkSlice in chunk_slices:
            deposition = self.inputs["Deposition"].read(slices=chunkSlice).values
            pec_soil = deposition / quotient
            self.outputs["PecSoil"].set_values(pec_soil, slices=chunkSlice, create=False, calculate_max=True)
        return
