"""
Class definition of the Landscape Model ExportData component.
"""
import base
import attrib
import stores
import numpy
import typing


class ExportData(base.Component):
    """
    A generic component that exports Landscape Model data into another data store. Currently, the only supported output
    store are SqlLite databases. The component allows to create a new SqlLite database or append to an existing one. It
    also features the execution of arbitrary SQL code after the export of data.
    """
    # CHANGELOG
    base.VERSION.added("1.4.3", "`components.ExportData` component")
    base.VERSION.fixed("1.4.5", "`components.ExportData` spelling error in inline documentation")
    base.VERSION.changed("1.4.9", "`components.ExportData` data type access")
    base.VERSION.changed("1.5.3", "`components.ExportData` changelog uses markdown for code elements")
    base.VERSION.fixed("1.5.4", "`components.ExportData` data type access")
    base.VERSION.added("1.7.0", "Type hints to `components.ExportData`")
    base.VERSION.changed("1.7.0", "Harmonized init signature of `components.ExportData` with base class")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `components.ExportData`")
    base.VERSION.changed("1.15.1", "Skip initial attribute checks for `Values` input of `ExportData` component")
    base.VERSION.changed("1.15.6", "Updated description of `ExportData` component")
    base.VERSION.added("1.15.6", "Input descriptions to `ExportData` component")
    base.VERSION.changed("1.15.8", "Removed ProvisionalOutputs from `ExportData` component")
    base.VERSION.changed("1.15.8", "Target outputs for export in `ExportData` component no longer check attributes")
    base.VERSION.changed("1.18.0", "Code refactory in `components.ExportData`")

    def __init__(self, name: str, default_observer: base.Observer, default_store: typing.Optional[base.Store]) -> None:
        super(ExportData, self).__init__(name, default_observer, default_store)
        self._inputs = base.InputContainer(self, [
            base.Input(
                "TargetStoreType",
                (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None), attrib.Equals("SqlLite")),
                self.default_observer,
                description="The type of the target store. Currently, `SqlLite` is the only supported store type."
            ),
            base.Input(
                "FilePath",
                (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer,
                description="The file path of the data store. If `Create` is set to `True`, the store is not allowed "
                            "to already exist. If set to `False`, however, the store is required to be present on the "
                            "specified location."
            ),
            base.Input(
                "Values", (),
                self.default_observer,
                description="The datasets to export. This can be virtually any data managed by the Landscape Model as "
                            "far as the datatype is supported by the `SqlLite` store. Some metadata might become lost "
                            "during export.",
                skip_initial_attribute_checks=True
            ),
            base.Input(
                "Create",
                (attrib.Class(bool), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer,
                description="Specifies if the data store should be created. If set to `True`, the store is not allowed "
                            "to already exist, if set to `False`, it has to already exist."
            ),
            base.Input(
                "ForeignKey",
                (attrib.Class(list[str]), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer,
                description="An optional input that specifies foreign keys for each dimension. This value is appended "
                            "to the table definition of the dataset and commonly looks like something similar to "
                            "``|`space/base_geometry`(`CascadeToxswa/hydrography_id`)``."
            ),
            base.Input(
                "Sql",
                (attrib.Class(str), attrib.Scales("global"), attrib.Unit(None)),
                self.default_observer,
                description="An optional SQL statement that is executed after the export. This can, for instance, be "
                            "used to create views in a SqlLite database."
            )
        ])

    def run(self) -> None:
        """
        Runs the component.
        :return: Nothing
        """
        store_type = self._inputs["TargetStoreType"].read().values
        if store_type == "SqlLite":
            store = stores.SqlLiteStore(
                self._inputs["FilePath"].read().values, self.default_observer, self._inputs["Create"].read().values)
        else:
            raise ValueError(f"Store type not supported: {store_type}")
        source_description = self._inputs["Values"].describe()
        output = base.Output(
            self._inputs["Values"].provider.output.name.split("/")[-1], store, self, skip_initial_attribute_checks=True)
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
                data_type=source_description["data_type"],
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
