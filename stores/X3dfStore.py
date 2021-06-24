"""
A class encapsulating an X3df data store.
"""

import datetime
import h5py
import numpy
import os
import pickle
import glob
import shutil
import base


class X3dfStore(base.Store):
    """
    Encapsulates an X3df data store for usage in the Landscape Model.

    PARAMETERS
    file_path: The file path and name for the HDF5 tom use.
    observer: A observer that handles the messages emitted by the store.
    mode: The file mode with which the HDF5 is opened.
    initialization: File path and name to an existing X3dfStore which contains data used for initializing the current
    store.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "store.X3dfStore")
    base.VERSION.changed("1.1.5", "store.X3dfStore scale information for numpy arrays if provided")
    base.VERSION.changed("1.1.5", "store.X3dfStore can calculate maximum for numpy arrays")
    base.VERSION.changed("1.2.2", "store.X3dfStore now handles boolean values separately")
    base.VERSION.changed("1.2.16", "Slicing enabled for list[byte] in store.X3dfStore")
    base.VERSION.changed("1.2.20", "Support of dates and times in store.X3dfStore")
    base.VERSION.changed("1.2.25", "Support of NoneType in store.X3dfStore")
    base.VERSION.changed("1.2.37", "Specified X3df file mode in store.X3dfStore")
    base.VERSION.changed("1.2.37", "Ability to open X3df in different modes in store.X3dfStore")
    base.VERSION.changed("1.2.37", "store.X3dfStore refactored")
    base.VERSION.changed("1.3.27", "store.X3dfStore acknowledges scales keyword for all value types")
    base.VERSION.changed("1.3.27", "store.X3dfStore default keyword added")
    base.VERSION.changed("1.3.27", "store.X3dfStore slice keyword renamed to slices")
    base.VERSION.changed("1.3.33", "store.X3dfStore no longer casts list[bytes] to bytes")
    base.VERSION.changed("1.3.33", "store.X3dfStore can store and read lists of strings")
    base.VERSION.changed("1.3.33", "store.X3dfStore is explicit about its parameters")
    base.VERSION.changed("1.3.33", "store.X3dfStore stores physical unit if specified")
    base.VERSION.changed("1.3.33", "store.X3dfStore.describe() outputs scales")
    base.VERSION.changed("1.3.35", "store.X3dfStore can be initialized using existing data")
    base.VERSION.added("1.3.35", "store.X3dfStore.has_dataset()")
    base.VERSION.added("1.4.1", "Changelog in store.X3dfStore")
    base.VERSION.changed("1.4.1", "store.X3dfStore class documentation")
    base.VERSION.changed("1.4.6", "identifier argument of initializer, parent run no longer randomly sampled")
    base.VERSION.fixed("1.4.8", "conversion of MC identifier to integer")

    def __init__(self, file_path, observer=None, mode="a", initialization=None, identifier=0):
        hdf5_file = os.path.join(file_path, "arr.dat")
        if mode != "r":
            try:
                os.makedirs(file_path)
            except FileExistsError:
                raise FileExistsError("Cannot create store if it already exists: " + file_path)
            observer.write_message(4, "Creating new X3dfStore at", file_path)
        if initialization is not None:
            available_runs = glob.glob(initialization)
            if len(available_runs) < 1:
                raise ValueError("No runs found at " + initialization)
            selected_source_run = available_runs[int(identifier) % len(available_runs)]
            observer.write_message(4, "Initializing data store from", selected_source_run)
            shutil.copyfile(selected_source_run, hdf5_file)
        self._f = h5py.File(hdf5_file, mode)
        self._observer = observer
        return

    def close(self):
        """
        Closes the data store.
        :return:
        """
        self._f.close()
        return

    def describe(self, name):
        """
        Returns metadata about a data set.
        :param name: The name of the data set.
        :return: A dictionary containing metadata about the data set.
        """
        data_set = self._f[name]
        return {
            "shape": data_set.shape,
            "data_type": data_set.dtype,
            "chunks": data_set.chunks,
            "unit": data_set.attrs.get("unit", None),
            "scales": data_set.attrs.get("scales", "global")
        }

    def get_values(self, name, **keywords):
        """
        Retrieves values from a data set.
        :param name: The name of the data set.
        :param keywords: Additional keywords controlling how to retrieve values.
        :return: The values of the data set in their corresponding type.
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
            values = str(data_set[()])
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
            values = datetime.datetime.strptime(data_set[()], "%Y-%m-%d").date()
        elif original_type == "numpy.ndarray":
            if "slices" in keywords:
                values = data_set[keywords["slices"]]
            else:
                values = data_set[()]
        elif original_type == "datetime.datetime":
            values = datetime.datetime.strptime(data_set[()], "%Y-%m-%d %H:%M:%S")
        elif original_type == "None":
            values = None
        elif original_type == "list[str]":
            values = data_set[()].tolist()
        else:
            raise TypeError("Stored type cannot be interpreted: " + original_type)
        return values

    def set_values(
            self,
            name,
            values,
            scales=None,
            default=None,
            unit=None,
            shape=None,
            data_type=None,
            chunks=None,
            create=True,
            slices=None,
            calculate_max=False
    ):
        """
        Sets the values of a data set.
        :param name: The name of the data set.
        :param values: The new values of the data set.
        :param scales: The scales to which the values apply.
        :param default: The default value for a new value array.
        :param unit: The physical unit of the values.
        :param shape: The shape of a newly created empty array.
        :param data_type: The data type of a newly created empty array.
        :param chunks: The chunk size for a newly created empty array.
        :param create: Specifies whether a data set should be created or not.
        :param slices: Defines the portion of the data set that was passed to the function.
        :param calculate_max: Specifies whether the data set should keep track of the maximum value.
        :return: Nothing.
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
                    data_set[i] = numpy.fromstring(str(pickle.dumps(values[i], 0)), dtype=numpy.uint8)
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
                raise TypeError("Unsupported type of tuple: " + str(values))
        elif isinstance(values, type):
            type_name = values.__module__ + "." + values.__qualname__
            # noinspection SpellCheckingInspection
            if type_name == "numpy.ndarray":
                data_set = self._f.create_dataset(name, compression="gzip", shape=shape, dtype=data_type, chunks=chunks)
                # noinspection SpellCheckingInspection
                data_set.attrs["_type"] = "numpy.ndarray"
            else:
                raise TypeError("Unsupported type: " + str(type(values)))
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
            raise TypeError("Cannot store objects of type " + str(type(values)) + " in X3df")
        if scales is not None:
            self._f[name].attrs["scales"] = scales
        if unit is not None:
            self._f[name].attrs["unit"] = unit
        return

    def has_dataset(self, name, partial=False):
        """
        Checks whether a dataset exists in the store or not.
        :param name: The name of the dataset.
        :param partial: Specifies whether to also check partial dataset paths or not.
        :return: A boolean value indicating whether the dataset exists or not.
        """
        if partial:
            return name.split("/")[0] in self._f
        else:
            return name in self._f
