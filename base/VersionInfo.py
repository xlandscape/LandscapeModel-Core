"""
Class definition of the Landscape Model VersionInfo class.
"""
import distutils.version
import datetime
import typing


class VersionInfo(distutils.version.StrictVersion):
    """
    A version number plus release date and changelog.
    """
    # CHANGELOG can be found in VERSION.py to avoid circular references

    def __init__(self, version: str, date: typing.Optional[str]) -> None:
        super(VersionInfo, self).__init__(version)
        self._date = datetime.datetime.strptime(date, "%Y-%m-%d").date() if date else None
        self._additions = []
        self._changes = []
        self._fixes = []

    def added(self, message: str) -> None:
        """
        Adds an addition to this version.
        :param message: A message describing the addition.
        :return: Nothing.
        """
        self._additions.append(message)

    def changed(self, message: str) -> None:
        """
        Adds a change to this version.
        :param message: A message describing the change.
        :return: Nothing.
        """
        self._changes.append(message)

    def fixed(self, message: str) -> None:
        """
        Adds a fix to this version.
        :param message: A message describing the fix.
        :return: Nothing.
        """
        self._fixes.append(message)

    @property
    def date(self) -> typing.Optional[datetime.date]:
        """
        The release date of the version.
        :return: A date.
        """
        return self._date

    @property
    def additions(self) -> list[str]:
        """
        The additions of this version.
        :return: A list of messages.
        """
        return self._additions

    @property
    def changes(self) -> list[str]:
        """
        The changes of this version.
        :return: A list of messages.
        """
        return self._changes

    @property
    def fixes(self) -> list[str]:
        """
        The fixes of this version.
        :return: A list of messages.
        """
        return self._fixes
