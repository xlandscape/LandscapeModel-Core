"""
Class definition of the LogFileObserver.
"""

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

    def __init__(self, **keywords):
        super(LogFileObserver, self).__init__()
        os.makedirs(os.path.dirname(keywords["logfile"]), exist_ok=True)
        self._file = open(keywords["logfile"], "a", encoding="utf-8")

    def __del__(self) -> None:
        self._file.close()

    def experiment_finished(self, detail: str = "") -> None:
        """
        Reacts when an experiment is completed.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        self.write_message(4, "Experiment finished")
        self.write_message(5, detail)

    def input_get_values(self, component_input: base.Input) -> None:
        """
        Reacts when values are requested from a component input.
        :param component_input: The input being requested.
        :return: Nothing.
        """
        for message in component_input.messages:
            self.write_message(message[0], f"{component_input.name}:{message[1]}:GetValues", message[2])

    def mc_run_finished(self, detail: str = "") -> None:
        """
        Reacts when a Monte Carlo run is finished.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        self.write_message(4, "MC run finished")
        self.write_message(5, detail)

    def store_set_values(self, level: int, store_name: str, message: str) -> None:
        """
        Reacts when values are stored.
        :param level: The severity of the message.
        :param store_name: The storage name.
        :param message: The message to report.
        :return: Nothing.
        """
        self.write_message(level, f"{store_name}:SetValues", message)

    def write_message(self, level: int, message: str, detail: str = "") -> None:
        """
        Sends a message to the reporter.
        :param level: The severity of the message.
        :param message: The message to report.
        :param detail: Additional details to report.
        :return: Nothing.
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
        :param composition: The composition of the Monte Carlo run.
        :return: Nothing.
        """
        self.write_message(5, "MC run start")

    def flush(self) -> None:
        """
        Flushes the buffer of the reporter.
        :return: Nothing.
        """
        self._file.flush()

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.
        :param text: The text to write.
        :return: Nothing.
        """
        self._file.write(text)
