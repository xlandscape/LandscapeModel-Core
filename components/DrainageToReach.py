"""
Class definition of the DrainageToReach Landscape Model component.
"""
import numpy as np
import base
import attrib
from osgeo import ogr, osr
import os


class DrainageToReach(base.Component):
    """
    Calculates input from field drainage into reaches.

    INPUTS
    Deposition: The substance deposited at the water surface. A NumPy array of scales time/day, space/base_geometry.
    Values have a unit of g/ha.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach. Values have no unit.
    Mapping: Maps base geometries to reaches. A list[int] of scale space/base_geometry. Values have no unit.

    OUTPUTS
    Deposition: The substance deposited at the water surface for reaches. A NumPy array of scales time/day, space/reach.
    Values have the same unit as the input deposition.
    Reaches: The identifiers of individual reaches. A NumPy array of scale space/reach.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "components.DrainageToReach basic implementation")

    def __init__(self, name, observer, store):
        super(DrainageToReach, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "DrainageLoad",
                (
                    attrib.Class(np.ndarray, 1),
                    attrib.Unit("mg/m2/h", 1),
                    attrib.Scales("time/hour, space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "DrainageLoad2nd",
                (
                    attrib.Class(np.ndarray, 1),
                    attrib.Unit("mg/m2/h", 1),
                    attrib.Scales("time/hour, space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "DRAINCON",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "FeatureIds",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "Reaches",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "FocusMacroUniqueID",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "FocusMacroFieldID",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "AppliedFields",
                (attrib.Class(np.ndarray, 1), attrib.Unit(None, 1), attrib.Scales("space/reach", 1)),
                self.default_observer
            ),
            base.Input(
                "Geometries",
                (
                    attrib.Class("list[bytes]", 1),
                    attrib.Unit(None, 1),
                    attrib.Scales("space/base_geometry", 1)
                ),
                self.default_observer
            ),
            base.Input(
                "GeometryCrs",
                (attrib.Class(str, 1), attrib.Unit(None, 1), attrib.Scales("global", 1)),
                self.default_observer
            ),
        ])
        self._outputs = base.OutputContainer(self, [
            base.Output("DrainageLoad", store, self),
        ])
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing.
        """
        self.default_observer.write_message(2, "DrainageToReach")
        # get reach names from hydrological scenario
        reaches = self.inputs["Reaches"].read().values
        
        # get draiange data from field drainage module
        DrainageLoad = self.inputs["DrainageLoad"].read().values
        DrainageLoad2nd = self.inputs["DrainageLoad2nd"].read().values
        
        # get table which holds unique simulation IDs and fields
        FocusMacroUniqueIDs = self.inputs["FocusMacroUniqueID"].read().values
        FocusMacroFieldIDs = self.inputs["FocusMacroFieldID"].read().values
        
        # get field informatio nfrom LULC
        FeatureIds = self.inputs["FeatureIds"].read().values
        DRAINCON = self.inputs["DRAINCON"].read().values
        
        # read geodata to calculate agricultural field areas
        geometries = self.inputs["Geometries"].read().values
        crs = self.inputs["GeometryCrs"].read().values
        spatial_reference = osr.SpatialReference()
        spatial_reference.ImportFromWkt(crs)
        ogr_driver = ogr.GetDriverByName("MEMORY")
        ogr_data_set = ogr_driver.CreateDataSource("memData")
        ogr_layer = ogr_data_set.CreateLayer("geom", spatial_reference, ogr.wkbPolygon)
        ogr_layer_definition = ogr_layer.GetLayerDefn()
        for i in range(len(geometries)):
            feature = ogr.Feature(ogr_layer_definition)
            feature.SetGeometry(ogr.CreateGeometryFromWkb(geometries[i]))
            ogr_layer.CreateFeature(feature)
        AREA=[feature.GetGeometryRef().GetArea() for feature in ogr_layer]
        del ogr_layer_definition, ogr_layer, ogr_data_set, ogr_driver
        
        # get shape for output variables
        dx = reaches.shape[0] # spatial shape
        dt = DrainageLoad.shape[0] # temporal shape

        # creat eoutput variable
        self.outputs["DrainageLoad"].set_values(
            np.ndarray, shape=(dt,dx),
            data_type= np.dtype('<f8'),
            chunks=(dt, 1),
            scales="time/hour, space/reach",
            unit="mg/hour"
        )        

        # write a timeseries for each reach with the drainage input
        for i, key in enumerate(reaches):
           
            #check if the reach has a drainage connections
            cons=[v for v,val in enumerate(DRAINCON) if val == 'r%i'%key]
            drainReach=np.zeros(dt)
            
            if len(cons)>0:
                for con in cons:
                  
                    # get index of field and realted macro simulation 
                    ind=np.argwhere(FocusMacroFieldIDs==FeatureIds[con])[0,0]
                    FocusMacroID=FocusMacroUniqueIDs[ind] # uniqhe macro runID
                    FocsMacroIndex=int(FocusMacroID.replace("sim",""))-1 # ids are coded sim1, sim2, --> equals index in DrainageLoad and DrainageLoad2n

                    # sum up draiange flux:  Drainage (mg/m²/hour) x field Area (m2)
                    drainReach+= ( DrainageLoad[:,FocsMacroIndex] * AREA[con] )  # get mass flux form primary draiange
                    drainReach+= ( DrainageLoad2nd[:,FocsMacroIndex] * AREA[con] ) # ge mass flux fro msecondary draiange
   
            # set timeseries for each reach
            self.outputs["DrainageLoad"].set_values(drainReach, slices=(slice(dt), i),create=False)













