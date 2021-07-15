"""
Class definition of a Landscape Model SqlLite store.
"""

import sqlite3
import os
import base
import datetime
import numpy as np
import functools
import operator


class SqlLiteStore(base.Store):
    """
    Writes simulation data into a SqlLite database.

    PARAMETERS
    file_path: The path and file name of the SqlLite database to be used.
    observer: An observer that handles the messages emitted by the store.
    """
    # CHANGELOG
    base.VERSION.added("1.3.27", "`store.SqlLiteStore` ")
    base.VERSION.added("1.4.1", "Changelog in `store.SqlLiteStore`")
    base.VERSION.changed("1.4.1", "`store.SqlLiteStore` has now `base.Store` as superclass")
    base.VERSION.changed("1.4.1", "`store.SqlLiteStore` class documentation")
    base.VERSION.added("1.4.1", "s`tore.SqlLiteStore.has_dataset()` ")
    base.VERSION.fixed("1.4.3", "`store.SqlLiteStore` can use existing directory")
    base.VERSION.fixed("1.4.3", "`store.SqlLiteStore` uses new version system")
    base.VERSION.changed("1.4.3", "`store.SqlLiteStore` got `create` argument for extending existing datasets")
    base.VERSION.changed("1.4.3", "`store.SqlLiteStore.set_values()` can add foreign keys")
    base.VERSION.added("1.4.3", "`store.SqlLiteStore.execute()` method")
    base.VERSION.changed("1.4.3", "`store.SqlLiteStore` manages physical units")
    base.VERSION.changed("1.4.4", "`store.SqlLiteStore` manages chunks")
    base.VERSION.changed("1.4.9", "`store.SqlLiteStore` data type access")

    def __init__(self, file_path, observer, create=True):
        self._observer = observer
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self._connection = sqlite3.connect(file_path)
        if create:
            self._connection.execute("CREATE TABLE global(store_version)")
            self._connection.execute("INSERT INTO global VALUES (?)", (str(base.VERSION.latest),))
            self._connection.execute("CREATE TABLE scales(scale, shape, PRIMARY KEY (scale))")
            self._connection.execute("""
                CREATE TABLE data_attributes(
                    data_name, 
                    scale, 
                    x3_type, 
                    unit,
                    chunks,
                    PRIMARY KEY (data_name), 
                    FOREIGN KEY (scale) REFERENCES scales(scale)
                )""")
            self._connection.execute("INSERT INTO scales VALUES ('global', '(1,)')")
            self._connection.commit()
        return

    def set_values(
            self,
            name,
            values,
            scales=None,
            shape=None,
            data_type=None,
            create=True,
            slices=None,
            default=None,
            foreign_keys=None,
            unit=None,
            chunks=None,
            **keywords
    ):
        """
        Writes values into the SqlLite database.
        :param name: The name of the value.
        :param values: The actual values.
        :param scales: The scales the values apply to.
        :param shape: The shape of the values if not obvious from the values.
        :param data_type: The type of the value if not obvious from the values.
        :param create: A boolean defining whether an entry in the database should be created or not (for appending).
        :param slices: Specifies a slice for partial updates of values.
        :param default: The default value if no actual value is given.
        :param foreign_keys: A list of foreign keys to add to the new dataset.
        :param unit: The unit of the values.
        :param chunks: The chunks defined for the dataset.
        :param keywords: Additional keywords.
        :return: Nothing.
        """
        if len(keywords) > 0:
            self._observer.write_message(2, "Ignoring keywords: {}".format(keywords))
        numpy_mappings = {float: "REAL", np.dtype("<f8"): "REAL", np.dtype("int32"): "INTEGER", np.dtype("<f4"): "REAL"}
        if create:
            if scales is None:
                self._observer.store_set_values(3, "SqlLiteStore",
                                                "No scale given for {}: assuming global".format(name))
            scale = scales if scales else "global"
        else:
            scale = self._connection.execute(
                "SELECT scale FROM data_attributes WHERE data_name = ?",
                (name,)).fetchone()[0]
        scale_info = self._connection.execute("SELECT shape FROM scales WHERE scale = ?", (scale,)).fetchone()
        if isinstance(values, str):
            data_type = "TEXT"
            encoded_values = ("'{}'".format(values))
            original_type = "str"
            stored_shape = (1,)
        elif isinstance(values, datetime.datetime):
            data_type = "TIMESTAMP"
            encoded_values = "'{}'".format(values)
            original_type = "datetime.datetime"
            stored_shape = (1,)
        elif isinstance(values, datetime.date):
            data_type = "DATE"
            encoded_values = "'{}'".format(values)
            original_type = "datetime.date"
            stored_shape = (1,)
        elif isinstance(values, float):
            data_type = "REAL"
            encoded_values = values
            original_type = "float"
            stored_shape = (1,)
        elif isinstance(values, bool):
            data_type = "INTEGER"
            encoded_values = 1 if values else 0
            original_type = "bool"
            stored_shape = (1,)
        elif values is None:
            data_type = "INTEGER"
            encoded_values = "NULL"
            original_type = "None"
            stored_shape = (1,)
        elif isinstance(values, list):
            if all(isinstance(x, int) for x in values):
                data_type = "INTEGER"
                original_type = "list[int]"
            elif all(isinstance(x, bytes) for x in values):
                data_type = "BLOB"
                original_type = "list[bytes]"
            elif all(isinstance(x, str) for x in values):
                data_type = "TEXT"
                original_type = "list[str]"
            elif all(isinstance(x, float) for x in values):
                data_type = "REAL"
                original_type = "list[float]"
            else:
                raise ValueError("Cannot store list: {}".format(values))
            encoded_values = [(x, i) for i, x in enumerate(values)]
            stored_shape = (len(values),)
        elif isinstance(values, tuple):
            if all(isinstance(x, float) for x in values):
                data_type = "REAL"
                original_type = "tuple[float]"
            else:
                raise ValueError("Cannot store tuple: {}".format(values))
            encoded_values = [(x, i) for i, x in enumerate(values)]
            stored_shape = (len(values),)
        elif isinstance(values, type):
            type_name = values.__module__ + "." + values.__qualname__
            if type_name == "numpy.ndarray":
                data_type = numpy_mappings[data_type]
                original_type = "numpy.ndarray"
                encoded_values = []
                stored_shape = shape
            else:
                raise ValueError("Cannot store type: {}".format(type_name))
        elif isinstance(values, np.ndarray):
            data_type = numpy_mappings[values.dtype]
            original_type = "numpy.ndarray"
            if slices:
                indices = [np.empty((0, ))] * len(slices)
                for i, dimension_slice in enumerate(slices):
                    if isinstance(dimension_slice, slice):
                        indices[i] = np.arange(dimension_slice.start or 0, dimension_slice.stop,
                                               dimension_slice.step or 1)
                    elif isinstance(dimension_slice, int):
                        indices[i] = np.full(1, dimension_slice, np.int)
                    else:
                        raise ValueError("Unsupported slice type: {}, dimension {}".format(dimension_slice, i))
                indices, stored_shape = self._cartesian_product(*indices)
                flattened_values = values.flatten()
                encoded_values = [[flattened_values[i]] + indices[i].tolist() for i in range(flattened_values.size)]
            else:
                stored_shape = values.shape
                encoded_values = [[x[1]] + list(x[0]) for x in np.ndenumerate(values)]
            if values.dtype == np.int:
                for i in range(len(encoded_values)):
                    encoded_values[i][0] = int(encoded_values[i][0])
            elif values.dtype in ["float32", "float64"]:
                for i in range(len(encoded_values)):
                    encoded_values[i][0] = float(encoded_values[i][0])
            else:
                raise ValueError("Cannot store numpy array values of type {}".format(values.dtype))
        else:
            raise ValueError("Cannot store values of type {} as {}: {}".format(type(values), name, values))
        if foreign_keys is None:
            fk_string = ""
        else:
            fk_string = "".join(
                [", FOREIGN KEY ({}) REFERENCES {}".format(["i", "j", "k"][x[0]], x[1]) for
                 x in enumerate(foreign_keys) if x[1]])
        if scale_info is None:
            if len(stored_shape) == 1:
                self._connection.execute("CREATE TABLE `{}` (i INTEGER, PRIMARY KEY (i){})".format(scale, fk_string))
                self._connection.executemany("INSERT INTO `{}` VALUES (?)".format(scale),
                                             [(i,) for i in range(stored_shape[0])])
            elif len(stored_shape) == 2:
                self._connection.execute("CREATE TABLE `{}` (i INTEGER, j INTEGER, PRIMARY KEY (i, j){})".format(
                    scale, fk_string))
                self._connection.executemany("INSERT INTO `{}` VALUES (?, ?)".format(scale),
                                             [(i, j) for i in range(stored_shape[0]) for j in range(stored_shape[1])])
            elif len(stored_shape) == 3:
                self._connection.execute(
                    "CREATE TABLE `{}` (i INTEGER, j INTEGER, k INTEGER, PRIMARY KEY (i, j, k){})".format(
                        scale, fk_string))
                self._connection.executemany("INSERT INTO `{}` VALUES (?, ?, ?)".format(scale),
                                             [(i, j, k) for i in range(stored_shape[0]) for j in range(stored_shape[1])
                                              for k in range(stored_shape[2])])
            else:
                raise ValueError("Unsupported number of dimensions: {}".format(stored_shape))
            self._connection.execute("INSERT INTO scales VALUES (?, ?)", (scale, str(stored_shape)))
            self._connection.commit()
            target_shape = stored_shape
        else:
            target_shape = eval(scale_info[0])
        if slices:
            if len(slices) != len(target_shape):
                raise ValueError(
                    "Wrong number of dimensions of {} slice: {}; expected: {}".format(name, slices, len(target_shape)))
        else:
            if stored_shape != target_shape:
                raise ValueError(
                    "Wrong target shape of value {}: {}; expected: {}".format(name, stored_shape, target_shape))
        if stored_shape == (1,) and create:
            self._connection.execute(
                "ALTER TABLE {} ADD COLUMN `{}` {} DEFAULT {}".format(scale, name, data_type, encoded_values))
        else:
            if create:
                if default is None:
                    self._connection.execute("ALTER TABLE `{}` ADD COLUMN `{}` {}".format(scale, name, data_type))
                else:
                    self._connection.execute(
                        "ALTER TABLE `{}` ADD COLUMN `{}` {} DEFAULT {}".format(scale, name, data_type, default))
            if len(stored_shape) == 1:
                self._connection.executemany("UPDATE `{}` SET `{}` = ? WHERE i = ?".format(scale, name), encoded_values)
            elif len(stored_shape) == 2:
                self._connection.executemany("UPDATE `{}` SET `{}` = ? WHERE i = ? AND j = ?".format(scale, name),
                                             encoded_values)
            elif len(stored_shape) == 3:
                self._connection.executemany(
                    "UPDATE `{}` SET `{}` = ? WHERE i = ? AND j = ? AND k = ?".format(scale, name), encoded_values)
            else:
                raise ValueError("Cannot handle shape: {}".format(stored_shape))
        if create:
            self._connection.execute(
                "INSERT INTO data_attributes VALUES(?, ?, ?, ?, ?)", (name, scale, original_type, unit, str(chunks)))
        self._connection.commit()
        return

    def get_values(self, name, slices=None, **keywords):
        """
        Retrieves values from the SqlLite database.
        :param name: The name of the value.
        :param slices: A slice for partial retrievals.
        :param keywords: Additional keywords.
        :return: The values in their original representation.
        """
        if len(keywords) > 0:
            raise ValueError("Unknown keywords: {}".format(keywords))
        data_info = self._connection.execute("SELECT scale, x3_type FROM data_attributes WHERE data_name = ?",
                                             (name,)).fetchone()
        if slices:
            ranges = self._slices_to_range_limits(slices)
            if len(slices) == 1:
                cursor = self._connection.execute(
                    "SELECT `{}` FROM `{}` WHERE i >= ? AND i < ? ORDER BY i".format(name, data_info[0]), ranges)
            elif len(slices) == 2:
                cursor = self._connection.execute(
                    "SELECT `{}` FROM `{}` WHERE i >= ? AND i < ? AND j >= ? AND j < ? ORDER BY i, j".format(name,
                                                                                                             data_info[
                                                                                                                 0]),
                    ranges)
            else:
                raise ValueError("Unsupported length of slice for value {}: {}".format(name, slices))
        else:
            cursor = self._connection.execute("SELECT `{}` FROM `{}`".format(name, data_info[0]))
        if data_info[1] in ["str", "float"]:
            return cursor.fetchone()[0]
        elif data_info[1] == "datetime.date":
            return datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()
        elif data_info[1] in ["list[int]", "list[bytes]", "list[str]", "list[float]"]:
            data = [x[0] for x in cursor.fetchall()]
            return data[0] if len(data) == 1 else data
        elif data_info[1] == "tuple[float]":
            return tuple([x[0] for x in cursor.fetchall()])
        elif data_info[1] == "bool":
            return cursor.fetchone()[0] == 1
        elif data_info[1] == "None":
            return None
        elif data_info[1] == "numpy.ndarray":
            if slices:
                ranges = self._slices_to_range_limits(slices)
                target_shape = tuple([ranges[2 * x + 1] - ranges[2 * x] for x in range(len(slices))])
            else:
                target_shape = eval(
                    self._connection.execute("SELECT shape FROM scales WHERE scale = ?", (data_info[0],)).fetchone()[0])
            table_info = self._connection.execute("PRAGMA table_info(`{}`)".format(data_info[0])).fetchall()
            data_type = [x[2] for x in table_info if x[1] == name][0]
            if data_type in ["INTEGER", "REAL"]:
                return np.asarray([x[0] for x in cursor.fetchall()]).reshape(target_shape)
            else:
                raise ValueError("Data type {} cannot be converted into a NumPy array".format(data_type))
        elif data_info[1] == "datetime.datetime":
            return datetime.datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")
        raise TypeError("Stored type cannot be interpreted: " + data_info[1])

    @staticmethod
    def _cartesian_product(*arrays):
        # adapted from https://stackoveflow.com/questions/11144513
        la = len(arrays)
        data_type = np.result_type(*arrays)
        arr = np.empty([len(a) for a in arrays] + [la], dtype=data_type)
        for i, a in enumerate(np.ix_(*arrays)):
            arr[..., i] = a
        return arr.reshape(-1, la), arr.shape[:-1]

    def describe(self, name):
        """
        Describes a data set.
        :param name: The name of the data set.
        :return: A dictionary containing information about the data set.
        """
        type_mappings = {"REAL": np.float}
        data_info = self._connection.execute("SELECT scale FROM data_attributes WHERE data_name = ?",
                                             (name,)).fetchone()
        scale_info = self._connection.execute("SELECT shape FROM scales WHERE scale = ?", (data_info[0],)).fetchone()
        table_info = self._connection.execute("PRAGMA table_info(`{}`)".format(data_info[0])).fetchall()
        data_type = [x[2] for x in table_info if x[1] == name][0]
        unit = self._connection.execute("SELECT unit FROM data_attributes WHERE data_name = ?", (name,)).fetchone()
        return {"shape": eval(scale_info[0]), "data_type": type_mappings[data_type], "chunks": None, "unit": unit[0]}

    @staticmethod
    def _slices_to_range_limits(slices):
        ranges = [(0, 0)] * len(slices)
        for i, dimension_slice in enumerate(slices):
            if isinstance(dimension_slice, slices):
                if dimension_slice.step is not None and dimension_slice.step != 1:
                    raise ValueError("Steps in slices are not supported")
                ranges[i] = (dimension_slice.start or 0, dimension_slice.stop)
            elif isinstance(dimension_slice, int):
                ranges[i] = (dimension_slice, dimension_slice + 1)
            else:
                raise ValueError("Unsupported slice type: {}".format(dimension_slice))
        return functools.reduce(operator.iconcat, ranges, [])

    def close(self):
        """
        Closes the database connection.
        :return: Nothing.
        """
        self._connection.close()
        return

    def has_dataset(self, name, partial=False):
        """
        Indicates whether the store contains a data set.
        :param name: The name of the dataset.
        :param partial: Indicates whether a partial match should be performed or not.
        :return: A boolean value indicating whether the dataset was found within the store.
        """
        if partial:
            hits = self._connection.execute(
                "SELECT data_name FROM data_attributes WHERE data_name LIKE ?", ("%" + name + "%",)).rowcount
        else:
            hits = self._connection.execute(
                "SELECT data_name FROM data_attributes WHERE data_name = ?", (name,)).rowcount
        return hits > 0

    def execute(self, sql):
        """
        Executes a SQL query within the SqlLite store.
        :param sql: The SQL query to execute
        :return: Nothing.
        """
        self._connection.execute(sql)
        return
