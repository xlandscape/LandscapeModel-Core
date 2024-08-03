"""A class encapsulating an X3df data store."""
import datetime
import h5py
import numpy
import os
import pickle
import glob
import shutil
import base
import typing
import h5py.h5r


class X3dfStore(base.Store):
    """
    Encapsulates a X3df data store for usage in the Landscape Model.

    PARAMETERS
    file_path: The file path and name for the HDF5 tom use.
    observer: A observer that handles the messages emitted by the store.
    mode: The file mode with which the HDF5 is opened.
    initialization: File path and name to an existing X3dfStore which contains data used for initializing the current
    store.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`store.X3dfStore` ")
    base.VERSION.changed("1.1.5", "`store.X3dfStore` scale information for numpy arrays if provided")
    base.VERSION.changed("1.1.5", "`store.X3dfStore` can calculate maximum for numpy arrays")
    base.VERSION.changed("1.2.2", "`store.X3dfStore` now handles boolean values separately")
    base.VERSION.changed("1.2.16", "Slicing enabled for `list[byte]` in `store.X3dfStore`")
    base.VERSION.changed("1.2.20", "Support of dates and times in `store.X3dfStore` ")
    base.VERSION.changed("1.2.25", "Support of `NoneType` in `store.X3dfStore`")
    base.VERSION.changed("1.2.37", "Specified X3df file mode in `store.X3dfStore` ")
    base.VERSION.changed("1.2.37", "Ability to open X3df in different modes in `store.X3dfStore` ")
    base.VERSION.changed("1.2.37", "`store.X3dfStore` refactored")
    base.VERSION.changed("1.3.27", "`store.X3dfStore` acknowledges `scales` keyword for all value types")
    base.VERSION.changed("1.3.27", "`store.X3dfStore` `default` keyword added")
    base.VERSION.changed("1.3.27", "`store.X3dfStore` `slice` keyword renamed to `slices` ")
    base.VERSION.changed("1.3.33", "`store.X3dfStore` no longer casts `list[bytes]` to bytes")
    base.VERSION.changed("1.3.33", "`store.X3dfStore` can store and read lists of strings")
    base.VERSION.changed("1.3.33", "`store.X3dfStore` is explicit about its parameters")
    base.VERSION.changed("1.3.33", "`store.X3dfStore` stores physical unit if specified")
    base.VERSION.changed("1.3.33", "`store.X3dfStore.describe()` outputs scales")
    base.VERSION.changed("1.3.35", "`store.X3dfStore` can be initialized using existing data")
    base.VERSION.added("1.3.35", "`store.X3dfStore.has_dataset()` ")
    base.VERSION.added("1.4.1", "Changelog in `store.X3dfStore` ")
    base.VERSION.changed("1.4.1", "`store.X3dfStore` class documentation")
    base.VERSION.changed("1.4.6", "`store.X3dfStore` `identifier` argument of initializer")
    base.VERSION.changed("1.4.6", "`store.X3dfStore` parent run no longer randomly sampled")
    base.VERSION.fixed("1.4.8", "`store.X3dfStore` conversion of MC identifier to integer")
    base.VERSION.changed("1.4.9", "`store.X3dfStore` data type access")
    base.VERSION.changed("1.5.3", "`store.X3fdStore` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.0", "`store.X3dfStore` acknowledges that HDF-stored strings are now returned as bytes")
    base.VERSION.added("1.7.0", "Type hints to `stores.X3dfStore` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `stores.X3dfStore` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `stores.X3dfStore` ")
    base.VERSION.changed("1.10.0", "`stores.X3dfStore` now manages element names for some scales")
    base.VERSION.changed("1.10.1", "`stores.X3dfStore` recognizes additional scales")
    base.VERSION.changed("1.11.0", "`stores.X3dfStore` manages storage of offsets")
    base.VERSION.changed("1.12.0", "`stores.X3dfStore` recognizes square-meter scales for offset description")
    base.VERSION.changed("1.12.2", "Fixed typos in `stores.X3dfStore` documentation")
    base.VERSION.changed("1.14.0", "`stores.X3dfStore` now stores and retrieves geometries of elements")
    base.VERSION.changed("1.14.4", "Changed chunk size for lists in `stores.X3dfStore`")
    base.VERSION.changed(
        "1.15.6", "Changed `other/application`, `other/runs` and `other/soil_horizon` to named scales in `XdfStore`")
    base.VERSION.changed("1.15.6", "Removed `space/reach2` as recognized scale from `X3dfStore`")
    base.VERSION.changed("1.15.8", "Changed `space/reach` to a named geometries scale in `X3dfStore`")
    base.VERSION.added("1.15.9", "Logic to postpone creation of reference links in `X3dfStore` if needed")
    base.VERSION.added("1.16.1", "Weather region as named scale")
    base.VERSION.changed("1.16.2", "Changed scale other/application to plain scale")
    base.VERSION.changed("1.16.2", "Changed scale other/soil_horizon to plain scale")
    base.VERSION.changed(
        "1.16.2", "Changed semantic checks in `X3dfStore` so that they only take place during creation of datasets")
    base.VERSION.changed("1.16.3", "Changed default value for newly created datasets in X3dfStore to NaN")
    base.VERSION.changed("1.16.4", "Changed chunking of byte lists in X3dfStore")

    def __init__(
            self,
            file_path: str,
            observer: typing.Optional[base.Observer] = None,
            mode: str = "a",
            initialization: typing.Optional[str] = None,
            identifier: int = 0
    ) -> None:
        """
        Initializes a X3df data store.

        Args:
            file_path: The path of the X3df file.
            observer: The observer used by the store.
            mode: The file mode in which the X3df file is opened.
            initialization: An existing store with which the new X3df store is initialized.
            identifier: The identifier of the initialized run.
        """
        hdf5_file = os.path.join(file_path, "arr.dat")
        if mode != "r":
            try:
                os.makedirs(file_path)
            except FileExistsError:
                raise FileExistsError(f"Cannot create store if it already exists: {file_path}")
            observer.write_message(4, "Creating new X3dfStore at", file_path)
        if initialization is not None:
            available_runs = glob.glob(initialization)
            if len(available_runs) < 1:
                raise ValueError(f"No runs found at {initialization}")
            selected_source_run = available_runs[int(identifier) % len(available_runs)]
            observer.write_message(4, "Initializing data store from", selected_source_run)
            shutil.copyfile(selected_source_run, hdf5_file)
        self._f = h5py.File(hdf5_file, mode)
        self._observer = observer
        self._known_scales = {
            "chemical/substance": "named",
            "global": "plain",
            "space/base_geometry": "named geometries",
            "space/extent": "plain",
            "space/reach": "named geometries",
            "space/weather_region": "named",
            "space/x_5dm": "offset",
            "space/y_5dm": "offset",
            "time/day": "offset",
            "time/day_of_year": "plain",
            "time/hour": "offset",
            "time/year": "offset",
            "other/application": "plain",
            "other/crop": "named",
            "other/factor": "named",
            "other/run": "named",
            "other/soil_horizon": "plain",
            "other/species": "named"
        }
        self._pending_links = {}

    def close(self) -> None:
        """
        Closes the store.

        Returns:
            Nothing.
        """
        if self._pending_links:
            self._observer.write_message(
                2, f"Store is closing but has still pending links: {', '.join(self._pending_links.keys())}")
        self._f.close()

    def describe(self, name: str) -> dict[str, typing.Any]:
        """
        Describes a dataset in the store.

        Args:
            name: The name of the dataset.

        Returns:
            A dictionary describing the dataset.
        """
        data_set = self._f[name]
        element_names = []
        offsets = []
        geometries = []
        scales = data_set.attrs.get("scales", ("global",))
        for dim in range(len(data_set.shape)):
            element_names.append(None)
            element_names_attribute = f"dim{dim}_element_names"
            if element_names_attribute in data_set.attrs:
                element_names[dim] = base.Output(self._f[data_set.attrs[element_names_attribute]].name, self)
            offsets.append(None)
            offset_attribute = f"dim{dim}_offset"
            if offset_attribute in data_set.attrs:
                if scales[dim] == "time/hour":
                    offsets[dim] = datetime.datetime.strptime(
                        data_set.attrs[offset_attribute], "%Y-%m-%d %H:%M:%S")
                elif scales[dim] == "time/day":
                    offsets[dim] = datetime.datetime.strptime(
                        data_set.attrs[offset_attribute], "%Y-%m-%d").date()
                else:
                    offsets[dim] = data_set.attrs[offset_attribute]
                    if scales[dim] != "time/year" and not scales[dim].startswith(
                            "space_") and not scales[dim].endswith("sqm"):
                        self._observer.write_message(2, f"Unimplemented description for offset scale {scales[dim]}")
            geometries.append(None)
            geometries_attribute = f"dim{dim}_geometries"
            if geometries_attribute in data_set.attrs:
                geometries[dim] = base.Output(self._f[data_set.attrs[geometries_attribute]].name, self)
        return {
            "shape": data_set.shape,
            "data_type": data_set.dtype,
            "chunks": data_set.chunks,
            "unit": data_set.attrs.get("unit", None),
            "scales": ", ".join(scales),
            "element_names": element_names,
            "offsets": offsets,
            "geometries": geometries
        }

    def get_values(self, name: str, **keywords) -> typing.Any:
        """
        Gets the values of a data set from the store.

        Args:
            name: The name of the data set.
            keywords: Additional keywords.

        Returns:
            The values of the data set in their original representation.
        """
        data_set = self._f[name]
        original_type = data_set.attrs["_type"]
        # noinspection SpellCheckingInspection
        if original_type == "bool":
            values = int(data_set[()]) == 1
        elif original_type == "int":
            values = int(data_set[()])
        elif original_type == "float":
            values = float(data_set[()])
        elif original_type == "str":
            values = data_set[()].decode()
        elif original_type == "list[bytes]":
            if "slices" in keywords:
                values = data_set[keywords["slices"]].tostring()
                if not isinstance(values, list):
                    values = [values]
            else:
                values = [data_set[i].tostring() for i in range(data_set.shape[0])]
        elif original_type == "list[float]":
            values = data_set[()].tolist()
        elif original_type == "list[int]":
            values = data_set[()].tolist()
        elif original_type == "tuple[float]":
            values = tuple(data_set[()].tolist())
        elif original_type == "list[object]":
            values = [pickle.loads(data_set[i]) for i in range(data_set.shape[0])]
        elif original_type == "datetime.date":
            values = datetime.datetime.strptime(data_set[()].decode(), "%Y-%m-%d").date()
        elif original_type == "numpy.ndarray":
            if "slices" in keywords and "select" in keywords:
                raise AttributeError("slices and select keywords may not be used simultaneously")
            elif data_set.attrs["requires_indexing"] and "select" not in keywords:
                raise AttributeError(f"Dataset {name} requires strict indexing, but select keyword is not present")
            elif "slices" in keywords:
                values = data_set[keywords["slices"]]
            elif "select" in keywords:
                data_set_scales = data_set.attrs["scales"]
                slices = []
                dataset_description = self.describe(name)
                for i, scale in enumerate(data_set_scales):
                    if scale == "time/day":
                        if keywords["select"][scale] == "all":
                            slices.append(slice(0, dataset_description["shape"][i]))
                        else:
                            slices.append(
                                slice(
                                    (keywords["select"][scale]["from"] - dataset_description["offsets"][i]).days,
                                    (keywords["select"][scale]["to"] - dataset_description["offsets"][i]).days
                                )
                            )
                    elif scale == "space/weather_region":
                        for selection_method in keywords["select"][scale]:
                            if selection_method == "element":
                                element_names = dataset_description["element_names"][i].get_values()
                                if keywords["select"][scale]["element"] in element_names:
                                    slices.append(element_names.index(keywords["select"][scale]["element"]))
                                else:
                                    raise ValueError(
                                        f"Element {keywords['select'][scale]['element']} not found for scale {scale}")
                    else:
                        raise ValueError(f"Selection not supported for scale {scale}")
                values = data_set[tuple(slices)]
                pass
            else:
                values = data_set[()]
        elif original_type == "datetime.datetime":
            values = datetime.datetime.strptime(data_set[()].decode(), "%Y-%m-%d %H:%M:%S")
        elif original_type == "None":
            values = None
        elif original_type == "list[str]":
            values = [s.decode() for s in data_set[()].tolist()]
        else:
            raise TypeError(f"Stored type cannot be interpreted: {original_type}")
        return values

    def set_values(
            self,
            name: str,
            values: typing.Any,
            scales: typing.Optional[str] = None,
            default: typing.Any = None,
            unit: typing.Optional[str] = None,
            shape: typing.Optional[typing.Sequence[int]] = None,
            data_type: typing.Optional[type] = None,
            chunks: typing.Optional[typing.Sequence[slice]] = None,
            create: bool = True,
            slices: typing.Optional[typing.Sequence[slice]] = None,
            calculate_max: bool = False,
            element_names: typing.Optional[typing.Union[list[str], list[base.Output]]] = None,
            offset: typing.Optional[list] = None,
            requires_indexing: typing.Optional[bool] = None,
            geometries: typing.Optional[list[base.Output]] = None,
            ignore_missing_metadata: list[str] = ()
    ) -> None:
        """
        Stores a data set in the store.

        Args:

            name: The name of the data set.
            values: The values of the data set.
            scales: The scales to which the values of the data set apply.
            default: The default value for a new value array.
            unit: The physical unit of the values.
            shape: The shape of a newly created empty array.
            data_type: The datatype of a newly created empty array.
            chunks: The chunk size for a newly created empty array.
            create: Specifies whether a data set should be created or not.
            slices: Defines the portion of the data set that was passed to the function.
            calculate_max: Specifies whether the data set should keep track of the maximum value.
            element_names: Specifies datasets by name that contain the identifiers of named elements per scale.
            offset: Specifies the origin of an axis along the consecutive elements of a scale.
            requires_indexing: Specifies whether retrieving values later on strictly requires coordinates.
            geometries: Specifies datasets that contain the spatial extents per scale.
            ignore_missing_metadata: A list of metadata names that are expected by a scale and are not passed to the
            function but still should not result in a warning.

        Returns:
            Nothing.
        """

        def create_link(
                target_dataset: typing.Union[str, h5py.h5r.Reference],
                source_dataset: str,
                attribute: str,
                expected_length: int
        ) -> None:
            """
            Creates a reference link within the HDF5 data store or adds it to the list of links that should be created
            as soon as possible, if the target dataset currently does not exist.

            Args:
                target_dataset: The full dataset name of the referenced dataset.
                source_dataset: The full dataset name of the source dataset.
                attribute: The name of the attribute in the source dataset that should be linked to the target dataset.
                expected_length: The number of elements that is expected to be present in the target dataset. A message
                    is send if the actual number is unequal to the expected number.

            Returns:
                Nothing.
            """
            if isinstance(target_dataset, h5py.h5r.Reference) or target_dataset in self._f:
                self._f[source_dataset].attrs[attribute] = self._f[target_dataset].ref
                if self._f[target_dataset].shape != (expected_length,):
                    self._observer.store_set_values(
                        2,
                        "X3dfStore",
                        f"Number of elements in {source_dataset} and {target_dataset} do not fit"
                    )
            else:
                self._pending_links.setdefault(target_dataset, set()).add((source_dataset, attribute, expected_length))

        geometries: list[typing.Union[str, h5py.h5r.Reference, None]]
        element_names: list[typing.Union[str, h5py.h5r.Reference, None]]
        if default is not None and default != 0:
            self._observer.write_message(2, "Default value not supported by X3dfStore")
        dimension_count = 1
        if isinstance(values, bool):
            self._f[name] = values
            self._f[name].attrs["_type"] = "bool"
        elif isinstance(values, float):
            self._f[name] = values
            self._f[name].attrs["_type"] = "float"
        elif isinstance(values, int):
            self._f[name] = values
            self._f[name].attrs["_type"] = "int"
        elif isinstance(values, list):
            if all(isinstance(x, bytes) for x in values):
                # noinspection PyUnresolvedReferences
                data_type = h5py.vlen_dtype(numpy.uint8)
                data_set = self._f.create_dataset(
                    name, (len(values),), dtype=data_type, compression="gzip", chunks=(1,))
                for i in range(len(values)):
                    data_set[i] = numpy.fromstring(values[i], dtype=numpy.uint8)
                self._f[name].attrs["_type"] = "list[bytes]"
            elif all(isinstance(x, float) for x in values):
                self._f[name] = values
                self._f[name].attrs["_type"] = "list[float]"
            elif all(isinstance(x, int) for x in values):
                self._f[name] = values
                self._f[name].attrs["_type"] = "list[int]"
            elif all(isinstance(x, str) for x in values):
                # noinspection PyUnresolvedReferences
                data_type = h5py.string_dtype()
                data_set = self._f.create_dataset(name, (len(values),), dtype=data_type)
                for i in range(len(values)):
                    data_set[i] = values[i]
                data_set.attrs["_type"] = "list[str]"
            else:
                # noinspection PyUnresolvedReferences
                data_type = h5py.vlen_dtype(numpy.uint8)
                data_set = self._f.create_dataset(name, (len(values),), dtype=data_type)
                for i in range(len(values)):
                    data_set[i] = numpy.fromstring(pickle.dumps(values[i], 0), dtype=numpy.uint8)
                data_set.attrs["_type"] = "list[object]"
                self._observer.store_set_values(3, "X3dfStore", "Stored list of pickled objects")
        elif isinstance(values, str):
            self._f[name] = values
            self._f[name].attrs["_type"] = "str"
        elif isinstance(values, tuple):
            if all(isinstance(x, float) for x in values):
                self._f[name] = values
                self._f[name].attrs["_type"] = "tuple[float]"
            else:
                raise TypeError(f"Unsupported type of tuple: {values}")
        elif isinstance(values, type):
            type_name = f"{values.__module__}.{values.__qualname__}"
            # noinspection SpellCheckingInspection
            if type_name == "numpy.ndarray":
                data_set = self._f.create_dataset(
                    name, compression="gzip",
                    shape=shape,
                    dtype=data_type,
                    chunks=chunks,
                    fillvalue=numpy.nan if default is None else default
                )
                # noinspection SpellCheckingInspection
                data_set.attrs["_type"] = "numpy.ndarray"
                dimension_count = len(shape)
            elif type_name == "base.Values.ExistingValues":
                pass
            else:
                raise TypeError(f"Unsupported type: {type(values)}")
        elif isinstance(values, datetime.datetime):
            self._f[name] = str(values)
            self._f[name].attrs["_type"] = "datetime.datetime"
        elif isinstance(values, datetime.date):
            self._f[name] = str(values)
            self._f[name].attrs["_type"] = "datetime.date"
        elif isinstance(values, numpy.ndarray):
            if create:
                data_set = self._f.create_dataset(
                    name,
                    values.shape,
                    values.dtype,
                    compression="gzip",
                    chunks=chunks
                )
                # noinspection SpellCheckingInspection
                data_set.attrs["_type"] = "numpy.ndarray"
            else:
                data_set = self._f[name]
            if slices:
                data_set[slices] = values
            else:
                data_set[()] = values
            if calculate_max:
                data_set.attrs["max"] = values.max(initial=data_set.attrs["max"] if "max" in data_set.attrs else 0)
            dimension_count = len(values.shape)
        elif isinstance(values, type(None)):
            self._f[name] = numpy.zeros((0,))
            self._f[name].attrs["_type"] = "None"
        else:
            raise TypeError(f"Cannot store objects of type {type(values)} in X3df")
        if create:
            element_names = None if element_names is None else [
                x.store_name if isinstance(x, base.Output) else x for x in element_names]
            geometries = None if geometries is None else [
                x.store_name if isinstance(x, base.Output) else x for x in geometries]
            if element_names is not None and len(element_names) != dimension_count:
                self._observer.store_set_values(2, "X3dfStore", f"Element names and dimensionality of {name} do not fit")
            if geometries is not None and len(geometries) != dimension_count:
                self._observer.store_set_values(2, "X3dfStore", f"Geometries and dimensionality of {name} do not fit")
            if any([x.endswith("_element_names") for x in self._f[name].attrs]):
                if element_names is not None:
                    raise ValueError(f"Cannot override existing element names for {name}")
                element_names = [None] * dimension_count
                for element_names_dim in [x for x in self._f[name].attrs if x.endswith("_element_names")]:
                    element_names[int(element_names_dim.removeprefix("dim").removesuffix("_element_names"))] = self._f[
                        name].attrs[element_names_dim]
            if any([x.endswith("_geometries") for x in self._f[name].attrs]):
                if geometries is not None:
                    raise ValueError(f"Cannot override existing geometries for {name}")
                geometries = [None] * dimension_count
                for geometries_dim in [x for x in self._f[name].attrs if x.endswith("_geometries")]:
                    geometries[int(geometries_dim.removeprefix("dim").removesuffix("_geometries"))] = self._f[
                        name].attrs[geometries_dim]
            if any([x.endswith("_offset") for x in self._f[name].attrs]):
                if offset is not None:
                    raise ValueError(f"Cannot override existing offsets for {name}")
                offset = [None] * dimension_count
                for offset_dim in [x for x in self._f[name].attrs if x.endswith("_offset")]:
                    offset[int(offset_dim.removeprefix("dim").removesuffix("_offset"))] = self._f[name].attrs[offset_dim]
            if "scales" in self._f[name].attrs:
                if scales is not None and scales != ", ".join(self._f[name].attrs["scales"]):
                    raise ValueError(f"Cannot override existing scales definition for {name}")
                scales = ", ".join(self._f[name].attrs["scales"])
            if scales is None:
                self._observer.store_set_values(3, "X3dfStore", f"No scales provided for {name}")
            else:
                scales_list = scales.split(", ")
                if len(scales_list) != dimension_count:
                    self._observer.store_set_values(2, "X3dfStore", f"Scales and dimensionality of {name} do not fit")
                self._f[name].attrs["scales"] = scales_list
                for dim, scale in enumerate(scales_list):
                    element_description = self._known_scales.get(scale)
                    if element_description in ("named", "named geometries"):
                        if "element_names" not in ignore_missing_metadata:
                            if element_names is None or element_names[dim] is None:
                                self._observer.store_set_values(
                                    2, "X3dfStore", f"{name} did not specify element names for {scale}")
                        if offset is not None and offset[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Offset provided for {scale} that does not require an offset")
                        if element_description == "named" and geometries is not None and geometries[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Geometries provided for {scale} that does not require geometries")
                    elif element_description == "plain":
                        if element_names is not None and element_names[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Names provided for {scale} that does not require named elements")
                        if offset is not None and offset[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Offset provided for {scale} that does not require an offset")
                        if geometries is not None and geometries[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Geometries provided for {scale} that does not require geometries")
                    elif element_description == "offset" or (
                            scale.startswith("space_x/") or scale.startswith("space_y/")) and scale.endswith("sqm"):
                        if offset is None or offset[dim] is None:
                            self._observer.store_set_values(
                                2, "X3dfStore", f"{name} did not specify an offset for {scale}")
                        if element_names is not None and element_names[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Names provided for {scale} that does not require named elements")
                        if geometries is not None and geometries[dim] is not None:
                            self._observer.store_set_values(
                                3, "X3dfStore", f"Geometries provided for {scale} that does not require geometries")
                    else:
                        self._observer.store_set_values(2, "X3dfStore", f"Unknown scale: {scale}")
                    if element_names is not None and element_names[dim] is not None:
                        create_link(element_names[dim], name, f"dim{dim}_element_names", self._f[name].shape[dim])
                    if offset is not None and offset[dim] is not None:
                        if scale in ("time/day", "time/hour"):
                            stored_offset = str(offset[dim])
                        else:
                            stored_offset = offset[dim]
                        self._f[name].attrs[f"dim{dim}_offset"] = stored_offset
                    if element_description == "named geometries":
                        if (
                                (geometries is None or geometries[dim] is None) and
                                "geometries" not in ignore_missing_metadata
                        ):
                            self._observer.store_set_values(
                                2, "X3dfStore", f"{name} did not specify geometries for {scale}")
                    if geometries is not None and geometries[dim] is not None:
                        create_link(geometries[dim], name, f"dim{dim}_geometries", self._f[name].shape[dim])
            if unit is not None:
                self._f[name].attrs["unit"] = unit
            if requires_indexing and not isinstance(values, numpy.ndarray):
                raise ValueError(f"Required indexing is not supported for data of type {type(values)}")
            self._f[name].attrs["requires_indexing"] = bool(requires_indexing)
        pending_links = self._pending_links.pop(name, set())
        for pending_link in pending_links:
            create_link(name, pending_link[0], pending_link[1], pending_link[2])

    def has_dataset(self, name: str, partial: bool = False) -> bool:
        """
        Checks whether a dataset exists in the store or not.

        Args:
            name: The name of the dataset.
            partial: Specifies whether to also check partial dataset paths or not.

        Returns:
            A boolean value indicating whether the dataset exists or not.
        """
        if partial:
            return name.split("/")[0] in self._f
        else:
            return name in self._f
