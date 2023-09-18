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
import json
import distutils.version
import configparser
import hashlib
import frontmatter

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
    base.VERSION.added("1.15.0", "Repository checks during initialization of `base.Experiment` ")
    base.VERSION.changed("1.15.2", "Relieved repository checks for external modules")
    base.VERSION.fixed("1.15.5", "Errors when scenario was not tested with current model")
    base.VERSION.added("1.15.6", "Message to writing of info XML in Experiment regarding un-checked scenario modules")

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
        self._replace_tokens = {}
        if parameters is not None:
            self._replace_tokens = dict(parameters.params)
            if param_dir is None:
                self._replace_tokens["_PARAM_DIR_"] = os.path.dirname(parameters.xml)
            else:
                self._replace_tokens["_PARAM_DIR_"] = param_dir
        x3dir = os.environ.setdefault("X3DIR", "")
        if x3dir != "":
            self._replace_tokens["_X3DIR_"] = x3dir
        else:
            self._replace_tokens["_X3DIR_"] = os.path.dirname(__file__)
        self._replace_tokens["_MODEL_DIR_"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        self._replace_tokens["_EXP_BASE_DIR_"] = basedir
        if project_dir is None:
            self._replace_tokens["_PROJECT_DIR_"] = self._replace_tokens["_PARAM_DIR_"]
        else:
            self._replace_tokens["_PROJECT_DIR_"] = os.path.abspath(project_dir)
        project = base.Project(self._replace_tokens["Project"], self._replace_tokens["_PROJECT_DIR_"])
        self._replace_tokens["_SCENARIO_DIR_"] = project.path
        self._replace_tokens.update(project.content)
        base.replace_tokens(self._replace_tokens, "$(_X3DIR_)/../../variant/experiment.xml", experiment_temporary_xml)
        config = xml.etree.ElementTree.parse(experiment_temporary_xml)
        self._replace_tokens["_EXP_DIR_"] = config.find("General/ExperimentDir").text
        self._replace_tokens["_MCS_BASE_DIR_"] = config.find("General/MCBaseDir").text
        os.makedirs(self._replace_tokens["_EXP_DIR_"])
        experiment_xml = os.path.join(self._replace_tokens["_EXP_DIR_"], "experiment.xml")
        shutil.move(experiment_temporary_xml, experiment_xml)
        if parameters is not None:
            shutil.copyfile(parameters.xml, os.path.join(self._replace_tokens["_EXP_DIR_"], "user.xml"))
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
                self._replace_tokens[globalParameter.tag] = globalParameter.text
        for mc in range(self._numberMC):
            mc_name = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            self._replace_tokens["_MC_NAME_"] = f"X3{mc_name}"
            self._replace_tokens["_MC_ID_"] = str(mc)
            mc_configuration = os.path.join(
                self._replace_tokens["_MCS_BASE_DIR_"], self._replace_tokens["_MC_NAME_"], "mc.xml")
            os.makedirs(os.path.dirname(mc_configuration))
            base.replace_tokens(self._replace_tokens, mc_xml, mc_configuration)
            self._mcRunConfigurations.append(mc_configuration)
        self._observer = base.MultiObserver(base.observers_from_xml(config.find("Observers")))
        sys.stdout = sys.stderr = self._observer
        self._observer.write_message(5, "Startup initialization")
        self._observer.write_message(5, f"Parameters: {parameters.xml}")
        self._observer.write_message(5, f"Project: {self._replace_tokens['Project']}")
        self._observer.write_message(5, f"Project directory: {self._replace_tokens['_PROJECT_DIR_']}")
        self._observer.write_message(5, f"Runtime directory: {self._replace_tokens['_X3DIR_']}")
        self._observer.write_message(5, f"Working directory: {self._replace_tokens['_EXP_BASE_DIR_']}")
        self.write_info_xml(os.path.join(self._replace_tokens["_EXP_DIR_"], "info.xml"), config.find("Parts"), project)

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

    def write_info_xml(self, path: str, model_parts: xml.etree.ElementTree.Element, scenario: "base.Project") -> None:
        """
        Writes version information into an XML file.

        Args:
            path: The file name of the XML file to write to.
            model_parts: The XML element describing the parts of the model.
            scenario: The scenario used for this experiment.

        Returns:
            Nothing.
        """

        def check_module(parent: str, base_path: str, module: base.Module) -> None:
            self._observer.write_message(5, f"{parent} uses {module.name} version {module.version}")
            self.check_repository_state(
                os.path.join(base_path, module.path),
                module.name,
                module.version,
                latest_versions,
                severity=3,
                external=module.external,
                changelog=module.changelog,
                documentation=module.doc_file
            )
            if module.module:
                check_module(module.name, base_path, module.module)

        info_xml = xml.etree.ElementTree.Element("info")
        xml.etree.ElementTree.SubElement(info_xml, "start_date").text = str(datetime.datetime.now().date())
        # noinspection SpellCheckingInspection
        xml.etree.ElementTree.SubElement(info_xml, "computer").text = os.environ["COMPUTERNAME"]
        versions = xml.etree.ElementTree.SubElement(info_xml, "versions")
        model_info_file = os.path.join(self._replace_tokens["_MODEL_DIR_"], "..", "model.json")
        model_info = {"name": "Model", "version": "0.0.1"}
        if os.path.exists(model_info_file):
            with open(model_info_file, encoding="utf-8") as f:
                model_info |= json.load(f)
            xml.etree.ElementTree.SubElement(
                versions, "model", {"name": model_info["name"]}).text = model_info["version"]
            self._observer.write_message(5, f"{model_info['name']} version {model_info['version']}")
        else:
            self._observer.write_message(2, "Model has no metadata file")
        latest_versions_file = os.path.join(self._replace_tokens["_MODEL_DIR_"], "..", "latest_versions.json")
        if os.path.exists(latest_versions_file):
            with open(latest_versions_file, encoding="utf-8") as f:
                latest_versions = json.load(f)
        else:
            latest_versions = {}
            self._observer.write_message(3, "Model has no latest-versions file")
        self.check_repository_state(
            os.path.join(
                self._replace_tokens["_MODEL_DIR_"], ".."), model_info["name"], model_info["version"], latest_versions)
        xml.etree.ElementTree.SubElement(versions, "core").text = str(base.VERSION.latest)
        self._observer.write_message(5, f"{model_info['name']} uses Landscape Model core version {base.VERSION.latest}")
        self.check_repository_state(
            os.path.join(self._replace_tokens["_MODEL_DIR_"], "core"),
            "Landscape Model core",
            base.VERSION.latest,
            latest_versions
        )
        check_module("Landscape Model core", os.path.join(self._replace_tokens["_MODEL_DIR_"], "core"), base.MODULE)
        parts = xml.etree.ElementTree.SubElement(versions, "parts")
        for model_part in model_parts:
            part_module = importlib.import_module(model_part.attrib["module"])
            part_class = getattr(part_module, model_part.attrib["class"])
            part_type = None
            part_xml = xml.etree.ElementTree.SubElement(parts, model_part.tag)
            part_xml.text = str(part_class.VERSION.latest)
            module = None
            if base.Observer in part_class.mro():
                part_type = "observer"
                module = part_class.MODULE
            elif base.Component in part_class.mro():
                part_type = "component"
                module = part_class(None, None, None).module
            part_xml.attrib["type"] = part_type
            self._observer.write_message(
                5, f"{model_info['name']} uses {part_type} {part_class.__name__} version {part_class.VERSION.latest}")
            self.check_repository_state(
                os.path.dirname(part_module.__file__), part_class.__name__, part_class.VERSION.latest, latest_versions)
            if module:
                check_module(part_class.__name__, os.path.dirname(part_module.__file__), module)
            else:
                self._observer.write_message(3, f"{part_class.__name__} does not specify a module")
        xml.etree.ElementTree.SubElement(versions, "scenario", {"name": scenario.name}).text = scenario.version
        self._observer.write_message(
            5, f"{model_info['name']} uses scenario {scenario.name} version {scenario.version}")
        scenario_supported_versions = scenario.supported_runtimes.get(model_info["name"]) or []
        if not scenario_supported_versions:
            self._observer.write_message(
                2,
                f"Usage of scenario {scenario.name} in {model_info['name']} is not officially "
                "supported. Please proceed with care."
            )
        elif not model_info["version"] in scenario_supported_versions:
            model_version = distutils.version.StrictVersion(model_info["version"])
            latest_supported_version = max([distutils.version.StrictVersion(x) for x in scenario_supported_versions])
            if model_version > latest_supported_version:
                self._observer.write_message(
                    3,
                    f"{scenario.name} {scenario.version} is not officially tested with {model_info['name']} "
                    f"{model_info['version']}, only with an earlier version, {latest_supported_version}",
                    "Scenario and model should be compatible, please report erroneous runtime behavior"
                )
            else:
                self._observer.write_message(
                    2,
                    f"{scenario.name} {scenario.version} is not supported by {model_info['name']} "
                    f"{model_info['version']}, only by a later version version, {latest_supported_version}",
                    "Please expect compatibility issues and try to update the scenario"
                )
        self.check_repository_state(scenario.path, scenario.name, scenario.version, latest_versions)
        xml.etree.ElementTree.indent(info_xml)
        xml.etree.ElementTree.ElementTree(info_xml).write(path, encoding="utf-8", xml_declaration=True)
        self._observer.write_message(3, "Modules of the scenario are currently not checked")

    def check_repository_state(
            self,
            path: str,
            part_name: str,
            part_version: typing.Union[str, distutils.version.StrictVersion],
            latest_versions: dict[str, str],
            git_dir: str = ".git",
            severity: int = 2,
            external: bool = False,
            changelog: typing.Optional[str] = None,
            documentation: typing.Optional[str] = None,
    ) -> None:
        git = os.path.join(path, git_dir)
        git_config_file = os.path.join(git, "config")
        git_versioned = True
        if os.path.exists(git_config_file):
            git_config = configparser.ConfigParser()
            git_config.read(git_config_file)
            if not 'remote "origin"' in git_config:
                self._observer.write_message(severity, f"{part_name} has no origin")
        elif os.path.exists(git):
            git_config = configparser.ConfigParser()
            with open(git, encoding="ascii") as f:
                git_config.read_string(f"[config]\n{f.read()}")
            self.check_repository_state(
                path,
                part_name,
                part_version,
                latest_versions,
                os.path.join(git_dir, "..", git_config["config"]["gitdir"])
            )
            return
        else:
            self._observer.write_message(severity, f"{part_name} is not git-versioned")
            git_versioned = False
        repository_info_file = os.path.join(path, "repository.json")
        repository_info = {
            "visibility": None,
            "license": None,
            "gitflow": None,
            "code_style_compliance": None,
            "issues_enabled": None,
            "default_branch": None,
            "branch_protection": None
        }
        if os.path.exists(repository_info_file):
            with open(repository_info_file, encoding="utf-8") as f:
                repository_info |= json.load(f)
        else:
            self._observer.write_message(3, f"{part_name} has no repository metadata")
        if not repository_info["visibility"] == "public":
            self._observer.write_message(
                2,
                f"{part_name} is not public, consider internal use only"
            )
        license_file = os.path.join(path, "LICENSE")
        if os.path.exists(license_file):
            with open(license_file, "rb") as f:
                license_bytes = f.read()
            license_file_is_cc0 = hashlib.md5(license_bytes).hexdigest() == "473a7959b44c2f42c375d904305b6307"
            if repository_info["license"] == "CC0-1.0" and not license_file_is_cc0:
                repository_info["license"] = None
            elif not repository_info["license"] and license_file_is_cc0:
                repository_info["license"] = "CC0-1.0"
        if repository_info["license"] not in ("CC0-1.0", "PSF-2.0", "GPL-2.0", "free"):
            self._observer.write_message(
                2,
                f"{part_name} is released under an unknown or non-free license",
                "Restrictions to usage and distribution may apply, check application for your use-case"
            )
        if not isinstance(part_version, distutils.version.StrictVersion):
            try:
                part_version = distutils.version.StrictVersion(part_version)
            except ValueError:
                part_version = distutils.version.StrictVersion("0.1")
        if (
                isinstance(part_version, distutils.version.StrictVersion) and
                part_version < distutils.version.StrictVersion("1.0")
        ):
            self._observer.write_message(
                2, f"{part_name} is a pre-release version", "Consider it experimental and report errors")
        if git_versioned and not repository_info["gitflow"]:
            self._observer.write_message(3, f"{part_name} does not follow git-flow")
        if not external and not repository_info["code_style_compliance"]:
            self._observer.write_message(3, f"Limited code-style conformance of {part_name}")
        for document in ("changelog", "readme", "contributing"):
            doc_file_path = os.path.join(path, f"{document.upper()}.md")
            if os.path.exists(doc_file_path):
                if frontmatter.check(doc_file_path):
                    changelog = frontmatter.load(
                        doc_file_path,
                        creation_method="manual",
                        software_version="0.1",
                        processor_version="0.1"
                    )
                    if "last_update" not in changelog.metadata:
                        self._observer.write_message(3, f"{document.title()} has no information on last update")
                    if changelog.metadata["creation_method"] == "manual":
                        if "author" not in changelog.metadata:
                            self._observer.write_message(3, f"{document.title()} has no author")
                    elif changelog.metadata["creation_method"] == "automatic":
                        if (
                                distutils.version.StrictVersion(changelog.metadata["processor_version"]) <
                                distutils.version.StrictVersion(repository_info[f"latest_{document}_processor"])
                        ):
                            self._observer.write_message(3, f"{document.title()} created with outdated processor")
                    else:
                        self._observer.write_message(2, f"Unknown {document} creation method")
                    if distutils.version.StrictVersion(changelog.metadata["software_version"]) != part_version:
                        self._observer.write_message(3, f"{document.title()} of {part_name} may be outdated")
                else:
                    self._observer.write_message(3, f"{document.title()} of {part_name} has no YAML header")
            elif external and {"changelog": changelog, "readme": documentation, "contributing": "OK"}[document]:
                pass
            else:
                self._observer.write_message(
                    2, f"{part_name} has no {document.replace('contributing', 'contributing note')}")
        latest_known_version = latest_versions.get(part_name, None)
        if latest_known_version:
            if part_version < distutils.version.StrictVersion(latest_known_version):
                self._observer.write_message(3, f"{part_name} is not the most recent version")
        else:
            self._observer.write_message(3, f"No latest version information on {part_name}")
        if not external and not repository_info["issues_enabled"]:
            self._observer.write_message(3, f"No issue tracking for {part_name}")
        if git_versioned and (not repository_info["default_branch"] or repository_info["default_branch"] != "main"):
            self._observer.write_message(3, f"Default branch of {part_name} is not main")
        if git_versioned and not repository_info["branch_protection"]:
            self._observer.write_message(3, f"Default branch of {part_name} is not protected")

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
