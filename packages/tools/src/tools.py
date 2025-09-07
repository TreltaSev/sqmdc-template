from collections.abc import Callable
import importlib
from importlib.machinery import ModuleSpec
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Optional, Self
from unittest import runner

from click import Context, Group
from utils.console import console


class Tool:
    
    root = Path(__file__).parent
    
    runner: Optional[Group] = None
    module: Optional[ModuleType] = None
    spec: Optional[ModuleSpec] = None
    name: Optional[str] = None
    
    def __init__(self, path: Path) -> None:
        self.load(path)
        self.path = path
        

    
    @classmethod
    def find_all(cls) -> list[Self]:
        """
        Returns a list of all available tools
        """
        out: list[str] = []
        for item in cls.root.rglob("__main__.py"):
            out.append(cls(item))
        return out
    
    def __try_resolve(self, name: str):
        """
        Uses the builtin `importlib` module's `util.resolve_name` method, just a more concise way of using it, if the return value
        of importlib.util.resolve_name results in an error, this method returns `None`
        :arg name: str: Relative Path of package, uses "." as separator
        :arg package: Optional[str]: Module with `__path__` attribute
        :returns: Union[str, None]: Returns either an absolute module name or None: import error
        """
        try:
            return importlib.util.resolve_name(name, None)
        except ImportError as e:
            console.error(f"Import error (name:str): {name} && (package: str | None): {package}, Error: ({e})")
            return None
    
    def load(self, path: Path) -> None:
        """
        Loads a path spec into self
        """
        module_path = ".".join(path.relative_to(self.root).with_suffix("").parts)
        spec: ModuleSpec | None = importlib.util.find_spec(
            self.__try_resolve(module_path)
        )
        
        if spec is None:
            raise FileNotFoundError(f"{module_path} is not a valid spec")

        # Execute Module
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Get main function
        main_runner = getattr(module, "main", None)        
        if main_runner is None:
            raise TypeError(f"Module {spec.name} doesn't have main function")
        
        name = getattr(module, "name", module.__name__.split(".")[0])
        
        self.runner = main_runner
        self.module = module
        self.spec = spec
        self.name = name
           

    def run(self, *args, **kwargs) -> None:
        """
        Runs a specified tool
        
        :param str tool: Name of the tool        
        :raises NotFound: If the tool isn't found
        """
        if not self.runner:
            raise ChildProcessError("No runner for this tool")
        
        return self.runner(args=list(args), standalone_mode=False, prog_name=f"just tool {self.name}", obj=kwargs.get("obj", None))