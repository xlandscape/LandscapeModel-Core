# Stores
This file lists all stores that are currently included in the Landscape Model core.
It was automatically created on 2021-09-08.


## InMemoryStore
    A Landscape model store that manages data exchange entirely by Python objects in memory.

    PARAMETERS
    None.
    

## SqlLiteStore
    Writes simulation data into a SqlLite database.

    PARAMETERS
    file_path: The path and file name of the SqlLite database to be used.
    observer: An observer that handles the messages emitted by the store.
    

## X3dfStore
    Encapsulates an X3df data store for usage in the Landscape Model.

    PARAMETERS
    file_path: The file path and name for the HDF5 tom use.
    observer: A observer that handles the messages emitted by the store.
    mode: The file mode with which the HDF5 is opened.
    initialization: File path and name to an existing X3dfStore which contains data used for initializing the current
    store.
    