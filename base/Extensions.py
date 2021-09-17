"""
Class definition of the Landscape Model Extensions class.
"""
import base


class Extensions(dict):
    """
    A container for value extensions.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Extensions` class as a container for data extensions")
    base.VERSION.changed("1.3.33", "`base.Extensions` refactored")
    base.VERSION.added("1.4.1", "Changelog in `base.Extensions` ")
    base.VERSION.changed("1.5.3", "`base.Extensions` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Extensions` ")

    def __getattr__(self, key: str) -> base.Extension:
        return self[key]
