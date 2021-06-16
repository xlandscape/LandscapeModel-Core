"""
Imports for the stores namespace.
"""
from .InMemoryStore import *
from .SqlLiteStore import *
from .X3dfStore import *

# CHANGELOG
base.VERSION.added("1.1.1", "components namespace")
base.VERSION.added("1.1.6", "Changelog through VersionInfo class in observer namespace")
base.VERSION.added("1.4.1", "Changelog in stores.__init__")
base.VERSION.changed("1.4.1", "Removed stores.VERSION")
