"""Imports for the `stores` namespace."""
from .InMemoryStore import *
from .SqlLiteStore import *
from .X3dfStore import *

# CHANGELOG
base.VERSION.added("1.1.1", "`stores` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `stores` namespace")
base.VERSION.added("1.4.1", "Changelog in `stores`")
base.VERSION.changed("1.4.1", "Removed `stores.VERSION`")
base.VERSION.changed("1.4.9", "`stores` changelog uses markdown for code elements")
base.VERSION.fixed("1.5.3", "`stores` changelog")
base.VERSION.changed("1.9.0", "Switched to Google docstring style in `stores.__init__`")
