"""
Imports of the attrib module.
"""
from .Class import *
from .Equals import *
from .InList import *
from .Ontology import *
from .Scales import *
from .Transformable import *
from .Unit import *

import base

# CHANGELOG
base.VERSION.added("1.1.1", "`attrib` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `attrib` namespace")
base.VERSION.added("1.4.1", "Changelog in `attrib`")
base.VERSION.changed("1.4.1", "Removed class `attrib.VERSION`")
base.VERSION.changed("1.4.2", "Changelog description")
base.VERSION.changed("1.4.9", "`attrib` changelog uses markdown for code elements")
