"""
The Landscape Model startup script.
"""
import os
import sys

# CHANGELOG can be found in base\VERSION.py


def run(argument, basedir=None):
    """
    Runs the Landscape Model.
    :param argument: The startup argument.
    :param basedir: The base directory to resolve relative paths from.
    :return: Nothing.
    """
    import base
    sys.path.extend([os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "variant"))])
    ext = os.path.splitext(argument)[1]
    if ext == ".xrun":
        parameters = base.UserParameters(argument)
        experiment = base.Experiment(
            parameters,
            os.path.join(os.path.dirname(__file__), "..", "..", "run"),
            param_dir=basedir
        )
        experiment.run()
    elif ext == ".xuasa":
        parameters = base.UserParameters(argument)
        configuration = base.Uasa(parameters)
        configuration.create()
    elif os.path.isdir(argument):
        if basedir is None:
            basedir = os.path.dirname(argument)
        for elem in os.listdir(argument):
            run(os.path.join(argument, elem), basedir)
    else:
        print("ERROR: Unknown file extension of " + argument)
    return


def start_notebook():
    """
    Starts a Jupyter notebook for the current Landscape Model variant.
    :return: Nothing.
    """
    import notebook.notebookapp
    os.environ["JUPYTER_PATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "variant", "jupyter"))
    os.environ["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__)))
    app = notebook.notebookapp.NotebookApp()
    app.initialize([
        r'--notebook-dir={}'.format(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "analysis")))
    ])
    app.start()
    return


if __name__ == "__main__":
    for arg in sys.argv[1:]:
        if arg == "notebook":
            start_notebook()
        else:
            run(arg)
