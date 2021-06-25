"""
This file contains various helper functions used throughout Landscape Model code.
"""
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
base.VERSION.changed("1.4.11", "parsing of XML parameters strips whitespaces")


def cartesian_product(*arrays):
    """
    Returns the Cartesian product of two or more arrays.
    :param arrays: The arrays from which the Cartesian product is calculated.
    :return: The Cartesian product of the input arrays.
    """
    number_arrays = len(arrays)
    data_type = np.result_type(*arrays)
    result_array = np.empty([len(a) for a in arrays] + [number_arrays], dtype=data_type)
    for i, array in enumerate(np.ix_(*arrays)):
        result_array[..., i] = array
    return result_array.reshape(-1, number_arrays)


def chunk_slices(shape, chunks):
    """
    Returns an array of tuples specifying chunks of an multidimensional array.
    :param shape: The shape of the array to be sliced into chunks.
    :param chunks: The required chunk size.
    :return: An array of ranges that specify the chunks within the provided shape.
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


def chunk_size(chunk, shape):
    """
    Calculates a chunk size for an multidimensional array.
    :param chunk: The requested chunk size.
    :param shape: The shape of the multidimensional array.
    :return: The calculated chunk size.
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


def convert(input_config):
    """
    Converts a configuration value into a Python value.
    :param input_config: The input type configuration.
    :return: A Python value of the configured type.
    """
    raw_value = eval(input_config.text) if "eval" in input_config.attrib \
                                           and input_config.attrib["eval"].lower() == "true" else input_config.text
    if raw_value is not None:
        raw_value = raw_value.strip()
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
            value = [int(x) for x in raw_value.split(" ")] if raw_value else []
        elif input_config.attrib["type"] == "list[float]":
            value = [float(x) for x in raw_value.split(" ")] if raw_value else []
        elif input_config.attrib["type"] == "list[str]":
            value = [x for x in raw_value.split("|")] if raw_value else []
        elif input_config.attrib["type"] == "datetime":
            value = datetime.datetime.strptime(raw_value, "%Y-%m-%d %H:%M")
        else:
            raise ValueError("Unsupported type of input '" + input_config.tag + "': " + input_config.attrib["type"])
    else:
        value = raw_value
    return value


def observers_from_xml(observers_xml, **keywords):
    """
    Instantiates Landscape Model observers according to an XML configuration.
    :param observers_xml: The observer configuration XML.
    :param keywords: Additional passed to the observer constructors.
    :return: A list of observer instances.
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


def replace_tokens(tokens, source, destination):
    """
    Replaces tokens in a text file and writes the resulting text to another file.
    :param tokens: The recognized tokens and their values.
    :param source: The source file.
    :param destination: The destination file.
    :return: Nothing.
    """
    parsed_source = source
    for key, value in tokens.items():
        parsed_source = parsed_source.replace("$(" + key + ")", str(value or ""))
    with open(parsed_source) as file:
        configuration = file.read()
        for key, value in tokens.items():
            configuration = configuration.replace("$$(" + key + ")", str(value or ""))
        for key, value in tokens.items():
            configuration = configuration.replace("$(" + key + ")", str(value or ""))
        with open(destination, "w") as f:
            f.write(configuration)
    return


def run_process(command, working_directory, observer, env=None):
    """
    Runs a separate process.
    :param command: A list describing the process call.
    :param working_directory: The working directory for the process.
    :param observer: The observer used for the process.
    :param env: A dictionary of environment variables available to the new process.
    :return: Nothing.
    """
    if env is None:
        env = {}
    result = subprocess.Popen(command,
                              cwd=working_directory,
                              stdout=subprocess.PIPE,
                              stderr=subprocess.STDOUT,
                              text=True,
                              bufsize=1,
                              env=dict(env, SystemRoot=os.getenv("SystemRoot")))
    for text in iter(result.stdout.readline, ''):
        observer.write(text)
    result.stdout.close()
    result.wait()
    return


def reporting(data_store, reporting_element_class, parameters, links):
    """
    Runs a reporting element in a default reporting environment.
    :param data_store: The file path where the X3df store is located.
    :param reporting_element_class: The class of the reporting element.
    :param parameters: A list of name-value tuples defining parameters.
    :param links: A list of name-dataset tuples defining links.
    :returns: Nothing
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
    return
