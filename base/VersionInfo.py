"""
Class definition of the Landscape Model VersionInfo class.
"""
import distutils.version
import datetime


class VersionInfo(distutils.version.StrictVersion):
    """
    A version number plus release date and changelog.
    """
    # CHANGELOG can be found in VERSION.py to avoid circular references

    def __init__(self, version, date):
        super(VersionInfo, self).__init__(version)
        self._date = datetime.datetime.strptime(date, "%Y-%m-%d").date() if date else None
        self._additions = []
        self._changes = []
        self._fixes = []
        return

    def added(self, message):
        """
        Adds an addition to this version.
        :param message: A message describing the addition.
        :return: Nothing.
        """
        self._additions.append(message)
        return

    def changed(self, message):
        """
        Adds a change to this version.
        :param message: A message describing the change.
        :return: Nothing.
        """
        self._changes.append(message)
        return

    def fixed(self, message):
        """
        Adds a fix to this version.
        :param message: A message describing the fix.
        :return: Nothing.
        """
        self._fixes.append(message)
        return

    @property
    def date(self):
        """
        The release date of the version.
        :return: A date.
        """
        return self._date

    @property
    def additions(self):
        """
        The additions of this version.
        :return: A list of messages.
        """
        return self._additions

    @property
    def changes(self):
        """
        The changes of this version.
        :return: A list of messages.
        """
        return self._changes

    @property
    def fixes(self):
        """
        The fixes of this version.
        :return: A list of messages.
        """
        return self._fixes
