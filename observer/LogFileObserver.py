"""
Class definition of the LogFileObserver.
"""

import base
import os


class LogFileObserver(base.Observer):
    """
    A Landscape Model observer that writes messages to a logfile.

    PARAMETERS
    logfile: The path and file name of the logfile to write.
    """
    # CHANGELOG
    base.VERSION.added("1.3.24", "observer.LogFileObserver")
    base.VERSION.added("1.4.1", "Changelog in observer.LogFileObserver")
    base.VERSION.changed("1.4.1", "observer.LogFileObserver class documentation")

    def __init__(self, **keywords):
        super(LogFileObserver, self).__init__()
        os.makedirs(os.path.dirname(keywords["logfile"]), exist_ok=True)
        self._file = open(keywords["logfile"], "a")
        return

    def __del__(self):
        self._file.close()
        return

    def experiment_finished(self, detail=""):
        """
        Reacts when an experiment is completed.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        self.write_message(4, "Experiment finished")
        self.write_message(5, detail)
        return

    def input_get_values(self, component_input):
        """
        Reacts when values are requested from a component input.
        :param component_input: The input being requested.
        :return: Nothing.
        """
        for message in component_input.messages:
            self.write_message(message[0], component_input.name + ":" + message[1] + ":GetValues", message[2])
        return

    def mc_run_finished(self, detail=""):
        """
        Reacts when a Monte Carlo run is finished.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        self.write_message(4, "MC run finished")
        self.write_message(5, detail)
        return

    def store_set_values(self, level, store_name, message):
        """
        Reacts when values are stored.
        :param level: The severity of the message.
        :param store_name: The storage name.
        :param message: The message to report.
        :return: Nothing.
        """
        self.write_message(level, store_name + ":SetValues", message)
        return

    def write_message(self, level, message, detail=""):
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
            self.write("{:6s}{}\n".format(severity, message))
        else:
            self.write("{:6s}{}\n".format(severity, message))
            self.write(" " * 6 + detail + "\n")
        return

    def mc_run_started(self, composition):
        """
        Reacts when a Monte Carlo run has started.
        :param composition: The composition of the Monte Carlo run.
        :return: Nothing.
        """
        self.write_message(5, "MC run start")
        return

    def flush(self):
        """
        Flushes the buffer of the reporter.
        :return: Nothing.
        """
        self._file.flush()
        return

    def write(self, text):
        """
        Requests the reporter to write text.
        :param text: The text to write.
        :return: Nothing.
        """
        self._file.write(text)
        return
