"""Class definition of the Landscape Model DataAttribute class."""
import base


class DataAttribute:
    """Checks whether values comply to a specification regarding a specific data attribute and potentially transforms
    them."""
    # CHANGELOG
    base.VERSION.added("1.7.0", "`base.DataAttribute` class")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.DataAttribute`")
    base.VERSION.changed("1.18.0", "Code refactory in `base.DataAttribute`")

    def check(self, values: base.Values) -> base.CheckResult:
        """
        Checks values regarding a specific data attribute.

        Args:
            values: The values to check.

        Returns:
            A tuple representing the result of the check.
        """
        raise NotImplementedError

    @property
    def name(self) -> str:
        """
        Gets the name of the attribute checker.

        Returns:
            A string containing the name of the attribute checker.
        """
        raise NotImplementedError
