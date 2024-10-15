"""Anaerobic Digestion Models in Python

The module contains submodules 'pyadm1', 'pyam2'.


---------- Rules ----------

--- I/O Rule ---

- Custom classes which are not intermediary should have a "save" method and a "load" classmethod.
The save function should output the name of the file (or folder) on which the data is
saved.

- As much as possible, the files should be human readable (e.g. use csv, json, yml files).
For objects which can not be saved in human readable format (e.g. functions), use package
dill as much as possible with extension '.dl'
"""

__version__ = "0.0.1"
