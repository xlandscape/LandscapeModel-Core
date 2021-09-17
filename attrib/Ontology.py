"""
Class definition of the Landscape Model Ontology checker.
"""
import base


class Ontology(base.DataAttribute):
    """
    Checks for semantic relationships between values.
    """
    # CHANGELOG
    base.VERSION.added("1.2.37", "Ontology attribute checker")
    base.VERSION.changed("1.3.33", "`attrib.Ontology.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Ontology`")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Ontology` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Ontology` got new base class `base.DataAttribute` ")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Ontology` ")
    base.VERSION.changed("1.7.0", "Removed deactivated code in `attrib.Ontology` ")

    def __init__(self, iri: str) -> None:
        self._iri = iri

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks whether values apply to an ontological definition.
        :param values: The values to check.
        :return: A CheckResult object.
        """
        return base.CheckResult((4, "Ontology checked"), values)

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.
        :return: A string containing the name of the attribute checker.
        """
        return "OntologyChecker"
