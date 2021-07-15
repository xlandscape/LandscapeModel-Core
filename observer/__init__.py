"""
Imports of the observer module.
"""
from .ConsoleObserver import *
from .GraphMLObserver import *
from .LogFileObserver import *

# CHANGELOG
base.VERSION.added("1.1.1", "`observer` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `observer` namespace")
base.VERSION.added("1.4.1", "Changelog in `observer.__init__` ")
base.VERSION.changed("1.4.1", "`Removed observer.VERSION` ")
