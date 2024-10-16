"""
Shared functions for basic read/write to human readable format
"""

import json
import os
from typing import Any, Callable, Optional, Union

import dill as dl
import numpy as np
import pandas as pd


class WrongExtension(Exception):
    """Wrong Extension error."""

    msg = "Expected extension {}. Got filename {}"

    def __init__(self, filename, extension):
        self.filename = filename
        self.extension = extension
        super().__init__(self.msg.format(extension, filename))


def add_extension(name: str, ext: Optional[str]) -> str:
    """Add an extension at the end of a path if not present.
    Raise WrongExtension if extension is present in path and does not match expected extension

    Args:
        name: a file name or path
        ext: an extension to add to the file name or path if not present
    NOTE:
        if ext == "" or ext is None, no checks are performed and name is returned as is. The
        convention is that ext == "" implies that the path maps to a folder, and ext is None
        means that no specific extension checks should be performed (e.g. text files for which
        custom extensions could be used). The assumption is that there is a single "." character
        for file names with an extension (there may be '.' characters in folder names)
    """
    if (ext == "") or (ext is None):
        return name

    blocks = name.split(os.sep)
    last = blocks[-1]
    separated = last.split(".")
    if len(separated) > 2:
        # Case with multiple "." in file name, e.g. "file.name.json",
        # which is NOT supported
        raise WrongExtension(filename=last, extension=ext)
    if len(separated) == 1:
        blocks[-1] = f"{last}.{ext}"
        return os.path.join(*blocks)

    if separated[1] != ext:
        raise WrongExtension(filename=name, extension=ext)

    return name


def combine_to_path(name: str, ext: Optional[str], directory: Optional[str]) -> str:
    """Combine a file name, an extension and directory to a path
    Exemples:

    combine("here/my_doc.json", "json", "there/it/goes")
    AND
    combine("here/my_doc", "json", "there/it/goes")
    AND
    combine("there/it/goes/here/my_doc", "json", None)
    AND
    combine("goes/here/my_doc.json", None, "there/it")
    all return "there/it/goes/here/my_doc.json"

    combine("here/my_doc.json", "csv", "there/it/goes")
    AND
    combine("here/my.doc.json, "json", "there/it/goes")
    both raise WrongExtension

    combine("here/is/the/folder", None, None)
    AND
    combine("folder", None, "here/is/the")
    AND
    combine("the/folder", "", "here/is")
    all return "here/is/the/folder".
    """
    name = add_extension(name, ext)
    if directory is None:
        return name
    return os.path.join(directory, name)


class SaveLoad:
    """Save and Load information.
    This class is constructed around 2 main functions,
    load and save (optional). 'load' should open a file and
    return an object, which can be saved to a file through 'save'.

    Other attributes:
        ext, the extension of the saving files.
    """

    def __init__(
        self,
        load: Callable[[str], Any],
        save: Optional[Callable[[str, Any], str]] = None,
        extension: Optional[str] = None,
    ):
        self.__load = load
        self.__save = save
        self.__ext = extension

    def check_ext(self, path):
        if self.__ext is not None:
            assert path[-len(self.__ext) :] == self.__ext

    @property
    def ext(self):
        """Extension of file"""
        return self.__ext

    def save(self, path: str, obj):
        """Save object to path"""
        # Check that extension is coherent with path
        self.check_ext(path)

        if self.__save is None:
            # Assumes that obj has a save method
            return obj.save(path)
        return self.__save(path, obj)

    def load(self, path: str, optional: bool = False):
        """Load object from path
        Arsg:
            path: path to load
            optional: behavior if file does not exist
                (if optional, returns None, else raise
                FileNotFound)
        """
        if not os.path.exists(path):
            if optional:
                return None
            raise FileNotFoundError(f"Could not find {path}")
        self.check_ext(path)
        return self.__load(path)


# str IO
def write_str(path: str, x: str):
    """Write str to a txt file"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(x)


def load_str(path: str) -> str:
    """Read str from txt file"""
    with open(path, "r", encoding="utf-8") as file:
        x = file.read()
    return x


rw_str = SaveLoad(save=write_str, load=load_str, extension="txt")


# int IO
def write_int(path: str, x: int):
    """Write int to a txt file"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(x))


def load_int(path: str) -> int:
    with open(path, "r", encoding="utf-8") as file:
        x = int(file.read())
    return x


rw_int = SaveLoad(save=write_int, load=load_int, extension="txt")


def write_bool(path: str, x: bool):
    return write_int(path, int(x))


def load_bool(path: str) -> bool:
    return bool(load_int(path))


rw_bool = SaveLoad(save=write_bool, load=load_bool, extension="txt")


def write_float(path: str, x: float) -> str:
    """Write float to a txt file"""
    with open(path, "w", encoding="utf-8") as file:
        file.write(str(x))
    return path


def load_float(path: str) -> float:
    """Read float from txt file"""
    with open(path, "r", encoding="utf-8") as file:
        x = float(file.read())
    return x


rw_flt = SaveLoad(save=write_float, load=load_float, extension="txt")


class NpEncoder(json.JSONEncoder):
    """JSONEncoder with partial np.ndarray support"""

    def default(self, o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.dtype):
            return str(o)
        if isinstance(o, np.ndarray):
            return {"__ndarray__": o.tolist(), "dtype": o.dtype}
        return super().default(o)


def json_numpy_obj_hook(dct):
    """Decodes a previously encoded numpy ndarray with proper shape and dtype.

    :param dct: (dict) json encoded ndarray
    :return: (ndarray) if input was an encoded ndarray
    """
    if isinstance(dct, dict) and "__ndarray__" in dct:
        return np.array(dct["__ndarray__"], dtype=dct["dtype"])
    return dct


class PdEncoder(NpEncoder):
    """
    JSONEncoder with partial numpy.npdarray and pandas support.
    Work in progresss
    """

    def default(self, o):
        if isinstance(o, pd.Index):
            return {"__pd_Index__": o.to_list()}
        if isinstance(o, pd.DatetimeIndex):
            return {"__pd_DatetimeIndex__": o.to_list()}
        if isinstance(o, pd.Timestamp):
            return str(o)
        if isinstance(o, pd.DataFrame):
            return {
                "__pd_DataFrame__": o.to_numpy(),
                "columns": o.columns,
                "index": o.index,
            }
        return super().default(o)


def json_pd_obj_hook(dct):
    if isinstance(dct, dict) and "__pd_Index__" in dct:
        return pd.Index(dct["__pd_Index__"])

    if isinstance(dct, dict) and "__pd_DataFrame__" in dct:
        return pd.DataFrame(
            dct["__pd_DataFrame__"], columns=dct["columns"], index=dct["index"]
        )
    if isinstance(dct, dict) and "__pd_DatetimeIndex__" in dct:
        return pd.DatetimeIndex(dct["__pd_DatetimeIndex__"])
    return json_numpy_obj_hook(dct)


def write_arr(path: str, arr: np.ndarray):
    """Write np.ndarray to json file as a dictionnary of shape and data.
    Resulting file can be loaded through load_arr function

    Args:
        path: str, where the array should be written
        arr: np.ndarray, array to be written
    Returns:
        path
    """
    # Force convert to array to allow function to be used
    # for np.ndarray convertibles input
    arr_clean = np.asarray(arr)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(arr_clean, file, cls=NpEncoder)
    return path


def load_arr(path: str) -> np.ndarray:
    """Load array written as json file containing a dictionnary of shape and data.
    Args:
        path: str, where the array is written
    Returns:
        loaded array"""
    with open(path, "r", encoding="utf-8") as file:
        arr_dsc = json.load(file, object_hook=json_numpy_obj_hook)

    return arr_dsc


rw_arr = SaveLoad(save=write_arr, load=load_arr, extension="json")


def write_dl(path: str, obj) -> str:
    with open(path, "wb") as file:
        dl.dump(obj, file)
    return path


def load_dl(path: str):
    with open(path, "rb") as file:
        obj = dl.load(file)
    return obj


rw_dl = SaveLoad(save=write_dl, load=load_dl, extension="dl")


def write_json_like(path: str, obj) -> str:
    with open(path, "w", encoding="UTF-8") as file:
        json.dump(obj, file, cls=PdEncoder)
    return path


def load_json_like(path: str):
    with open(path, "r", encoding="UTF-8") as file:
        obj = json.load(file, object_hook=json_pd_obj_hook)
    return obj


rw_jsonlike = SaveLoad(save=write_json_like, load=load_json_like, extension="json")

# Preparation for future work
base_io = {
    "ARRAY": rw_arr,
    "FLOAT": rw_flt,
    "INT": rw_int,
    "BOOL": rw_bool,
    "STR": rw_str,
    "DILL": rw_dl,
    "JSONLIKE": rw_jsonlike,
}


def safe_load_json(
    path: str,
    buffering: int = -1,
    encoding: str = "utf-8",
    errors: Optional[str] = None,
    newline: Optional[str] = None,
    closefd: bool = True,
    opener=None,
    **kwargs,
) -> dict:
    """Load a json file.
    If loading fails, makes sure the path is printed before raising the exception.
    """
    try:
        with open(
            file=path,
            mode="r",
            buffering=buffering,
            encoding=encoding,
            errors=errors,
            newline=newline,
            closefd=closefd,
            opener=opener,
        ) as file:
            to_return = json.load(file, **kwargs)
        return to_return
    except FileNotFoundError as exc:
        print(f"{path} does not exist")
        raise exc
    except Exception as exc:
        print(f"File at {path} could not be loaded with json")
        raise exc


class ClassAttrIO:
    """Class designed to simplify saving/loading attributes of
    classes defined for data structuration (i.e. where the main
    goal of the class is to organise data).

    Construction:
        name: name at construction time
        save_name: name of file where the attribute is saved
        loader: indicator of SaveLoad object for this attribute IO
        attr_name: name of the attribute (if None, same as name)
        mandatory: if False, attribute can be None (and not saved)
    """

    def __init__(
        self,
        name: str,
        save_name: str,
        loader: str,
        attr_name: Optional[str] = None,
        mandatory: bool = True,
    ):
        self.__name = name
        self.__save_name = save_name
        self.__attr_name = attr_name
        self.__loader = loader
        self.__mandatory = mandatory

    @property
    def name(self) -> str:
        """Name of OptimField"""
        return self.__name

    @property
    def save_name(self) -> str:
        """Name of save file of OptimField"""
        return self.__save_name

    @property
    def attr_name(self) -> str:
        """Attribute name of the field"""
        if self.__attr_name is None:
            return self.name
        return self.__attr_name

    @property
    def loader(self) -> str:
        """Name of loading method"""
        return self.__loader

    @property
    def mandatory(self) -> bool:
        return self.__mandatory

    def to_json(self) -> dict[str, Union[str, bool]]:
        return {
            "name": self.__name,
            "save_name": self.__save_name,
            "attr_name": self.__attr_name,
            "loader": self.__loader,
            "mandatory": self.__mandatory,
        }

    def __repr__(self):
        return self.to_json().__repr__()

    def __str__(self):
        return self.to_json().__str__()

    def save(self, path):
        with open(path, "w", encoding="utf-8") as file:
            json.dump(
                {key: val for key, val in self.to_json().items() if val is not None},
                file,
            )

    def copy(self):
        return ClassAttrIO(
            name=self.__name,
            save_name=self.__save_name,
            loader=self.__loader,
            attr_name=self.__attr_name,
            mandatory=self.__mandatory,
        )


def _clean_dict(dico: dict) -> dict:
    """Removes None values from dictionnary"""
    return {key: val for key, val in dico.items() if val is not None}


class LoadInfo:
    """Loading information of a class, as a list of ClassAttrIO."""

    def __init__(self, extra_fields: list[ClassAttrIO]):
        # One should perform checks on extra_fields passed
        self.__extra_fields = extra_fields

    def save(self, path):
        """Save OptimLoadInfo to yaml file"""
        json_able = [_clean_dict(field.to_json()) for field in self.__extra_fields]
        with open(path, "w", encoding="utf-8") as file:
            json.dump(json_able, file)

    def load_obj(
        self, path, load_methods: dict[str, Callable[[str], Any]]
    ) -> dict[str, Any]:
        """Load a dictionnary of information which can be used
        as argument to initialize a class."""
        dico = {}
        for field in self.__extra_fields:
            try:
                dico[field.name] = load_methods[field.loader](
                    os.path.join(path, field.save_name)
                )

            except Exception as exc:
                if field.mandatory:
                    raise exc
                # Not mandatory field, print exception for now
                print(exc)
        return dico

    def save_obj(
        self,
        obj,
        path: str,
        write_methods: dict[str, Optional[Callable[[str, Any], Any]]],
    ):
        """Save class instance obj using attribute saving information from"""
        for field in self.__extra_fields:

            value = getattr(obj, field.name)
            writer = write_methods[field.loader]
            save_path = os.path.join(path, field.save_name)

            if value is None:
                if field.mandatory:
                    raise ValueError("Missing mandatory field")
            else:
                if writer is None:
                    # This assumes that the object has a save method
                    value.save(save_path)
                else:
                    writer(save_path, value)

    def extend(self, new_fields: list[ClassAttrIO]):
        self.__extra_fields.extend(new_fields)


def load_load_info(path: str) -> LoadInfo:
    """Load an optim load info file"""
    with open(path, "r", encoding="utf-8") as file:
        optim_load_json = json.load(file)

    return LoadInfo([ClassAttrIO(**info) for info in optim_load_json])
