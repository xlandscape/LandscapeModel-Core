"""This file contains various helper functions used throughout Landscape Model code."""
import xml.etree.ElementTree

import datetime
import functools
import importlib
import math
import numpy as np
import operator
import subprocess
import os
import base
import inspect
import typing


# CHANGELOG
base.VERSION.added("1.1.1", "`base.functions` providing helper functions")
base.VERSION.changed("1.2.1", "`base.functions.replaceTokens()` allows macros in source path")
base.VERSION.fixed("1.2.3", "`base.functions.chunkSlices()` indexing")
base.VERSION.changed("1.2.17", "`base.functions.replaceTokens()` accepts non-string values")
base.VERSION.changed("1.3.5", "`base.functions.replaceTokens()` replaces $$-tokens before $-tokens")
base.VERSION.changed("1.3.5", "`base.functions `refactored")
base.VERSION.changed("1.3.13", "Option to disable observers in configuration by `base.functions.observers_from_xml()` ")
base.VERSION.changed(
    "1.3.20", "`base.functions.observers_from_xml()` enables/disables observers also through expression")
base.VERSION.changed("1.3.20", "`base.functions.convert()` separator of list[str] parameters changed to |")
base.VERSION.fixed(
    "1.3.24", "`base.functions.chunkSlices()` determining chunk size when dimensions have the same extent")
base.VERSION.added("1.3.24", "`base.functions.run_process()` for invoking system processes")
base.VERSION.fixed("1.3.33", "`base.functions.convert()` crashes with empty lists")
base.VERSION.changed("1.3.35", "`base.functions.run_process()` manages system environment variables")
base.VERSION.fixed("1.3.35", "`base.functions.replace_tokens()` treats None values as empty string")
base.VERSION.added("1.4.1", "Changelog in `base.functions` ")
base.VERSION.fixed("1.4.1", "`base.functions.observers_from_xml()` passes lock argument only if needed by observer")
base.VERSION.changed("1.4.3", "`base.functions.convert()` can evaluate values")
base.VERSION.added("1.4.5", "`base.functions.reporting()` ")
base.VERSION.changed("1.4.9", "`base.functions` changelog uses markdown for code elements")
base.VERSION.changed("1.4.11", "parsing of XML parameters strips whitespaces in `base.functions` ")
base.VERSION.fixed("1.5.4", "stripping of raw configuration values in `base.functions` ")
base.VERSION.changed("1.5.4", "parsing of raw parameters in `base.functions` ")
base.VERSION.added("1.5.9", "`base.functions.run_process()` option to run external processes minimized")
base.VERSION.added("1.6.5", "`base.functions.run_process()` makes use of new Python dict union operator")
base.VERSION.added("1.7.0", "Type hints to `base.functions` ")
base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.functions` ")
base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.functions` ")
base.VERSION.changed(
    "1.9.1", "Check if module R instances are sufficiently encapsulated in `base.functions.run_process()` ")


def cartesian_product(*arrays: np.ndarray) -> np.ndarray:
    """
    Returns the Cartesian product of two or more arrays.

    Args:
        arrays: The arrays from which the Cartesian product is calculated.

    Returns:
        The Cartesian product of the input arrays.
    """
    number_arrays = len(arrays)
    data_type = np.result_type(*arrays)
    result_array = np.empty([len(a) for a in arrays] + [number_arrays], dtype=data_type)
    for i, array in enumerate(np.ix_(*arrays)):
        result_array[..., i] = array
    return result_array.reshape(-1, number_arrays)


def chunk_slices(shape: typing.Sequence[int], chunks: typing.Sequence[int]) -> list[tuple[slice]]:
    """
    Returns an array of tuples specifying chunks of a multidimensional array.

    Args:
        shape: The shape of the array to be sliced into chunks.
        chunks: The required chunk size.

    Returns:
        An array of ranges that specify the chunks within the provided shape.
    """
    arrays = []
    for i in range(len(shape)):
        arrays.append(np.arange(0, shape[i], chunks[i]))
    chunk_indices = cartesian_product(*arrays)
    ranges = []
    for i in range(chunk_indices.shape[0]):
        dimension_ranges = [slice(chunk_indices[i, j],
                                  shape[j] if chunk_indices[i, j] + chunks[j] > shape[j] else
                                  chunk_indices[i, j] + chunks[j]) for j in range(len(shape))]
        ranges.append(tuple(dimension_ranges))
    return ranges


def chunk_size(chunk: typing.Sequence[int], shape: typing.Sequence[int]) -> tuple[int]:
    """
    Calculates a chunk size for a multidimensional array.

    Args:
        chunk: The requested chunk size.
        shape: The shape of the multidimensional array.

    Returns:
        The calculated chunk size.
    """
    result = [0] * 3
    divisor = [1] * 3
    max_chunk_elements = 2 ** 16
    for i in range(len(chunk)):
        if chunk[i] is None:
            result[i] = shape[i]
        else:
            result[i] = chunk[i]
            divisor[i] = 9999
    while functools.reduce(operator.mul, result) > max_chunk_elements:
        minimum_divisor_index = min(enumerate(divisor), key=operator.itemgetter(1))
        if isinstance(minimum_divisor_index, tuple):
            minimum_divisor_index = minimum_divisor_index[0]
        divisor[minimum_divisor_index] += 1
        result[minimum_divisor_index] = math.ceil(shape[minimum_divisor_index] / divisor[minimum_divisor_index])
    return tuple(result)


def convert(input_config: xml.etree.ElementTree.Element) -> typing.Optional[
    typing.Union[bool, datetime.date, float, int, list[int], list[float], list[str], datetime.datetime, str]
]:
    """
    Converts a configuration value into a Python value.

    Args:
        input_config: The input type configuration.

    Returns:
        A Python value of the configured type.
    """
    text_value = None if input_config.text is None else input_config.text.strip()
    raw_value = eval(text_value) if "eval" in input_config.attrib \
                                    and input_config.attrib["eval"].lower() == "true" else text_value
    if "type" in input_config.attrib:
        if input_config.attrib["type"] == "bool":
            value = raw_value.lower() == "true"
        elif input_config.attrib["type"] == "date":
            value = datetime.datetime.strptime(raw_value, "%Y-%m-%d").date()
        elif input_config.attrib["type"] == "float":
            value = float(raw_value)
        elif input_config.attrib["type"] == "int":
            value = int(raw_value)
        elif input_config.attrib["type"] == "list[int]":
            value = [int(x) for x in raw_value.split()] if raw_value else []
        elif input_config.attrib["type"] == "list[float]":
            value = [float(x) for x in raw_value.split()] if raw_value else []
        elif input_config.attrib["type"] == "list[str]":
            value = [x for x in raw_value.split("|")] if raw_value else []
        elif input_config.attrib["type"] == "datetime":
            value = datetime.datetime.strptime(raw_value, "%Y-%m-%d %H:%M")
        else:
            raise ValueError(f"Unsupported type of input '{input_config.tag}': {input_config.attrib['type']}")
    else:
        value = raw_value
    return value


def observers_from_xml(observers_xml: xml.etree.ElementTree.Element, **keywords) -> list[base.Observer]:
    """
    Instantiates Landscape Model observers according to an XML configuration.

    Args:
        observers_xml: The observer configuration XML.
        **keywords: Additional passed to the observer constructors.

    Returns:
        A list of observer instances.
    """
    observers = []
    for observerConfig in observers_xml.findall("Observer"):
        if ("enabled" not in observerConfig.attrib or observerConfig.attrib["enabled"] == "true") and (
                "enabled_expression" not in observerConfig.attrib or eval(observerConfig.attrib["enabled_expression"])):
            observer_module = importlib.import_module(observerConfig.attrib["module"])
            observer_params = dict(keywords)
            for observerParam in observerConfig:
                observer_params[observerParam.tag.lower()] = convert(observerParam)
            observer_init = getattr(observer_module, observerConfig.attrib["class"]).__init__
            observer_init_args = inspect.getfullargspec(observer_init)
            if "lock" in observer_params and not (
                    "lock" in observer_init_args.args or observer_init_args.varkw is not None):
                del observer_params["lock"]
            observer = getattr(observer_module, observerConfig.attrib["class"])(**observer_params)
            observers.append(observer)
    return observers


def replace_tokens(tokens: typing.Mapping[str, str], source: str, destination: str) -> None:
    """
    Replaces tokens in a text file and writes the resulting text to another file.

    Args:
        tokens: The recognized tokens and their values.
        source: The source file.
        destination: The destination file.

    Returns:
        Nothing.
    """
    parsed_source = source
    for key, value in tokens.items():
        parsed_source = parsed_source.replace(f"$({key})", str(value or ""))
    with open(parsed_source) as file:
        configuration = file.read()
        for key, value in tokens.items():
            configuration = configuration.replace(f"$$({key})", str(value or ""))
        for key, value in tokens.items():
            configuration = configuration.replace(f"$({key})", str(value or ""))
        with open(destination, "w") as f:
            f.write(configuration)


def run_process(
        command: typing.Sequence[str],
        working_directory: str,
        observer: base.Observer,
        env: typing.Optional[typing.Mapping[str, str]] = None,
        minimized: bool = True
) -> None:
    """
    Runs a separate process.

    Args:
        command: A list describing the process call.
        working_directory: The working directory for the process.
        observer: The observer used for the process.
        env: A dictionary of environment variables available to the new process.
        minimized: Specifies whether to start the process minimized.

    Returns:
        Nothing.
    """
    if env is None:
        env = {}
    if os.path.basename(command[0]).lower() in ("r.exe", "rscript.exe", ):
        env = {"HOME": working_directory, "R_USER": working_directory} | env
        if "R_LIBS_USER" not in env:
            observer.write_message(2, f"Presumably starting R instance, but R_LIBS_USER not set")
    startupinfo = subprocess.STARTUPINFO()
    if minimized:
        startupinfo.dwFlags = subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = 6
    result = subprocess.Popen(
        command,
        cwd=working_directory,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        env=env | {"SystemRoot": os.getenv("SystemRoot")},
        startupinfo=startupinfo
    )
    for text in iter(result.stdout.readline, ''):
        observer.write(text)
    result.stdout.close()
    result.wait()


def reporting(
        data_store: str,
        reporting_element_class: typing.Type[base.Component],
        parameters: typing.Sequence[tuple[str, typing.Any]],
        links: typing.Sequence[tuple[str, typing.Any]]
) -> None:
    """
    Runs a reporting element in a default reporting environment.

    Args:
        data_store: The file path where the X3df store is located.
        reporting_element_class: The class of the reporting element.
        parameters: A list of name-value tuples defining parameters.
        links: A list of name-dataset tuples defining links.

    Returns:
        Nothing.
    """
    import observer
    import stores
    import components

    console_observer = observer.ConsoleObserver(print_output=True)
    x3df_store = stores.X3dfStore(data_store, console_observer, "r")
    in_memory_store = stores.InMemoryStore()
    reporting_element = reporting_element_class.__new__(reporting_element_class)
    reporting_element.__init__("ReportingElement", console_observer, None)
    parameters_definition = [components.UserParameter(name, value, "global") for name, value in parameters]
    user_parameters = components.UserParameters(
        "UserParameters", parameters_definition, console_observer, in_memory_store)
    for name, value in parameters:
        if value is not None:
            reporting_element.inputs[name] = user_parameters.outputs[name]
    for name, dataset in links:
        reporting_element.inputs[name] = base.Output(dataset, x3df_store)
    reporting_element.run()
