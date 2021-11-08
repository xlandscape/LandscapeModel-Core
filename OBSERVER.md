# Observers
This file lists all observers that are currently included in the Landscape Model core.
It was automatically created on 2021-11-08.


## ConsoleObserver
    Reports to the default standard output.

    PARAMETERS
    lock: Allows to lock the console in multi-threaded runs.
    print_output: A bool tht defines that the print() method is used instead of the `write()` method of the standard
    output. Setting it to True is useful when using the observer within a Jupyter notebook.
    

## GraphMLObserver
    An observer that writes a Landscape Model's composition as a GraphML file.

    PARAMETERS
    output_file: The path to which the GraphML file should be written.
    include_modules: If the string "true" (case-insensitive), modules ae included into the GraphML file.
    

## LogFileObserver
    A Landscape Model observer that writes messages to a logfile.

    PARAMETERS
    logfile: The path and file name of the logfile to write.
    