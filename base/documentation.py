"""
This file contains functions for automatically documenting parts Landscape Model code.
"""
import datetime
import inspect
import base


def write_changelog(name, version_history, file_path):
    """
    Writes an updated changelog according to the version history stored along with the code.
    :param name: The name of the documented Landscape Model part.
    :param version_history: The version history containing the individual changes per version.
    :param file_path: The path of file where the changelog is written to.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Changelog\n")
        f.write("This is the changelog for the {}. It was automatically created on {}.".format(
            name,
            datetime.date.today()))
        for version in version_history:
            f.write(
                "\n\n## [{}]{}\n\n".format(version, "" if version.date is None else " - {}".format(version.date)))
            f.write("### Added\n")
            for message in version.additions:
                f.write("- {}\n".format(message.replace("_", r"\_")))
            f.write("\n### Changed\n")
            for message in version.changes:
                f.write("- {}\n".format(message.replace("_", r"\_")))
            f.write("\n### Fixed\n")
            for message in version.fixes:
                f.write("- {}\n".format(message.replace("_", r"\_")))


def document_components(components_module, file_path):
    """
    Documents the components included in the Landscape Model core.
    :param components_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Components\n")
        f.write("This file lists all components that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in components_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Component):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return


def document_observers(observers_module, file_path):
    """
    Documents the observers included in the Landscape Model core.
    :param observers_module: The module containing the components.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Observers\n")
        f.write("This file lists all observers that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in observers_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Observer):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return


def document_stores(stores_module, file_path):
    """
    Documents the stores included in the Landscape Model core.
    :param stores_module: The module containing the stores.
    :param file_path: The path of the output documentation file.
    :return: Nothing.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# Stores\n")
        f.write("This file lists all stores that are currently included in the Landscape Model core.\n")
        f.write("It was automatically created on {}.\n".format(datetime.date.today()))
        for name, member in stores_module.__dict__.items():
            if inspect.isclass(member) and issubclass(member, base.Store):
                f.write("\n\n## {}".format(name))
                f.write(member.__doc__)
    return
