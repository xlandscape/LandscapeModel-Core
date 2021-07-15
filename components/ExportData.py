"""
Class definition of the Landscape Model ExportData component.
"""
import base
import attrib
import stores
import numpy


class ExportData(base.Component):
    """
    A generic component that exports Landscape Model data into another data store.

    INPUTS
    TargetStoreType: The type of the target store. A string of global scale. Must be "SqlLite". Value has no unit.
    FilePath: The file path of the non-existing data store. A string of global scale. Value has no unit.
    Values: The datasets to export.
    Create: Specifies if the data store should be created. A bool of global scale. Value has no unit.
    ForeignKey: An optional input that specifies foreign keys for each dimension. A list[str] with global scale. Values
    have no unit.
    Sql: An optional SQL statement that is executed after the export. A string with global scale. Value has no unit.

    OUTPUTS
    None.
    """
    # CHANGELOG
    base.VERSION.added("1.4.3", "`components.ExportData` component")
    base.VERSION.fixed("1.4.5", "`components.ExportData` spelling error in inline documentation")
    base.VERSION.changed("1.4.9", "`components.ExportData` data type access")
    base.VERSION.changed("1.5.3", "`components.ExportData` changelog uses markdown for code elements")

    def __init__(self, name, observer, store):
        super(ExportData, self).__init__(name, observer, store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "TargetStoreType",
                (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer
            ),
            base.Input(
                "FilePath",
                (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer
            ),
            base.Input("Values", (), self.default_observer),
            base.Input(
                "Create",
                (attrib.Class(bool), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer
            ),
            base.Input(
                "ForeignKey",
                (attrib.Class("list[str]"), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer
            ),
            base.Input("Sql", (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)), self.default_observer)
        ])
        self._outputs = base.ProvisionalOutputs(self, store)
        return

    def run(self):
        """
        Runs the component.
        :return: Nothing
        """
        store_type = self._inputs["TargetStoreType"].read().values
        if store_type == "SqlLite":
            store = stores.SqlLiteStore(
                self._inputs["FilePath"].read().values, self.default_observer, self._inputs["Create"].read().values)
        else:
            raise ValueError("Store type not supported: " + store_type)
        source_description = self._inputs["Values"].describe()
        output = base.Output(self._inputs["Values"].provider.output.name.split("/")[-1], store, self)
        foreign_keys = self._inputs["ForeignKey"].read().values if self._inputs["ForeignKey"].has_provider else None
        if source_description["chunks"] is None:
            output.set_values(
                self._inputs["Values"].read().values,
                scales=source_description["scales"],
                unit=source_description["unit"],
                foreign_keys=foreign_keys
            )
        else:
            output.set_values(
                numpy.ndarray,
                shape=source_description["shape"],
                dtype=source_description["data_type"],
                chunks=source_description["chunks"],
                scales=source_description["scales"],
                unit=source_description["unit"],
                foreign_keys=foreign_keys
            )
            for chunk in base.chunk_slices(source_description["shape"], source_description["chunks"]):
                data = self._inputs["Values"].read(slices=chunk)
                output.set_values(data.values, create=False, slices=chunk)
        if self._inputs["Sql"].has_provider:
            store.execute(self._inputs["Sql"].read().values)
        store.close()
        return
