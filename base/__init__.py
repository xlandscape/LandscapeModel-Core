"""
Imports for the base module.
"""
from .VersionInfo import *
from .VersionCollection import *
from .VERSION import *
from .Extension import *
from .Extensions import *
from .Values import *
from .CheckResult import *
from .DataAttribute import *
from .DataAttributes import *
from .Store import *
from .Output import *
from .OutputContainer import *
from .DataProvider import *
from .Input import *
from .InputContainer import *
from .Module import *
from .Observer import *
from .Component import *
from .UserParameters import *
from .Experiment import *
from .functions import *
from .MCRun import *
from .Project import *
from .UncertaintyAndSensitivityAnalysis import *
import base.VERSION

MODULE: base.Module = base.Module(
    "Python",
    "3.9.7",
    "bin/python-3.9.7-amd64",
    "bin/python-3.9.7-amd64/Doc/python397.chm",
    None,
    True,
    "bin/python-3.9.7-amd64/NEWS.txt"
)

# CHANGELOG
base.VERSION.added("1.1.1", "`base` namespace")
base.VERSION.added("1.1.6", "Changelog through `VersionInfo` class in `base` namespace")
base.VERSION.changed("1.3.5", "`base.__init__` refactored")
base.VERSION.added("1.4.1", "Changelog in `base.__init__`")
base.VERSION.changed("1.4.9", "`base` updated imports to changed class names")
base.VERSION.changed("1.5.3", "`base` changelog uses markdown for code elements")
base.VERSION.changed("1.7.0", "Order of imports in `base.__init__`")
base.VERSION.added("1.7.0", "Import of new classes in `base.__init__`")
base.VERSION.added("1.15.0", "Runtime environment information of core in `base.__init__`")
base.VERSION.changed("1.15.2", "Extended module information for Python runtime environment")
