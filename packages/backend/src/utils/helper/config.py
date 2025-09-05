"""
This module has one simple purpose: Find and Parse given configuration files.
In this file, imports are handled
"""

import re
import yaml

from abc import ABC, abstractmethod
from pathlib import Path

from typing import Any, Callable, Dict, Optional, Union

_SENTINEL = object()


class Primitive(ABC):
    """
    Primitive config loader and parser helper class

    Interfaces
    ----------
    `parse()
    > test
    """

    def __init__(self, path: Optional[str] = None, lazy: bool = False, default: str = ""):
        """
        Before anything, makes sure that the config is fully loaded and ready to go.
        This includes root folders, os env specs etc.


        Properties
        ----------
        file: Optional[Path]
            Path object to the file in question, only accessible if the file exists


        :param str file: Name of the file that will be used        
        :param bool lazy: Whether or not to create the file if it doesn't exist
        :param str default: If lazy is specified, this is what is written to the file to create it
        :raises FileNotFoundError: Whenever no `path` is supplied or the "discovered" file doesn't exist       

        """

        self.file: Optional[Path] = None

        # Make sure a path is given
        if path is None:
            raise FileNotFoundError("No path specified")

        _config_root: Path = Path("/config")
        _config_file: Path = _config_root / path

        while not _config_file.exists():

            if not lazy:
                raise FileNotFoundError(f"Config File Not Found: {_config_file.resolve()}")

            _config_file.write_text("", encoding="utf-8")

            break

        self.file = _config_file

    def read(self, lazy: bool = False, default: str = ""):
        """
        Reads the specified file given to the __init__ function

        :param bool lazy: If this is true, the file is created if it doesn't exist
        :param str default: If lazy is specified and the file is created, this is what will be written into it.

        :raises FileNotFoundError: If no file was handled or the file doesn't exist and lazy isn't specified
        """

        # Checks if the file was even handled
        if self.file is None:
            raise FileNotFoundError("File not loaded, and or doesn't exist")

        while not self.file.exists():

            if not lazy:
                raise FileNotFoundError(f"Config File Not Found: {self.file.resolve()}")

            self.file.write_text(default)

            break

        return self.file.read_text(encoding="utf-8")

    def populate_environment(self, _in: Union[str, Dict, list, tuple]) -> Union[str, Dict, list, tuple]:
        """
        Takes a string, dict, list, or tuple and recursively populates all environment variables
        formatted like {$ENV_VAR}. Will raise KeyError if any are missing.

        :param _in: Input value to process
        :return: Populated version of the input
        :raises KeyError: If a referenced environment variable is not found
        """
        pattern = re.compile(r"\{([A-Za-z0-9_.]+)\}")

        def replacer(match):
            var_name = match.group(1)
            return str(self.get(var_name))

        if isinstance(_in, str):
            return pattern.sub(replacer, _in)

        elif isinstance(_in, dict):
            return {
                self.populate_environment(k): self.populate_environment(v)
                for k, v in _in.items()
            }

        elif isinstance(_in, list):
            return [self.populate_environment(item) for item in _in]

        elif isinstance(_in, tuple):
            return tuple(self.populate_environment(item) for item in _in)

        return _in

    @abstractmethod
    def parse(self, lazy: bool = False, default: Optional[Any] = _SENTINEL) -> dict:
        """
        Parses the given file, returns a dictionary object.

        :param bool lazy: Whether to create the file if it doesn't exist
        :param Optional[Any] default: Object that is returned if parsing fails        
        :returns dict: Dict representation of configuration
        """
        pass

    @staticmethod
    def on_fail(fallback: Callable):
        """
        Runs a specified method on failure of the parent method.

        The error object is passed to the `fallback` method as `error`

        :param Callable fallback: Fallback function that runs whenever the parent function fails
        """

        def wrapper(func: Callable):
            def decorator(*args, **kwargs):
                try:
                    return func(*args, **kwargs)
                except Exception as e:

                    # Inject error to keyword arguments
                    kwargs["error"] = e

                    return fallback(*args, **kwargs)
            return decorator
        return wrapper

    @staticmethod
    def return_default(*args, **kwargs):
        """
        Returns default specified within the keyword arguments as long is default isn't a blank value
        """
        if kwargs.get("default", _SENTINEL) != _SENTINEL:
            return kwargs.get("default")

        raise kwargs.get("error", NotImplementedError("No Error Specified"))

    @on_fail(return_default)
    def get(self, key: str = "", default: Optional[Any] = _SENTINEL) -> Any:
        """
        Gets a value from the parsed file.

        While this function can fail, if a default is specified, 
        whether that be None or an actual value, return the default

        :param str key: Key value of the item, either a regular string or a dot notation string
        :param Optional[Any] default: Default value if the key or key's parent(s) doesn't exist
        """

        if not isinstance(key, str):
            raise TypeError(f"Key is of an incorrect type, expected str, got {type(key)} instead")

        # Get config from parse function
        config: Dict[str, Any] = self.parse()

        if key == "":
            return config

        # Split key on dots
        keys = key.split(".")

        for i, _key in enumerate(keys):

            if _key not in config:
                raise KeyError(f"Key \"{_key}\" not found within object.")

            # Assume _key in config
            value = config[_key]

            if i == len(keys) - 1:
                # Last Key in key string, return no matter what
                return value

            # Not last key, _key in config

            # If its not a dict, kill it here
            if not isinstance(value, dict):
                raise IndexError(f"Not the last key but value is not sub-scriptable. key_string: {key}, failed_on: {_key}")

            # Is a dict, continue
            config = value


class Yaml(Primitive):
    """Yaml Config Loader

    Attempts to locate and parse a .yaml file
    """

    def __init__(self, path: str = "config.yml"):
        super().__init__(path)

    def parse(self, lazy: bool = False, default: Optional[Any] = _SENTINEL) -> dict:
        contents: str = self.read(lazy, "")
        return yaml.load(contents, Loader=yaml.FullLoader)
