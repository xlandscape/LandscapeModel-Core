"""
Script for documenting the code of the Landscape Model core.
"""
import os
import base.documentation
import components
import observer
import stores

# CHANGELOG can be found in base\VERSION.py


root_folder = os.path.abspath(os.path.join(os.path.dirname(base.__file__), ".."))
base.documentation.write_changelog("Landscape Model core", base.VERSION, os.path.join(root_folder, "CHANGELOG.md"))
base.documentation.document_components(components, os.path.join(root_folder, "COMPONENTS.md"))
base.documentation.document_observers(observer, os.path.join(root_folder, "OBSERVER.md"))
base.documentation.document_stores(stores, os.path.join(root_folder, "STORES.md"))
base.documentation.write_contribution_notes(os.path.join(root_folder, "CONTRIBUTING.md"))
base.documentation.write_repository_info(
    os.path.join(root_folder), os.path.join(root_folder, "repository.json"), r"A:\Xplicit\dev\versions.json", "core")
