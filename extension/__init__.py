"""
Imports of the extension namespace.
"""
from .CoordinateTransform import *

import base.VERSION

# CHANGELOG
base.VERSION.added("1.1.1", "`components` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `extension` namespace")
base.VERSION.added("1.4.1", "Changelog in `extension.__init__` ")
base.VERSION.changed("1.4.1", "Removed `extension.VERSION` ")
base.VERSION.changed("1.5.3", "`extension` changelog uses markdown for code elements")
base.VERSION.changed("1.9.0", "Renamed `extend` namespace to `extension` ")
