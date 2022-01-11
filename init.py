"""The Landscape Model startup script."""
import os
import sys
import typing

# CHANGELOG can be found in base\VERSION.py


def run(argument: str, basedir: typing.Optional[str] = None) -> None:
    """
    Runs the Landscape Model.

    Args:
        argument: The startup argument.
        basedir: The base directory to resolve relative paths from.

    Returns:
        Nothing.
    """
    import base
    sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "variant"))])
    ext = os.path.splitext(argument)[1]
    # noinspection SpellCheckingInspection
    if ext == ".xrun":
        parameters = base.UserParameters(argument)
        experiment = base.Experiment(
            parameters,
            os.path.join(os.path.dirname(__file__), "..", "..", "run"),
            param_dir=basedir
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
