"""
Class definition of an individual Monte Carlo run.
"""
import datetime
import importlib
import base
import components
import xml.etree.ElementTree


class MCRun:
    """
    A individual Monte Carlo run of a Landscape Model experiment.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.MCRun` class for managing individual Monte Carlo runs")
    base.VERSION.changed("1.1.2", "`base.MCRun` allows disabling components in configuration")
    base.VERSION.changed("1.1.2", "`base.MCRun` allows disabling links between inputs and outputs")
    base.VERSION.changed("1.2.12", "`base.MCRun.run()` signals MC run start to observer")
    base.VERSION.changed("1.3.5", "`base.MCRun` refactored")
    base.VERSION.changed("1.3.20", "`base.MCRun` can be enabled/disabled also through expression in configuration")
    base.VERSION.changed("1.3.27", "`base.MCRun` parses user-defined parameter scales")
    base.VERSION.changed("1.3.35", "`base.MCRun` can continue previous simulations")
    base.VERSION.added("1.4.1", "Changelog in `base.MCRun` ")
    base.VERSION.changed("1.4.2", "`base.McRun` changelog description")
    base.VERSION.changed("1.5.0", "`base.MCRun` iterates over output objects instead of names")
    base.VERSION.changed("1.5.1", "small changes in `base.MCRun` changelog")
    base.VERSION.changed("1.5.3", "`base.MCRun` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.MCRun` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.MCRun` ")

    def __init__(self, xml_file: str, **keywords) -> None:
        config = xml.etree.ElementTree.parse(xml_file)
        observers = base.observers_from_xml(config.find("Observers"), **keywords)
        self._observer = base.MultiObserver(observers)
        store_config = config.find("Store")
        store_module = importlib.import_module(store_config.attrib["module"])
        store_params = {}
        for storeParam in store_config:
            observer_reference = storeParam.find("ObserverReference")
            if observer_reference is not None:
                store_params[storeParam.tag.lower()] = self._observer
            else:
                store_params[storeParam.tag.lower()] = base.convert(storeParam)
        self._store = getattr(store_module, store_config.attrib["class"])(**store_params)
        self._composition = {}
        user_parameters = []
        for componentConfig in config.find("Composition"):
            if self._store.has_dataset(componentConfig.tag):
                self._observer.write_message(
                    2,
                    f"Component {componentConfig.tag} already present in data store",
                    "Configuration and parameterization ignored"
                )
            elif ("enabled" not in componentConfig.attrib or componentConfig.attrib["enabled"] == "true") and \
                    ("enabled_expression" not in componentConfig.attrib or
                     eval(componentConfig.attrib["enabled_expression"])):
                component_module = importlib.import_module(componentConfig.attrib["module"])
                try:
                    component = getattr(component_module, componentConfig.attrib["class"])(
                        componentConfig.tag, self._observer, self._store)
                except AttributeError:
                    raise AttributeError(
                        f"Module '{componentConfig.attrib['module']}' does not contain a component "
                        f"'{componentConfig.attrib['class']}'"
                    )
                for inputConfig in componentConfig:
                    from_output = inputConfig.find("FromOutput")
                    if from_output is not None:
                        if "enabled" not in from_output.attrib or from_output.attrib["enabled"] == "true":
                            if from_output.attrib["component"] in self._composition:
                                source_component = self._composition[from_output.attrib["component"]]
                                component.inputs[inputConfig.tag] = source_component.outputs[
                                    from_output.attrib["output"]
                                ]
                            elif self._store.has_dataset(from_output.attrib["component"]):
                                output_name = f"{from_output.attrib['component']}/{from_output.attrib['output']}"
                                component.inputs[inputConfig.tag] = base.Output(
                                    output_name,
                                    self._store
                                )
                                self._observer.write_message(
                                    3,
                                    f"Using stored data of {output_name} to satisfy",
                                    f"input {inputConfig.tag} of component {componentConfig.tag}"
                                )
                            else:
                                raise KeyError(f"No component '{from_output.attrib['component']}' in composition")
                    else:
                        value = base.convert(inputConfig)
                        user_parameters.append(
                            components.UserParameter(
                                f"{componentConfig.tag}/{inputConfig.tag}",
                                value,
                                inputConfig.attrib["scales"] if "scales" in inputConfig.attrib else None,
                                inputConfig.attrib["unit"] if "unit" in inputConfig.attrib else None,
                                inputConfig.attrib["element_names"] if "element_names" in inputConfig.attrib else None
                            )
                        )
                    for extensionConfig in inputConfig.findall("Extension"):
                        params = {}
                        for param in extensionConfig:
                            params[param.tag.lower()] = param.text
                        extension_module = importlib.import_module(extensionConfig.attrib["module"])
                        extension = getattr(extension_module, extensionConfig.attrib["class"])(**params)
                        component.inputs[inputConfig.tag].add_extension(extension)
                self._composition[component.name] = component
        user_parameters_component = components.UserParameters(
            "__UserParameters__", user_parameters, self._observer, self._store)
        for component_output in user_parameters_component.outputs:
            output = user_parameters_component.outputs[component_output.name]
            component_name, input_name = output.name.split("/")
            self._composition[component_name].inputs[input_name] = output

    def run(self) -> None:
        """
        Conducts the Monte Carlo run.
        :return: Nothing.
        """
        mc_start_time = datetime.datetime.now()
        self._observer.mc_run_started(self._composition)
        for component in self._composition.values():
            component_start_time = datetime.datetime.now()
            self._observer.write_message(5, f"Running component {component.name}")
            component.run()
            self._observer.write_message(5, f"Component {component.name} finished")
            self._observer.write_message(5, f"Elapsed time: {datetime.datetime.now() - component_start_time}")
        self._store.close()
        self._observer.mc_run_finished(f"Elapsed time: {datetime.datetime.now() - mc_start_time}")
