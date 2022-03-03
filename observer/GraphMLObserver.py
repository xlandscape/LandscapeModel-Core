"""Class definition of a GraphML observer."""

import base
import xml.etree.ElementTree
import typing


class GraphMLObserver(base.Observer):
    """
    An observer that writes a Landscape Model's composition as a GraphML file.

    PARAMETERS
    output_file: The path to which the GraphML file should be written.
    include_modules: If the string "true" (case-insensitive), modules ae included into the GraphML file.
    """
    # CHANGELOG
    base.VERSION.added("1.2.12", "`observer.GraphMLObserver` ")
    base.VERSION.changed("1.2.13", "further implementation of `observer.GraphMLObserver` ")
    base.VERSION.added("1.3.24", "Added `observer.GraphMLObserver.flush()` and `observer.GraphMLObserver.write()` ")
    base.VERSION.changed("1.3.33", "`observer.GraphMLObserver` refactored")
    base.VERSION.added("1.4.1", "Changelog in `observer.GraphMLObserver` ")
    base.VERSION.changed("1.4.1", "`observer.GraphMLObserver` class documentation")
    base.VERSION.changed("1.5.3", "`observer.GraphMLObserver` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `observer.GraphMLObserver` ")
    base.VERSION.changed("1.7.0", "Removed unused methods in `observer.GraphMLObserver` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `observer.GraphMLObserver` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `observer.GraphMLObserver` ")

    def __init__(self, output_file: str, include_modules: str) -> None:
        """
        Initializes a GraphMLObserver.

        Args:
            output_file: The file path of the output GraphML file.
            include_modules: Specifies whether to include modules in the GraphML file.
        """
        super(GraphMLObserver, self).__init__()
        self._outputFile = output_file
        self._include_modules = str.lower(include_modules) == "true"

    def mc_run_started(self, composition: typing.Mapping[str, base.Component]) -> None:
        """
        Reacts when a Monte Carlo run has started.

        Args:
            composition: The composition of the Monte Carlo run.

        Returns:
             Nothing.
        """
        # noinspection SpellCheckingInspection
        graph_ml = xml.etree.ElementTree.Element(
            "graphml",
            {
                "xmlns": "https://graphml.graphdrawing.org/xmlns",
                "xmlns:xsi": "http://www.w3org/2001/XMLSchema-instance",
                "xsi:schemaLocation":
                    "https://graphml.graphdrawing.org/xmlns https://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd"
            }
        )
        graph_ml.append(xml.etree.ElementTree.Element(
            "key", {"id": "name", "for": "node", "attr.name": "name", "attr.type": "string"}))
        graph_ml.append(xml.etree.ElementTree.Element(
            "key", {"id": "type", "for": "node", "attr.name": "type", "attr.type": "string"}))
        # noinspection SpellCheckingInspection
        graph = xml.etree.ElementTree.Element("graph", {"id": "composition", "edgedefault": "directed"})
        graph_ml.append(graph)
        modules = set()
        for component in composition.values():
            component_node = self._create_node(component.name, "component")
            graph.append(component_node)
            providing_component_names = set(
                [
                    inp.provider.output.component.name
                    for inp in component.inputs
                    if inp.has_provider and inp.provider.output.component
                ]
            )
            for providing_component in providing_component_names:
                edge = xml.etree.ElementTree.Element("edge", {"source": providing_component, "target": component.name})
                graph.append(edge)
            if self._include_modules and component.module:
                module_label = f"{component.module.name} {component.module.version}"
                modules.add(module_label)
                edge = xml.etree.ElementTree.Element("edge", {"source": component.name, "target": module_label})
                graph.append(edge)
        for module_name in modules:
            graph.append(self._create_node(module_name, "module"))
        xml.etree.ElementTree.ElementTree(graph_ml).write(self._outputFile, encoding="utf-8", xml_declaration=True)

    @staticmethod
    def _create_node(name, entity_type):
        """
        Creates a GraphML element node.

        Args:
            name: The name of the element.
            entity_type: The type of element.

        Returns:
            The created node.
        """
        node = xml.etree.ElementTree.Element("node", {"id": name})
        name_sub_node = xml.etree.ElementTree.Element("data", {"key": "name"})
        name_sub_node.text = name
        node.append(name_sub_node)
        type_sub_node = xml.etree.ElementTree.Element("data", {"key": "type"})
        type_sub_node.text = entity_type
        node.append(type_sub_node)
        return node
