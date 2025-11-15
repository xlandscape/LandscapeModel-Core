"""A collection of version information."""
import typing

import distutils.version
import base


class VersionCollection:
    """Collects version changes to compile a changelog."""

    # CHANGELOG can be found in `VERSION.py` to avoid circular references

    def __init__(self, *versions: base.VersionInfo) -> None:
        """
        Initializes a VersionCollection.

        Args:
            *versions: The versions of the collection.
        """
        self._versions = versions
        self._roadmap = []
        self._authors = []
        self._acknowledgements = []

    def __iter__(self) -> typing.Iterator[base.VersionInfo]:
        """
        Provides an iterator over the versions of the collection.

        Returns:
            An iterator over the versions of the collection.
        """
        self._sorted_versions = sorted(self._versions, reverse=True)
        self._idx = 0
        return self

    def __next__(self) -> base.VersionInfo:
        """
        The next version within the collection.

        Returns:
            The next version within the collection.
        """
        if self._idx < len(self._sorted_versions):
            version = self._sorted_versions[self._idx]
            self._idx += 1
            return version
        else:
            raise StopIteration

    def added(self, version: str, message: str) -> None:
        """
        Adds a message to the additions of a version.

        Args:
            version: The version to which an element was added.
            message: A message describing the addition.

        Returns:
            Nothing.
        """
        parsed_version = distutils.version.StrictVersion(version)
        result = [x for x in self._versions if x == parsed_version]
        if len(result) != 1:
            raise IndexError(f"Version number not found: {version}")
        result[0].added(message)

    def changed(self, version: str, message: str) -> None:
        """
        Adds a message to the changes of a version.

        Args:
            version: The version in which an element was changed.
            message: A message describing the change.

        Returns:
            Nothing.
        """
        parsed_version = distutils.version.StrictVersion(version)
        result = [x for x in self._versions if x == parsed_version]
        if len(result) != 1:
            raise IndexError(f"Version number not found: {version}")
        result[0].changed(message)

    def fixed(self, version: str, message: str) -> None:
        """
        Adds a message to the fixes of a version.

        Args:
            version: The version in which an element was fixed.
            message: A message describing the fix.

        Returns:
            Nothing.
        """
        parsed_version = distutils.version.StrictVersion(version)
        result = [x for x in self._versions if x == parsed_version]
        if len(result) != 1:
            raise IndexError(f"Version number not found: {version}")
        result[0].fixed(message)

    @property
    def latest(self) -> base.VersionInfo:
        """
        The latest version in the collection.

        Returns:
            The highest version number found in the collection.
        """
        return max(self._versions)

    @property
    def roadmap(self) -> list[str]:
        """
        Planned changes to current version.

        Returns:
            A list of changes planned for future versions.
        """
        return self._roadmap

    @property
    def authors(self) -> list[str]:
        """
        The authors that contributed to the project.

        Returns:
            A list of contributing authors.
        """
        return self._authors

    @property
    def acknowledgements(self) -> list[str]:
        """
        Persons or project of special mention.

        Returns:
            A list of acknowledged persons and projects.
        """
        return self._acknowledgements
