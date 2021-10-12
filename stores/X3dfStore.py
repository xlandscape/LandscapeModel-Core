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

    def close(self) -> None:
        """
        Closes the store.

        Returns:
            Nothing.
        """
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
        return {
            "shape": data_set.shape,
            "data_type": data_set.dtype,
            "chunks": data_set.chunks,
            "unit": data_set.attrs.get("unit", None),
            "scales": data_set.attrs.get("scales", "global")
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
            if "slices" in keywords:
                values = data_set[keywords["slices"]]
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
            calculate_max: bool = False
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

        Returns:
            Nothing.
        """
        if default is not None and default != 0:
            self._observer.write_message(2, "Default value not supported by X3dfStore")
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
                data_set = self._f.create_dataset(name, (len(values),), dtype=data_type)
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
                data_set = self._f.create_dataset(name, compression="gzip", shape=shape, dtype=data_type, chunks=chunks)
                # noinspection SpellCheckingInspection
                data_set.attrs["_type"] = "numpy.ndarray"
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
        elif isinstance(values, type(None)):
            self._f[name] = numpy.zeros((0,))
            self._f[name].attrs["_type"] = "None"
        else:
            raise TypeError(f"Cannot store objects of type {type(values)} in X3df")
        if scales is not None:
            self._f[name].attrs["scales"] = scales
        if unit is not None:
            self._f[name].attrs["unit"] = unit
        return

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
