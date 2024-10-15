# SciSave - Python Data Loader/Dumper for Science 

> * **Repository: [github.com/otvam/scisave](https://github.com/otvam/scisave)**
> * **Package: [pypi.org/project/scisave](https://pypi.org/project/scisave)**

## Summary

**SciSave** is a **Python serialization/deserialization** module:
* Specially targeted for **scientific applications**.
* Load **JSON/YAML configuration files**. 
* Load and write **JSON/Pickle data files**

For **YAML** files, the following **custom extensions** are used:
* `!path` - parse relative paths (with respect to the YAML file)
* `!include` - include other YAML files (recursion possible)
* `!env` - include YAML string from environment variables
* `!merge_dict` - merge a list of dicts
* `!merge_list` - merge a list of lists

For **JSON** files, the following **custom extensions** are used:
* `__complex__` - allows the serialization of complex numbers
* `__numpy__` - allows the serialization of NumPy arrays

The **JSON** files can be serialized/deserialized as/from **text and gzip** files.

The JSON/YAML files with the custom extensions are still valid JSON/YAML files.

SciSave is written in Python (NumPy is the only dependency).

## Warning

* Pickling data is not secure.
* Only load pickle files that you trust.

## Example

An example is located in the `example` folder of the repository:
* `run_data.py` contains an example file for the loader/dumper
* `config_main.yaml` YAML configuration file with custom extensions
* `config_include.yaml` YAML configuration file for include extension
* `dump.json` JSON plain text file for testing data dumping/loading
* `dump.gz` JSON plain gzip file for testing data dumping/loading
* `dump.pickle` Pickle file for testing data dumping/loading

## Project Links

* Repository: https://github.com/otvam/scisave
* Releases: https://github.com/otvam/scisave/releases
* Tags: https://github.com/otvam/scisave/tags
* Issues: https://github.com/otvam/scisave/issues
* PyPi: https://pypi.org/project/scisave

## Author

* **Thomas Guillod**
* Email: guillod@otvam.ch
* Website: https://otvam.ch

## Copyright

> (c) 2023 - Thomas Guillod
> 
>  BSD 2-Clause "Simplified" License
