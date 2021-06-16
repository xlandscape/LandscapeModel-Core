"""
The changelog of the Landscape Model base module.
"""
import base.VersionInfo

# RELEASES
VERSION = base.VersionCollection(
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
VERSION.added("1.1.6", "base.VERSION for describing code changes")
VERSION.changed("1.2.31", "init script recursive to run entire folders")
VERSION.changed("1.4.0", "components.CascadeToxswa repackaged as external part")
VERSION.changed("1.4.0", "components.CmfContinuous repackaged as external part")
VERSION.changed("1.4.0", "components.LEffectModel repackaged as external part")
VERSION.changed("1.4.0", "components.LP50 repackaged as external part")
VERSION.changed("1.4.0", "components.RunOffPrzm repackaged as external part")
VERSION.changed("1.4.0", "components.StepsRivernetwork repackaged as external part")
VERSION.changed("1.4.0", "components.StreamCom repackaged as external part")
VERSION.changed("1.4.0", "components.XSprayDrift repackaged as external part")
VERSION.changed("1.4.0", "observer.AnalysisObserver repackaged as external part")
VERSION.changed("1.4.0", "observer.ReportingObserver repackaged as external part")
VERSION.changed("1.4.1", "Changed base.VERSION to a base.VersionCollection, tracking changes in classes")
VERSION.added("1.4.1", "Changelog in base.VERSION")
VERSION.added("1.4.2", "Corrections in README")

# CHANGELOG VersionCollection.py
VERSION.added("1.4.1", "base.VersionCollection for managing revision history")

# CHANGELOG VersionInfo.py
VERSION.added("1.1.6", "base.VersionInfo for describing individual revisions")
VERSION.changed("1.3.27", "base.VersionInfo refactored")
VERSION.changed("1.4.1", "base.VersionInfo completely rewritten to move changelogs nearer to code")
