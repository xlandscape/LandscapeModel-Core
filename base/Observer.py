"""
Class definitions of a Landscape Model observer and the MultiObserver.
"""
import base


class Observer:
    """
    Base class for Landscape Model observers.
    """
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Observer` class for representing Landscape Model observers")
    base.VERSION.added("1.2.12", "`base.Observer.mc_run_started()` for messages about newly started Monte Carlo runs")
    base.VERSION.changed("1.3.5", "`base.Observer` refactored")
    base.VERSION.added(
        "1.3.24", "Added `base.Observer.flush()` and `base.Observer.write()` to use observers as streams")
    base.VERSION.added("1.4.1", "Changelog in `base.Observer` ")

    def __init__(self):
        self._default_observer = None
        return

    def experiment_finished(self, detail=""):
        """
        Reacts when an experiment is completed.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        raise NotImplementedError

    def input_get_values(self, component_input):
        """
        Reacts when values are requested from a component input.
        :param component_input: The input being requested.
        :return: Nothing.
        """
        raise NotImplementedError

    def mc_run_finished(self, detail=""):
        """
        Reacts when a Monte Carlo run is finished.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        raise NotImplementedError

    def store_set_values(self, level, store_name, message):
        """
        Reacts when values are stored.
        :param level: The severity of the message.
        :param store_name: The storage name.
        :param message: The message to report.
        :return: Nothing.
        """
        raise NotImplementedError

    def write_message(self, level, message, detail=""):
        """
        Sends a message to the reporter.
        :param level: The severity of the message.
        :param message: The message to report.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        raise NotImplementedError

    def mc_run_started(self, composition):
        """
        Reacts when a Monte Carlo run has started.
        :param composition: The composition of the Monte Carlo run.
        :return: Nothing.
        """
        raise NotImplementedError

    def flush(self):
        """
        Flushes the buffer of the reporter.
        :return: Nothing.
        """
        raise NotImplementedError

    def write(self, text):
        """
        Requests the reporter to write text.
        :param text: The text to write.
        :return: Nothing.
        """
        raise NotImplementedError

    @property
    def default_observer(self):
        """
        Gets the default observer of the observer.
        :return: A Landscape Model observer.
        """
        return self._default_observer

    @default_observer.setter
    def default_observer(self, observer):
        """
        Sets the default observer of the observer.
        :param observer: The new default observer.
        """
        self._default_observer = observer


class MultiObserver(Observer):
    """
    A Landscape Model observer that encapsulates multiple observers.
    """
    def __init__(self, observers):
        super(MultiObserver, self).__init__()
        self._observers = observers
        for observer in self.observers:
            observer.default_observer = self
        return

    def experiment_finished(self, detail=""):
        """
        Reacts when an experiment is completed.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.experiment_finished(detail)
        return

    def input_get_values(self, component_input):
        """
        Reacts when values are requested from a component input.
        :param component_input: The input being requested.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.input_get_values(component_input)
        return

    def mc_run_finished(self, detail=""):
        """
        Reacts when a Monte Carlo run is finished.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.mc_run_finished(detail)
        return

    def store_set_values(self, level, store_name, message):
        """
        Reacts when values are stored.
        :param level: The severity of the message.
        :param store_name: The storage name.
        :param message: The message to report.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.store_set_values(level, store_name, message)
        return

    def write_message(self, level, message, detail=""):
        """
        Sends a message to the reporter.
        :param level: The severity of the message.
        :param message: The message to report.
        :param detail: Additional details to report.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.write_message(level, message, detail)
        return

    def mc_run_started(self, composition):
        """
        Reacts when a Monte Carlo run has started.
        :param composition: The composition of the Monte Carlo run.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.mc_run_started(composition)
        return

    def flush(self):
        """
        Flushes the buffer of the reporter.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.flush()
        return

    def write(self, text):
        """
        Requests the reporter to write text.
        :param text: The text to write.
        :return: Nothing.
        """
        for observer in self._observers:
            observer.write(text)
        return

    @property
    def observers(self):
        """
        The observers encapsulated by the MultiObserver.
        :return: A list of Landscape Model observers.
        """
        return self._observers
