# === Core ===
from fastapi import FastAPI, APIRouter

from pathlib import Path

import importlib.util


# === Utils ===
from utils.console import console
from utils.helper.config import Yaml

# === Typing ===
from typing import Any, Dict, List, Union
from importlib.machinery import ModuleSpec


class App(FastAPI):

    def __init__(self, file_path, *args, **kwargs):
        # Path Objects
        self.main: Path = Path(file_path)
        self.root = self.main.parent

        # Routers
        self.routers: Dict[str, Any] = {}

        super().__init__(*args, **kwargs)

    def __try_resolve(self, name: str, package: str | None = None) -> str | None:
        """
        Uses the builtin `importlib` module's `util.resolve_name` method, just a more concise way of using it, if the return value
        of importlib.util.resolve_name results in an error, this method returns `None`
        :arg name: str: Relative Path of package, uses "." as separator
        :arg package: Optional[str]: Module with `__path__` attribute
        :returns: Union[str, None]: Returns either an absolute module name or None: import error
        """
        try:
            return importlib.util.resolve_name(name, package)
        except ImportError as e:
            console.error(f"Import error (name:str): {name} && (package: str | None): {package}, Error: ({e})")
            return None

    def __load(self, spec: Union[str, ModuleSpec]) -> None:
        """
        Imports and attempts to load a router variable in each spec if it exists

        :param Union[str, ModuleSpec] spec: Spec string or object
        """

        if isinstance(spec, str):
            spec: ModuleSpec | None = importlib.util.find_spec(
                self.__try_resolve(spec, package=None)
            )

        if spec is None:
            return None

        # Find and execute module
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)

        external_router: Any = getattr(mod, "router", None)

        if external_router is None:
            console.warn(f"No router variable found in [orange1 underline]{spec.name.replace('.', '/')}.py[/]")
            return None

        if not isinstance(external_router, APIRouter):
            console.warn(f"Provided router variable isn't of type APIRouter in [orange1 underline]{spec.name.replace('.', '/')}.py[/]")
            return None

        self.include_router(external_router)
        
        for route in external_router.routes:
            console.info(f"Registered Route: [orange1]{route.path} [{', '.join(route.methods)}][/]")

    def register_routers(self) -> None:
        """
        Actively finds and registers all routers lazily
        """
        for possible_router in self.__get_routers():
            self.__load(possible_router)

    def __get_routers(self) -> List[Any]:
        out_specs = []

        api_route = self.root / "api"

        files = api_route.rglob("*.py")

        for file in files:

            # Skip files that start with _
            if file.name.startswith("_"):
                continue

            # Skip files in directories or files starting with _
            if any(part.startswith("_") for part in file.parts):
                continue

            module_path = ".".join(file.relative_to(self.root).with_suffix("").parts)
            out_specs.append(module_path)

        return out_specs

    @property
    def config(self) -> dict:
        yml = Yaml()
        return yml.populate_environment(yml.get("backend.uvicorn_config"))
