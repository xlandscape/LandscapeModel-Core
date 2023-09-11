"""Class definitions of a Landscape Model observer and the MultiObserver."""
import base
import typing
import re


class Observer:
    """Base class for Landscape Model observers."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Observer` class for representing Landscape Model observers")
    base.VERSION.added("1.2.12", "`base.Observer.mc_run_started()` for messages about newly started Monte Carlo runs")
    base.VERSION.changed("1.3.5", "`base.Observer` refactored")
    base.VERSION.added(
        "1.3.24", "Added `base.Observer.flush()` and `base.Observer.write()` to use observers as streams")
    base.VERSION.added("1.4.1", "Changelog in `base.Observer` ")
    base.VERSION.changed("1.5.3", "`base.Observer` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Observer` ")
    base.VERSION.changed("1.7.0", "None-return instead of NotImplementedError in `base.Observer` methods")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.Observer` ")
    base.VERSION.added(
        "1.15.0",
        "`base.MultiObserver` remembers whether errors, warnings and notes were written during simulation run"
    )

    def __init__(self) -> None:
        """Initializes an Observer."""
        self._default_observer = None

    def experiment_finished(self, detail: str = "") -> None:
        """
        Reacts when an experiment is completed.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        return

    def input_get_values(self, component_input: base.Input) -> None:
        """
        Reacts when values are requested from a component input.

        Args:
            component_input: The input being requested.

        Returns:
            Nothing.
        """
        return

    def mc_run_finished(self, detail: str = "") -> None:
        """
        Reacts when a Monte Carlo run is finished.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        return

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
        return

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
        return

    def mc_run_started(self, composition: typing.Mapping[str, "base.Component"]) -> None:
        """
        Reacts when a Monte Carlo run has started.

        Args:
            composition: The composition of the Monte Carlo run.

        Returns:
             Nothing.
        """
        return

    def flush(self) -> None:
        """
        Flushes the buffer of the reporter.

        Returns:
            Nothing.
        """
        return

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.

        Args:
            text: The text to write.

        Returns:
             Nothing.
        """
        return

    @property
    def default_observer(self) -> typing.Optional["base.Observer"]:
        """
        Gets the default observer of the observer.

        Returns:
            A Landscape Model observer.
        """
        return self._default_observer

    @default_observer.setter
    def default_observer(self, observer: "base.Observer") -> None:
        """
        Sets the default observer of the observer.

        Args:
            observer: The new default observer.
        """
        self._default_observer = observer


class MultiObserver(Observer):
    """A Landscape Model observer that encapsulates multiple observers."""
    def __init__(self, observers: typing.Sequence["base.Observer"]) -> None:
        """
        Initializes a MultiObserver.

        Args:
            observers: The observers encapsulated by the MultiObserver.
        """
        super(MultiObserver, self).__init__()
        self._observers = observers
        self._error = None
        self._warning = None
        self._note = None
        for observer in self.observers:
            observer.default_observer = self

    def experiment_finished(self, detail: str = "") -> None:
        """
        Reacts when an experiment is completed.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        for observer in self._observers:
            observer.experiment_finished(detail)
            if self._error:
                observer.write_message(1, "Experiment completed with errors", "Please report to the developers:")
                observer.write_message(1, self._error[0].rstrip(), self._error[1].rstrip())
            if self._warning:
                observer.write_message(
                    2,
                    "Experiment completed with warnings",
                    "Please check results and consider reporting to the developers:"
                )
                observer.write_message(2, self._warning[0].rstrip(), self._warning[1].rstrip())
            if self._note:
                observer.write_message(3, "Experiment completed with notes", "Simulation results are not affected:")
                observer.write_message(3, self._note[0].rstrip(), self._note[1].rstrip())

    def input_get_values(self, component_input: base.Input) -> None:
        """
        Reacts when values are requested from a component input.

        Args:
            component_input: The input being requested.

        Returns:
            Nothing.
        """
        for observer in self._observers:
            observer.input_get_values(component_input)

    def mc_run_finished(self, detail: str = "") -> None:
        """
        Reacts when a Monte Carlo run is finished.

        Args:
            detail: Additional details to report.

        Returns:
             Nothing.
        """
        for observer in self._observers:
            observer.mc_run_finished(detail)
            if self._error:
                observer.write_message(1, "MC run completed with errors", "Please report to the developers:")
                observer.write_message(1, self._error[0].rstrip(), self._error[1].rstrip())

            if self._warning:
                observer.write_message(
                    2,
                    "MC run completed with warnings",
                    "Please check results and consider reporting to the developers:"
                )
                observer.write_message(2, self._warning[0].rstrip(), self._warning[1].rstrip())

            if self._note:
                observer.write_message(
                    3, "MC run completed with notes", "Simulation results are not affected:")
                observer.write_message(3, self._note[0].rstrip(), self._note[1].rstrip())

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
        for observer in self._observers:
            observer.store_set_values(level, store_name, message)

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
        if not self._error and level == 1:
            self._error = message, detail
        if not self._error and level == 2:
            self._warning = message, detail
        if not self._error and level == 3:
            self._note = message, detail
        for observer in self._observers:
            observer.write_message(level, message, detail)

    def mc_run_started(self, composition: typing.Mapping[str, "base.Component"]) -> None:
        """
        Reacts when a Monte Carlo run has started.

        Args:
            composition: The composition of the Monte Carlo run.

        Returns:
             Nothing.
        """
        for observer in self._observers:
            observer.mc_run_started(composition)

    def flush(self) -> None:
        """
        Flushes the buffer of the reporter.

        Returns:
            Nothing.
        """
        for observer in self._observers:
            observer.flush()

    def write(self, text: str) -> None:
        """
        Requests the reporter to write text.

        Args:
            text: The text to write.

        Returns:
             Nothing.
        """
        if not self._error and re.search("(?<!std. )error", text, re.IGNORECASE):
            self._error = text, ""
        if not self._error and re.search("warn", text, re.IGNORECASE):
            self._warning = text, ""
        if not self._error and re.search("note", text, re.IGNORECASE):
            self._note = text, ""
        for observer in self._observers:
            observer.write(text)

    @property
    def observers(self) -> typing.Sequence["base.Observer"]:
        """
        The observers encapsulated by the MultiObserver.

        Returns:
            A list of Landscape Model observers.
        """
        return self._observers
