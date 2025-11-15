"""Class definition of a Landscape Model console observer."""
import multiprocessing

import colorama
import sys
import base
import typing


class ConsoleObserver(base.Observer):
    """
    Reports to the default standard output.

    PARAMETERS
    lock: Allows to lock the console in parallel runs.
    print_output: A bool tht defines that the print() method is used instead of the `write()` method of the standard
    output. Setting it to True is useful when using the observer within a Jupyter notebook.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`observer.ConsoleObserver`")
    base.VERSION.added("1.2.12", "`observer.ConsoleObserver.mc_run_started()`")
    base.VERSION.added("1.3.24", "Added `observer.ConsoleObserver.flush()` and `observer.ConsoleObserver.write()`")
    base.VERSION.changed("1.3.24", "`observer.ConsoleObserver` refactored")
    base.VERSION.added("1.4.1", "Changelog in `observer.ConsoleObserver`")
    base.VERSION.changed("1.4.1", "`observer.ConsoleObserver` class documentation")
    base.VERSION.changed("1.5.3", "`observer.ConsoleObserver` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `observer.ConsoleObserver`")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `observer.ConsoleObserver`")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `observer.ConsoleObserver`")
    base.VERSION.added("1.9.5", "`observer.ConsoleObserver` parameter for less verbose output")
    base.VERSION.changed("1.9.6", "updated docstring of `ConsoleObserver.__init__`")
    base.VERSION.changed("1.9.11", "`observer.ConsoleObserver` flushes buffer after every write")
    base.VERSION.changed("1.10.3", "Spell checking in `observer.ConsoleObserver`")

    def __init__(
            self,
            lock: typing.Optional[multiprocessing.Lock] = None,
            print_output: bool = False,
            show_messages_get_values_ok: typing.Union[bool, str] = True
    ) -> None:
        """
        Initializes a ConsoleObserver.

        Args:
            lock: Allows to lock the console in parallel runs.
            print_output: A bool tht defines that the print() method is used instead of the `write()` method of the
                standard output. Setting it to True is useful when using the observer within a Jupyter notebook.
            show_messages_get_values_ok: Specifies whether messages regarding the retrieval of values are shown if they
                have a severity of 3 or 4.
        """
        super(ConsoleObserver, self).__init__()
        colorama.init()
        self._lock = lock
        self._print_output = print_output
        self._show_messages_get_values_ok = str(show_messages_get_values_ok).lower() == "true"

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
        if not self._print_output:
            sys.__stdout__.flush()

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.

        Args:
            text: The text to write.

        Returns:
             Nothing.
        """
        if self._print_output:
            print(text)
        else:
            sys.__stdout__.write(text)
            self.flush()
