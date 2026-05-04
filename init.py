"""The Landscape Model startup script."""
import datetime
import os
import re
import sys
import typing
import xml.etree.ElementTree as ET

import yaml


# CHANGELOG can be found in base\VERSION.py


def _yaml_to_xrun(yaml_path: str) -> str:
    """
    Converts a YAML parameterisation file to a temporary .xrun XML file.

    Args:
        yaml_path: Path to the .yaml file.

    Returns:
        Path to the generated temporary .xrun file (placed next to the YAML source).
    """
    with open(yaml_path, "r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    root = ET.Element("Parameters", xmlns="urn:xAquaticRisk")
    for section_name, section_params in data.items():
        section_el = ET.SubElement(root, str(section_name))
        if isinstance(section_params, dict):
            for param_name, param_value in section_params.items():
                param_el = ET.SubElement(section_el, str(param_name))
                if param_value is None:
                    param_el.text = ""
                elif isinstance(param_value, bool):
                    param_el.text = "true" if param_value else "false"
                else:
                    param_el.text = str(param_value)
        elif section_params is not None:
            section_el.text = str(section_params)
    ET.indent(root, space="  ")
    tree = ET.ElementTree(root)
    xrun_path = os.path.splitext(yaml_path)[0] + ".tmp.xrun"
    tree.write(xrun_path, encoding="utf-8", xml_declaration=True)
    return xrun_path


def _print_windows_policy_block_guidance(error: OSError) -> bool:
    """
    Prints actionable guidance for WinError 4551 (blocked runtime binary on Windows).

    Args:
        error: The OSError raised during import.

    Returns:
        True when a known policy-blocking case was handled, False otherwise.
    """
    if os.name != "nt":
        return False
    if getattr(error, "winerror", None) != 4551:
        return False
    runtime_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "bin", "python-3.9.7-amd64"))
    print("ERROR: Windows blocked loading a bundled runtime binary (WinError 4551).")
    print("This is usually caused by Windows policy or downloaded-file blocking metadata.")
    print("")
    print("Try in PowerShell:")
    print(f"  Get-ChildItem -Path '{runtime_root}' -Recurse -File | Unblock-File")
    print("")
    print("Then retry the run.")
    print("If it still fails, re-extract xAquaticRisk to a trusted local folder")
    print("or ask your administrator to allow this path/runtime under application control policy.")
    return True


def run(argument: str, basedir: typing.Optional[str] = None) -> None:
    """
    Runs the Landscape Model.

    Args:
        argument: The startup argument.
        basedir: The base directory to resolve relative paths from.

    Returns:
        Nothing.
    """
    try:
        import base
    except OSError as error:
        if _print_windows_policy_block_guidance(error):
            raise SystemExit(1) from error
        raise
    sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "variant"))])
    ext = os.path.splitext(argument)[1].lower()
    # noinspection SpellCheckingInspection
    if ext in (".yaml", ".yml"):
        argument = _yaml_to_xrun(argument)
        ext = ".xrun"
    # noinspection SpellCheckingInspection
    if ext in (".xrun", ".yaml", ".yml"):
        parameters = base.UserParameters(argument)
        experiment_id = str(parameters.params.get("ExperimentID", "Simulation")).strip()
        if not re.search(r"_\d{8}-\d{6}$", experiment_id):
            timestamp = datetime.datetime.now().strftime("%d%m%Y-%H%M%S")
            experiment_id = f"{experiment_id}_{timestamp}"
        parameters.params["ExperimentID"] = experiment_id
        experiment = base.Experiment(
            parameters,
            os.path.join(os.path.dirname(__file__), "..", "..", "run"),
            param_dir=basedir,
            project_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        )
        experiment.run()
    # noinspection SpellCheckingInspection
    elif ext == ".xuasa":
        parameters = base.UserParameters(argument)
        configuration = base.UncertaintyAndSensitivityAnalysis(parameters)
        configuration.create()
    elif os.path.isdir(argument):
        if basedir is None:
            basedir = os.path.dirname(argument)
        for elem in os.listdir(argument):
            run(os.path.join(argument, elem), basedir)
    else:
        print(f"ERROR: Unknown file extension of {argument}")


def start_notebook() -> None:
    """
    Starts a Jupyter notebook for the current Landscape Model variant.

    Returns:
        Nothing.
    """
    import notebook.notebookapp
    import winreg
    analysis_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'analysis'))
    with winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice"
    ) as rk:
        browser_choice = winreg.QueryValueEx(rk, 'ProgId')[0]
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, rf"{browser_choice}\shell\open\command") as rk:
        browser_path = winreg.QueryValueEx(rk, "")[0].split(".exe")[0].strip('"') + ".exe"
    local_app_data = os.environ["LOCALAPPDATA"]
    os.environ.clear()
    os.environ["USERPROFILE"] = analysis_folder
    os.environ["LOCALAPPDATA"] = local_app_data
    os.environ["JUPYTER_PATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "variant", "jupyter"))
    # noinspection SpellCheckingInspection
    os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    app = notebook.notebookapp.NotebookApp()
    app.initialize([f"--notebook-dir={analysis_folder}", "--ip=127.0.0.1", f'--browser="{browser_path}" %s'])
    app.start()


if __name__ == "__main__":
    """The main entry point for the Landscape Model."""
    for arg in sys.argv[1:]:
        if arg == "notebook":
            start_notebook()
        else:
            run(arg)
