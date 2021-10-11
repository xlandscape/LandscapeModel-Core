"""
Class definition of a Landscape Model console observer.
"""
import multiprocessing

import colorama
import sys
import base
import typing


class ConsoleObserver(base.Observer):
    """
    Reports to the default standard output.

    PARAMETERS
    lock: Allows to lock the console in multi-threaded runs.
    print_output: A bool tht defines that the print() method is used instead of the write() method of the standard
    output. Setting it to True is useful when using the observer within a Jupyter notebook.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`observer.ConsoleObserver` ")
    base.VERSION.added("1.2.12", "`observer.ConsoleObserver.mc_run_started()` ")
    base.VERSION.added("1.3.24", "Added `observer.ConsoleObserver.flush()` and `observer.ConsoleObserver.write()` ")
    base.VERSION.changed("1.3.24", "`observer.ConsoleObserver` refactored")
    base.VERSION.added("1.4.1", "Changelog in `observer.ConsoleObserver` ")
    base.VERSION.changed("1.4.1", "`observer.ConsoleObserver` class documentation")
    base.VERSION.changed("1.5.3", "`observer.ConsoleObserver` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `observer.ConsoleObserver` ")

    def __init__(self, lock: typing.Optional[multiprocessing.Lock] = None, print_output: bool = False) -> None:
        super(ConsoleObserver, self).__init__()
        colorama.init()
        self._lock = lock
        self._print_output = print_output

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
            color = colorama.Fore.LIGHTRED_EX
        elif level == 2:
            severity = "WARN"
            color = colorama.Fore.YELLOW
        elif level == 3:
            severity = "NOTE"
            color = colorama.Fore.CYAN
        elif level == 4:
            severity = "OK"
            color = colorama.Fore.GREEN
        elif level == 5:
            severity = "INFO"
            color = colorama.Fore.WHITE
        else:
            severity = ""
            color = colorama.Fore.WHITE
        if self._lock is not None:
            self._lock.acquire()
        if detail == "":
            self.write(f"{color}{severity.ljust(6)}{message}\n{colorama.Style.RESET_ALL}")
        else:
            self.write(f"{color}{severity.ljust(6)}{message}\n")
            self.write(f"      {detail}\n{colorama.Style.RESET_ALL}")

        if self._lock is not None:
            self._lock.release()

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
        if not self._print_output:
            sys.__stdout__.flush()

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.
        :param text: The text to write.
        :return: Nothing.
        """
        if self._print_output:
            print(text)
        else:
            sys.__stdout__.write(text)
