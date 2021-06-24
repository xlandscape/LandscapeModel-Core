"""
Class definition of the Landscape Model Ontology checker.
"""
# import owl ready2
import base


class Ontology:
    """
    Checks for semantic relationships between values.
    """
    # CHANGELOG
    base.VERSION.added("1.2.37", "Ontology attribute checker")
    base.VERSION.changed("1.3.33", "`attrib.Ontology.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Ontology`")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Ontology` changelog uses markdown for code elements")

    # onto = owl ready2.get_ontology("file:///" + )
    # owl ready2.onto_path.append(r"F:\Temp\onto")
    # onto = owl ready2.get_ontology(r"file://F:\Temp\pizza_onto.owl")
    # onto.load()
    def __init__(self, iri):
        self._iri = iri
        return
    
    @staticmethod
    def check(values):
        """
        Checks whether values apply to an ontological definition.
        :param values: The values to check.
        :return: A CheckResult object.
        """
        # owl ready2.onto_path.append(os.path.join(os.path.dir name(os.path.dir name(
        # os.path.dir name(__file__))), "onto"))
        # onto = owl ready2.get_ontology("abc.owl")
        # onto = get_ontology("http://x3onto.org/landscape-model.owl")
        # onto.load()
        # onto = Ontology("")
        return base.CheckResult((4, "Ontology checked"), values)

    @property
    def name(self):
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        return "OntologyChecker"
