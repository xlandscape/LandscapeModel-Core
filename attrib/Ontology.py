"""Class definition of the Landscape Model Ontology checker."""
import base


class Ontology(base.DataAttribute):
    """Checks for semantic relationships between values."""
    # CHANGELOG
    base.VERSION.added("1.2.37", "Ontology attribute checker")
    base.VERSION.changed("1.3.33", "`attrib.Ontology.check()` returns base.CheckResult instead of tuple")
    base.VERSION.added("1.4.1", "Changelog in class `attrib.Ontology`")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.9", "`attrib.Ontology` changelog uses markdown for code elements")
    base.VERSION.changed("1.7.0", "`attrib.Ontology` got new base class `base.DataAttribute`")
    base.VERSION.added("1.7.0", "Type hints to `attrib.Ontology`")
    base.VERSION.changed("1.7.0", "Removed deactivated code in `attrib.Ontology`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `attrib.Ontology`")

    def __init__(self, iri: str) -> None:
        """
        Initializes an Ontology attribute.

        Args:
            iri: The IRI of the ontology.
        """
        self._iri = iri

    def __repr__(self) -> str:
        return f"Ontology: `{self._iri}`"

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        return base.CheckResult((4, "Ontology checked"), values)

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        return "OntologyChecker"
