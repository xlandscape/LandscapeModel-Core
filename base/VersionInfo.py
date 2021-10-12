"""Class definition of the Landscape Model VersionInfo class."""
import distutils.version
import datetime
import typing


class VersionInfo(distutils.version.StrictVersion):
    """A version number plus release date and changelog."""
    # CHANGELOG can be found in `VERSION.py` to avoid circular references

    def __init__(self, version: str, date: typing.Optional[str]) -> None:
        """
        Initializes a VersionInfo.

        Args:
            version: The version number.
            date: The release date of the version.
        """
        super(VersionInfo, self).__init__(version)
        self._date = datetime.datetime.strptime(date, "%Y-%m-%d").date() if date else None
        self._additions = []
        self._changes = []
        self._fixes = []

    def added(self, message: str) -> None:
        """
        Adds an addition to this version.

        Args:
            message: A message describing the addition.

        Returns:
            Nothing.
        """
        self._additions.append(message)

    def changed(self, message: str) -> None:
        """
        Adds a change to this version.

        Args:
            message: A message describing the change.

        Returns:
            Nothing.
        """
        self._changes.append(message)

    def fixed(self, message: str) -> None:
        """
        Adds a fix to this version.

        Args:
            message: A message describing the fix.

        Returns:
            Nothing.
        """
        self._fixes.append(message)

    @property
    def date(self) -> typing.Optional[datetime.date]:
        """
        The release date of the version.

        Returns:
            A date.
        """
        return self._date

    @property
    def additions(self) -> list[str]:
        """
        The additions of this version.

        Returns:
            A list of messages.
        """
        return self._additions

    @property
    def changes(self) -> list[str]:
        """
        The changes of this version.

        Returns:
            A list of messages.
        """
        return self._changes

    @property
    def fixes(self) -> list[str]:
        """
        The fixes of this version.

        Returns:
            A list of messages.
        """
        return self._fixes
