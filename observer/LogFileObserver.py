"""Class definition of the LogFileObserver."""

import base
import os
import typing


class LogFileObserver(base.Observer):
    """
    A Landscape Model observer that writes messages to a logfile.

    PARAMETERS
    logfile: The path and file name of the logfile to write.
    """
    # CHANGELOG
    base.VERSION.added("1.3.24", "`observer.LogFileObserver` ")
    base.VERSION.added("1.4.1", "Changelog in `observer.LogFileObserver` ")
    base.VERSION.changed("1.4.1", "`observer.LogFileObserver` class documentation")
    base.VERSION.changed("1.5.3", "`observer.LogFileObserver` changelog uses markdown for code elements")
    base.VERSION.changed("1.6.3", "`observer.LogFileObserver` uses utf-8 encoding for logfiles")
    base.VERSION.added("1.7.0", "Type hints to `observer.LogFileObserver` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `observer.LogFileObserver` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `observer.LogFileObserver` ")

    def __init__(self, logfile: str, show_messages_get_values_ok: typing.Union[bool, str] = True):
        """
        Initializes a LogFileObserver.

        Args:
            logfile: The file path of the logfile.
            show_messages_get_values_ok: Specifies whether messages regarding the retrieval of values are shown if they
                have a severity of 4.
        """
        super(LogFileObserver, self).__init__()
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        self._file = open(logfile, "a", encoding="utf-8")
        self._show_messages_get_values_ok = str(show_messages_get_values_ok).lower() == "true"

    def __del__(self) -> None:
        """
        Destroys the observer.

        Returns:
            Nothing.
        """
        self._file.close()

    def experiment_finished(self, detail: str = "") -> None:
        """
        Reacts when an experiment is completed.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        self.write_message(4, "Experiment finished")
        self.write_message(5, detail)

    def input_get_values(self, component_input: base.Input) -> None:
        """
        Reacts when values are requested from a component input.

        Args:
            component_input: The input being requested.

        Returns:
            Nothing.
        """
        for message in component_input.messages:
            if message[0] not in (3, 4) or self._show_messages_get_values_ok:
                self.write_message(message[0], f"{component_input.name}:{message[1]}:GetValues", message[2])

    def mc_run_finished(self, detail: str = "") -> None:
        """
        Reacts when a Monte Carlo run is finished.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        self.write_message(4, "MC run finished")
        self.write_message(5, detail)

    def store_set_values(self, level: int, store_name: str, message: str) -> None:
        """
        Reacts when values are stored.

        Args:
            level: The severity of the message.
            store_name: The storage name.
            message: The message to report.

        Returns:
            Nothing.
        """
        self.write_message(level, f"{store_name}:SetValues", message)

    def write_message(self, level: int, message: str, detail: str = "") -> None:
        """
        Sends a message to the reporter.

        Args:
            level: The severity of the message.
            message: The message to report.
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        if level == 1:
            severity = "ERROR"
        elif level == 2:
            severity = "WARN"
        elif level == 3:
            severity = "NOTE"
        elif level == 4:
            severity = "OK"
        elif level == 5:
            severity = "INFO"
        else:
            severity = ""
        if detail == "":
            self.write(f"{severity.ljust(6)}{message}\n")
        else:
            self.write(f"{severity.ljust(6)}{message}\n")
            self.write(f"      {detail}\n")

    def mc_run_started(self, composition: typing.Mapping[str, base.Component]) -> None:
        """
        Reacts when a Monte Carlo run has started.

        Args:
            composition: The composition of the Monte Carlo run.

        Returns:
             Nothing.
        """
        self.write_message(5, "MC run start")

    def flush(self) -> None:
        """
        Flushes the buffer of the reporter.

        Returns:
            Nothing.
        """
        self._file.flush()

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.

        Args:
            text: The text to write.

        Returns:
             Nothing.
        """
        self._file.write(text)
