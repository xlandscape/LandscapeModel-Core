"""
The changelog of the Landscape Model base module.
"""
import base.VersionInfo

# RELEASES
VERSION: base.VersionCollection = base.VersionCollection(
    base.VersionInfo("1.9.2", "2021-10-18"),
    base.VersionInfo("1.9.1", "2021-10-15"),
    base.VersionInfo("1.9.0", "2021-10-12"),
    base.VersionInfo("1.8.0", "2021-10-11"),
    base.VersionInfo("1.7.0", "2021-09-17"),
    base.VersionInfo("1.6.5", "2021-09-14"),
    base.VersionInfo("1.6.4", "2021-09-13"),
    base.VersionInfo("1.6.3", "2021-09-09"),
    base.VersionInfo("1.6.2", "2021-09-08"),
    base.VersionInfo("1.6.1", "2021-09-03"),
    base.VersionInfo("1.6.0", "2021-09-02"),
    base.VersionInfo("1.5.10", "2021-08-27"),
    base.VersionInfo("1.5.9", "2021-08-23"),
    base.VersionInfo("1.5.8", "2021-08-18"),
    base.VersionInfo("1.5.7", "2021-08-17"),
    base.VersionInfo("1.5.6", "2021-08-13"),
    base.VersionInfo("1.5.5", "2021-08-05"),
    base.VersionInfo("1.5.4", "2021-07-16"),
    base.VersionInfo("1.5.3", "2021-07-15"),
    base.VersionInfo("1.5.2", "2021-07-13"),
    base.VersionInfo("1.5.1", "2021-07-09"),
    base.VersionInfo("1.5.0", "2021-07-08"),
    base.VersionInfo("1.4.14", "2021-07-06"),
    base.VersionInfo("1.4.13", "2021-07-05"),
    base.VersionInfo("1.4.12", "2021-06-29"),
    base.VersionInfo("1.4.11", "2021-06-25"),
    base.VersionInfo("1.4.10", "2021-06-24"),
    base.VersionInfo("1.4.9", "2021-06-24"),
    base.VersionInfo("1.4.8", "2021-02-03"),
    base.VersionInfo("1.4.7", "2021-02-03"),
    base.VersionInfo("1.4.6", "2021-01-19"),
    base.VersionInfo("1.4.5", "2012-12-29"),
    base.VersionInfo("1.4.4", "2012-12-15"),
    base.VersionInfo("1.4.3", "2020-12-14"),
    base.VersionInfo("1.4.2", "2020-12-07"),
    base.VersionInfo("1.4.1", "2020-12-03"),
    base.VersionInfo("1.4.0", "2020-10-23"),
    base.VersionInfo("1.3.35", "2020-08-12"),
    base.VersionInfo("1.3.34", "2020-08-04"),
    base.VersionInfo("1.3.33", "2020-07-30"),
    base.VersionInfo("1.3.29", "2020-06-15"),
    base.VersionInfo("1.3.28", "2020-06-03"),
    base.VersionInfo("1.3.27", "2020-05-20"),
    base.VersionInfo("1.3.24", "2020-04-02"),
    base.VersionInfo("1.3.22", "2020-03-27"),
    base.VersionInfo("1.3.21", "2020-03-26"),
    base.VersionInfo("1.3.20", "2020-03-23"),
    base.VersionInfo("1.3.13", "2020-02-07"),
    base.VersionInfo("1.3.5", "2020-01-08"),
    base.VersionInfo("1.3.3", "2019-12-15"),
    base.VersionInfo("1.3.2", "2019-12-10"),
    base.VersionInfo("1.2.40", "2019-11-21"),
    base.VersionInfo("1.2.37", None),
    base.VersionInfo("1.2.36", None),
    base.VersionInfo("1.2.35", None),
    base.VersionInfo("1.2.34", None),
    base.VersionInfo("1.2.31", None),
    base.VersionInfo("1.2.28", None),
    base.VersionInfo("1.2.27", None),
    base.VersionInfo("1.2.25", None),
    base.VersionInfo("1.2.20", None),
    base.VersionInfo("1.2.19", None),
    base.VersionInfo("1.2.18", None),
    base.VersionInfo("1.2.17", None),
    base.VersionInfo("1.2.16", None),
    base.VersionInfo("1.2.14", None),
    base.VersionInfo("1.2.13", None),
    base.VersionInfo("1.2.12", None),
    base.VersionInfo("1.2.7", None),
    base.VersionInfo("1.2.6", None),
    base.VersionInfo("1.2.5", None),
    base.VersionInfo("1.2.4", None),
    base.VersionInfo("1.2.3", None),
    base.VersionInfo("1.2.2", None),
    base.VersionInfo("1.2.1", None),
    base.VersionInfo("1.1.6", None),
    base.VersionInfo("1.1.5", None),
    base.VersionInfo("1.1.2", None),
    base.VersionInfo("1.1.1", None)
)

# CHANGELOG
VERSION.added("1.1.6", "`base.VERSION` for describing code changes")
VERSION.changed("1.2.31", "init script recursive to run entire folders")
VERSION.changed("1.4.0", "`components.CascadeToxswa` repackaged as external part")
VERSION.changed("1.4.0", "`components.CmfContinuous` repackaged as external part")
VERSION.changed("1.4.0", "`components.LEffectModel` repackaged as external part")
VERSION.changed("1.4.0", "`components.LP50` repackaged as external part")
VERSION.changed("1.4.0", "`components.RunOffPrzm` repackaged as external part")
VERSION.changed("1.4.0", "`components.StepsRiverNetwork` repackaged as external part")
VERSION.changed("1.4.0", "`components.StreamCom` repackaged as external part")
VERSION.changed("1.4.0", "`components.XSprayDrift` repackaged as external part")
VERSION.changed("1.4.0", "`observer.AnalysisObserver` repackaged as external part")
VERSION.changed("1.4.0", "`observer.ReportingObserver` repackaged as external part")
VERSION.changed("1.4.1", "Changed `base.VERSION` to a `base.VersionCollection`, tracking changes in classes")
VERSION.added("1.4.1", "Changelog in `base.VERSION` ")
VERSION.added("1.4.2", "Corrections in `README` ")
VERSION.changed("1.4.9", "`base` changelog uses markdown for code elements")
VERSION.fixed("1.4.10", "automatic documentation error")
VERSION.changed("1.5.5", "renamed `LICENSE.txt` to `LICENSE` ")
VERSION.fixed("1.5.5", "spelling error in readme")
VERSION.added("1.7.0", "Type hints to `base.VERSION` ")

# CHANGELOG VersionCollection.py
VERSION.added("1.4.1", "`base.VersionCollection` for managing revision history")
VERSION.changed("1.5.0", "fixed spelling in `base.VersionCollection` ")
VERSION.added("1.5.0", "properties `roadmap`, `authors` and `acknowledgements` to `base.VersionCollection` ")
VERSION.added("1.7.0", "Type hints to `base.VersionCollection` ")
VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.VersionCollection` ")
VERSION.changed("1.9.0", "Switched to Google docstring style in `base.VersionCollection` ")

# CHANGELOG VersionInfo.py
VERSION.added("1.1.6", "`base.VersionInfo` for describing individual revisions")
VERSION.changed("1.3.27", "`base.VersionInfo` refactored")
VERSION.changed("1.4.1", "`base.VersionInfo` completely rewritten to move changelogs nearer to code")
VERSION.added("1.7.0", "Type hints to `base.VersionInfo` ")
VERSION.changed("1.9.0", "Switched to Google docstring style in `base.VersionInfo` ")

# CHANGELOG init.py
VERSION.changed("1.4.9", "`init.py` spell check exclusions")
VERSION.added("1.7.0", "Type hints to `init.py` ")
VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `init.py` ")
VERSION.changed("1.9.0", "Switched to Google docstring style in `init.py` ")

# CHANGELOG document.py
VERSION.added("1.4.9", "`document.py` ")

# CHANGELOG runtime environment
VERSION.changed("1.6.0", "updated runtime environment to Python 3.9.7")
VERSION.changed("1.6.1", "updated Python packages")
