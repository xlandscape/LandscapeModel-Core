"""Class definition of the Landscape Model Extension class."""
import base


class Extension:
    """Extends values by additional functionality."""
    # CHANGELOG
    base.VERSION.added("1.7.0", "`base.Extension` class")

    def register(self, values: "base.Values") -> None:
        """
        Registers the extension.

        Args:
            values: The values to register the extension for.

        Returns:
            Nothing.
        """
        raise NotImplementedError
