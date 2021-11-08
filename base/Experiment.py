"""An individual experiment prepared for the Landscape Model."""
import datetime
import multiprocessing
import os
import random
import shutil
import string
import sys
import base
import xml.etree.ElementTree
import importlib
import typing
import time
import psutil

global globalLock


class Experiment:
    """An individual experiment prepared for the Landscape Model."""
    # CHANGELOG
    base.VERSION.added("1.1.1", "`base.Experiment` class for managing individual experiments")
    base.VERSION.added("1.1.6", "`base.Experiment.write_info_xml()` for saving runtime information of the experiment")
    base.VERSION.changed("1.2.1", "`base.Experiment` expects a global section in the Monte Carlo run configuration")
    base.VERSION.changed("1.2.1", "`base.Experiment` has new macro `_X3DIR_` ")
    base.VERSION.changed("1.2.17", "`base.Experiment` has new macro `_PARAM_DIR_` ")
    base.VERSION.changed("1.2.17", "`base.Experiment` is more flexible in parameter directory")
    base.VERSION.changed("1.3.5", "`base.Experiment` refactored")
    base.VERSION.changed("1.3.5", "`base.Experiment` project encapsulation and support of versions")
    base.VERSION.changed("1.3.24", "`base.Experiment` sets standard and error output to default observer")
    base.VERSION.added("1.4.1", "Changelog in `base.Experiment` ")
    base.VERSION.changed("1.4.1", "`base.Experiment.write_info_xml()` uses new `Version` classes")
    base.VERSION.changed("1.4.2", "Changelog description")
    base.VERSION.changed("1.4.6", "New system macro `_MC_ID_` ")
    base.VERSION.changed("1.5.3", "`base.Experiment` changelog uses markdown for code elements")
    base.VERSION.added("1.7.0", "Type hints to `base.Experiment` ")
    base.VERSION.changed("1.8.0", "Replaced Legacy format strings by f-strings in `base.Experiment` ")
    base.VERSION.changed("1.9.0", "Switched to Google docstring style in `base.Experiment` ")
    base.VERSION.changed("1.9.1", "New macro `_MODEL_DIR_` in `base.Experiment` ")
    base.VERSION.added("1.9.9", "Option to profile performance of simulation runs in `base.Experiment` ")
    base.VERSION.fixed("1.9.11", "Processing of exceptions thrown in non-blocking mode in `base.Experiment` ")

    def __init__(
            self,
            parameters: typing.Optional[base.UserParameters] = None,
            work_dir: str = "run",
            param_dir: typing.Optional[str] = None,
            project_dir: typing.Optional[str] = None
    ) -> None:
        """
        Initializes an Experiment.

        Args:
            parameters: The user parameters defining the experiment.
            work_dir: The working directory of the experiment.
            param_dir: The parameterization directory of the experiment.
            project_dir: The project directory of the experiment.
        """
        basedir = os.path.abspath(work_dir)
        experiment_temporary_xml = os.path.join(
            basedir, f"{''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))}.xml")
        replace_tokens = {}
        if parameters is not None:
            replace_tokens = dict(parameters.params)
            if param_dir is None:
                replace_tokens["_PARAM_DIR_"] = os.path.dirname(parameters.xml)
            else:
                replace_tokens["_PARAM_DIR_"] = param_dir
        x3dir = os.environ.setdefault("X3DIR", "")
        if x3dir != "":
            replace_tokens["_X3DIR_"] = x3dir
        else:
            replace_tokens["_X3DIR_"] = os.path.dirname(__file__)
        replace_tokens["_MODEL_DIR_"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        replace_tokens["_EXP_BASE_DIR_"] = basedir
        if project_dir is None:
            replace_tokens["_PROJECT_DIR_"] = replace_tokens["_PARAM_DIR_"]
        else:
            replace_tokens["_PROJECT_DIR_"] = os.path.abspath(project_dir)
        project = base.Project(replace_tokens["Project"], replace_tokens["_PROJECT_DIR_"])
        replace_tokens["_SCENARIO_DIR_"] = project.path
        replace_tokens.update(project.content)
        base.replace_tokens(replace_tokens, "$(_X3DIR_)/../../variant/experiment.xml", experiment_temporary_xml)
        config = xml.etree.ElementTree.parse(experiment_temporary_xml)
        replace_tokens["_EXP_DIR_"] = config.find("General/ExperimentDir").text
        replace_tokens["_MCS_BASE_DIR_"] = config.find("General/MCBaseDir").text
        os.makedirs(replace_tokens["_EXP_DIR_"])
        experiment_xml = os.path.join(replace_tokens["_EXP_DIR_"], "experiment.xml")
        shutil.move(experiment_temporary_xml, experiment_xml)
        if parameters is not None:
            shutil.copyfile(parameters.xml, os.path.join(replace_tokens["_EXP_DIR_"], "user.xml"))
        self._numberMC = int(config.find("General/NumberMC").text)
        self._numberParallelProcesses = int(config.find("General/NumberParallelProcesses").text)
        self._mcRunConfigurations = []
        self._enable_profiling = config.find("General/EnableProfiling").text.lower() == "true"
        self._profiling_waiting_time = float(config.find("General/ProfilingWaitingTime").text)
        self._profiling_polling_duration = float(config.find("General/ProfilingPollingDuration").text)
        mc_xml = config.find("General/MCRunTemplate").text
        mc_config = xml.etree.ElementTree.parse(mc_xml)
        global_parameters = mc_config.find("Global")
        if global_parameters is not None:
            for globalParameter in global_parameters:
                replace_tokens[globalParameter.tag] = globalParameter.text
        for mc in range(self._numberMC):
            mc_name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            replace_tokens["_MC_NAME_"] = f"X3{mc_name}"
            replace_tokens["_MC_ID_"] = str(mc)
            mc_configuration = os.path.join(replace_tokens["_MCS_BASE_DIR_"], replace_tokens["_MC_NAME_"], "mc.xml")
            os.makedirs(os.path.dirname(mc_configuration))
            base.replace_tokens(replace_tokens, mc_xml, mc_configuration)
            self._mcRunConfigurations.append(mc_configuration)
        self._observer = base.MultiObserver(base.observers_from_xml(config.find("Observers")))
        sys.stdout = sys.stderr = self._observer
        self._observer.write_message(5, "Startup initialization")
        self._observer.write_message(5, f"Parameters: {parameters.xml}")
        self._observer.write_message(5, f"Project: {replace_tokens['Project']}")
        self._observer.write_message(5, f"Project directory: {replace_tokens['_PROJECT_DIR_']}")
        self._observer.write_message(5, f"Runtime directory: {replace_tokens['_X3DIR_']}")
        self._observer.write_message(5, f"Working directory: {replace_tokens['_EXP_BASE_DIR_']}")
        self.write_info_xml(
            os.path.join(replace_tokens["_EXP_DIR_"], "info.xml"), config.find("Parts"), project.version)

    def run(self) -> None:
        """
        Runs the experiment.

        Returns:
            Nothing.
        """
        experiment_start_time = datetime.datetime.now()
        self._observer.write_message(5, "Experiment started")
        if self.number_mc_runs > 1 and self.number_parallel_processes > 1:
            self._observer.write_message(
                5, f"Parallel mode with {self.number_parallel_processes} processes, {self.number_mc_runs} MC(s)")
            lock = multiprocessing.Lock()
            if self._enable_profiling:
                self._observer.write_message(5, f"Profiling enabled, using non-blocking parallelization")
                manager = multiprocessing.Manager().list()
                with multiprocessing.Pool(
                        self.number_parallel_processes, initializer=pool_init, initargs=(lock, manager)) as pool:
                    result = pool.map_async(run_mc, self.mc_run_configurations, 1)
                    processes_dict = {}
                    while not result.ready():
                        for pid in manager:
                            processes_dict.setdefault(pid, psutil.Process(pid))
                        for process in processes_dict.values():
                            self.profile_process(process)
                            time.sleep(self._profiling_waiting_time)
                    result.get()
            else:
                self._observer.write_message(5, f"Profiling not enabled, using blocking parallelization")
                with multiprocessing.Pool(
                        self.number_parallel_processes, initializer=pool_init, initargs=(lock,)) as pool:
                    pool.map(run_mc, self.mc_run_configurations, 1)
                    pool.close()
                    pool.join()
        else:
            self._observer.write_message(5, f"Serial mode, {self.number_mc_runs} MC(s)")
            for mcConfig in self.mc_run_configurations:
                base.MCRun(mcConfig).run()
        self._observer.experiment_finished(f"Elapsed time: {datetime.datetime.now() - experiment_start_time}")

    def profile_process(self, process: psutil.Process) -> None:
        """
        Profiles a running process and reports it to the experiment's observer.

        Args:
            process: The process to profile.

        Returns:
            Nothing.
        """
        try:
            with process.oneshot():
                process_io = process.io_counters()
                self._observer.write_message(
                    5,
                    f"profile {datetime.datetime.now()} - process {process.pid}, parent {process.ppid()}: "
                    f"{process.name()}, {round(process.cpu_percent(self._profiling_polling_duration))}% CPU (logical), "
                    f"{round(process.memory_info()[0] / 1048576)}MB memory usage, "
                    f"{round(process_io[2] / 1048576)}MB read, "
                    f"{round(process_io[3] / 1048576)}MB written"
                )
                for child in process.children():
                    self.profile_process(child)
        except psutil.NoSuchProcess:
            pass

    @staticmethod
    def write_info_xml(path: str, model_parts: xml.etree.ElementTree.Element, scenario_version: str) -> None:
        """
        Writes version information into an XML file.

        Args:
            path: The file name of the XML file to write to.
            model_parts: The XML element describing the parts of the model.
            scenario_version: The version number of the scenario.

        Returns:
            Nothing.
        """
        info_xml = xml.etree.ElementTree.Element("info")
        xml.etree.ElementTree.SubElement(info_xml, "start_date").text = str(datetime.datetime.now().date())
        # noinspection SpellCheckingInspection
        xml.etree.ElementTree.SubElement(info_xml, "computer").text = os.environ["COMPUTERNAME"]
        versions = xml.etree.ElementTree.SubElement(info_xml, "versions")
        xml.etree.ElementTree.SubElement(versions, "core").text = str(base.VERSION.latest)
        parts = xml.etree.ElementTree.SubElement(versions, "parts")
        for model_part in model_parts:
            part_module = importlib.import_module(model_part.attrib["module"])
            part_class = getattr(part_module, model_part.attrib["class"])
            xml.etree.ElementTree.SubElement(parts, model_part.tag).text = str(part_class.VERSION.latest)
        xml.etree.ElementTree.SubElement(versions, "scenario").text = scenario_version
        xml.etree.ElementTree.ElementTree(info_xml).write(path, encoding="utf-8", xml_declaration=True)

    @property
    def mc_run_configurations(self) -> list[str]:
        """
        The Monte Carlo run configurations prepared for this experiment.

        Returns:
            A list of Monte Carlo run configurations.
        """
        return self._mcRunConfigurations

    @property
    def number_mc_runs(self) -> int:
        """
        The total number of Monte Carlo runs of this experiment.

        Returns:
            The total number of Monte Carlo runs of this experiment.
        """
        return self._numberMC

    @property
    def number_parallel_processes(self) -> int:
        """
        The number of parallel processes planned for this experiment.

        Returns:
            The number of parallel processes planned for this experiment.
        """
        return self._numberParallelProcesses


def run_mc(mc_config: str) -> None:
    """
    Runs an individual Monte Carlo run.

    Args:
        mc_config: The configuration of the Monte Carlo run.

    Returns:
        The return value of the Monte Carlo run.
    """
    return base.MCRun(mc_config, lock=globalLock).run()


def pool_init(lock: multiprocessing.Lock, running_processes: typing.Optional[list[int]] = None) -> None:
    """
    Initializes a pool for parallel processing.

    Args:
        lock: The lock shared among processes.
        running_processes: A list of identifiers of currently running process conducting Monte Carlo runs of the
            experiment.

    Returns:
        Nothing.
    """
    global globalLock
    globalLock = lock
    if running_processes is not None:
        running_processes.append(multiprocessing.current_process().pid)
