"""
An individual experiment prepared for the Landscape Model.
"""
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

global globalLock


class Experiment:
    """
    An individual experiment prepared for the Landscape Model.
    """
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

    def __init__(self, parameters=None, work_dir="run", param_dir=None, project_dir=None):
        basedir = os.path.abspath(work_dir)
        experiment_temporary_xml = os.path.join(basedir, ''.join(
            random.choice(string.ascii_uppercase + string.digits) for _ in range(16)) + ".xml")
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
        mc_xml = config.find("General/MCRunTemplate").text
        mc_config = xml.etree.ElementTree.parse(mc_xml)
        global_parameters = mc_config.find("Global")
        if global_parameters is not None:
            for globalParameter in global_parameters:
                replace_tokens[globalParameter.tag] = globalParameter.text
        for mc in range(self._numberMC):
            replace_tokens["_MC_NAME_"] = "X3" + ''.join(
                random.choice(string.ascii_uppercase + string.digits) for _ in range(16))
            replace_tokens["_MC_ID_"] = str(mc)
            mc_configuration = os.path.join(replace_tokens["_MCS_BASE_DIR_"], replace_tokens["_MC_NAME_"], "mc.xml")
            os.makedirs(os.path.dirname(mc_configuration))
            base.replace_tokens(replace_tokens, mc_xml, mc_configuration)
            self._mcRunConfigurations.append(mc_configuration)
        self._observer = base.MultiObserver(base.observers_from_xml(config.find("Observers")))
        sys.stdout = sys.stderr = self._observer
        self._observer.write_message(5, "Startup initialization")
        self._observer.write_message(5, "Parameters: " + parameters.xml)
        self._observer.write_message(5, "Project: " + replace_tokens["Project"])
        self._observer.write_message(5, "Project directory: " + replace_tokens["_PROJECT_DIR_"])
        self._observer.write_message(5, "Runtime directory: " + replace_tokens["_X3DIR_"])
        self._observer.write_message(5, "Working directory: " + replace_tokens["_EXP_BASE_DIR_"])
        self.write_info_xml(
            os.path.join(replace_tokens["_EXP_DIR_"], "info.xml"), config.find("Parts"), project.version)
        return

    def run(self):
        """
        Runs the experiment.
        :return: Nothing.
        """
        experiment_start_time = datetime.datetime.now()
        self._observer.write_message(5, "Experiment started")
        if self.number_mc_runs > 1 and self.number_parallel_processes > 1:
            self._observer.write_message(5, "Parallel mode with " + str(
                self.number_parallel_processes) + " processes, " + str(self.number_mc_runs) + " MC(s)")
            lock = multiprocessing.Lock()
            with multiprocessing.Pool(self.number_parallel_processes, initializer=pool_init, initargs=(lock,)) as pool:
                pool.map(run_mc, self.mc_run_configurations, 1)
                pool.close()
                pool.join()
        else:
            self._observer.write_message(5, "Serial mode, " + str(self.number_mc_runs) + " MC(s)")
            for mcConfig in self.mc_run_configurations:
                base.MCRun(mcConfig).run()
        self._observer.experiment_finished("Elapsed time: " + str(datetime.datetime.now() - experiment_start_time))
        return

    @staticmethod
    def write_info_xml(path, model_parts, scenario_version):
        """
        Writes version information into an XML file.
        :param path: The file name of the XML file to write to.
        :param model_parts: The XML element describing the parts of the model.
        :param scenario_version: The version number of the scenario.
        :return: Nothing.
        """
        info_xml = xml.etree.ElementTree.Element("info")
        xml.etree.ElementTree.SubElement(info_xml, "start_date").text = str(datetime.datetime.now().date())
        xml.etree.ElementTree.SubElement(info_xml, "computer").text = os.environ["COMPUTER" + "NAME"]
        versions = xml.etree.ElementTree.SubElement(info_xml, "versions")
        xml.etree.ElementTree.SubElement(versions, "core").text = str(base.VERSION.latest)
        parts = xml.etree.ElementTree.SubElement(versions, "parts")
        for model_part in model_parts:
            part_module = importlib.import_module(model_part.attrib["module"])
            part_class = getattr(part_module, model_part.attrib["class"])
            xml.etree.ElementTree.SubElement(parts, model_part.tag).text = str(part_class.VERSION.latest)
        xml.etree.ElementTree.SubElement(versions, "scenario").text = scenario_version
        xml.etree.ElementTree.ElementTree(info_xml).write(path, encoding="utf-8", xml_declaration=True)
        return

    @property
    def mc_run_configurations(self):
        """
        The Monte Carlo run configurations prepared for this experiment.
        :return: A list of Monte Carlo run configurations.
        """
        return self._mcRunConfigurations

    @property
    def number_mc_runs(self):
        """
        The total number of Monte Carlo runs of this experiment.
        :return: The total number of Monte Carlo runs of this experiment.
        """
        return self._numberMC

    @property
    def number_parallel_processes(self):
        """
        The number of parallel processes planned for this experiment.
        :return: The number of parallel processes planned for this experiment.
        """
        return self._numberParallelProcesses


def run_mc(mc_config):
    """
    Runs an individual Monte Carlo run of the experiment.
    :param mc_config: The configuration of the Monte Carlo run.
    :return: The return value of the Monte Carlo run.
    """
    return base.MCRun(mc_config, lock=globalLock).run()


def pool_init(lock):
    """
    Initializes a pool for parallel processing.
    :param lock: The lock shared among processes.
    :return: Nothing.
    """
    global globalLock
    globalLock = lock
    return
