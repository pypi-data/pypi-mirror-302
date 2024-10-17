from os.path import expanduser, expandvars, join
from os import getcwd as cwd
from typing import Any, Dict
from colorama import Fore as cf
import toml
import sys

class _Toml:
    def __init__(self, file: str) -> None:
        self.toml_file_location = file

        # normalize the path
        if self.toml_file_location.startswith('./'):
            self.toml_file_location = join(cwd(), self.toml_file_location[2:])
        
        # expand if anything
        self.toml_file_location = expanduser(expandvars(self.toml_file_location))
    
    def __enter__(self):
        self.TOML = self._load()
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.TOML = None
    
    def _load(self) -> Dict[str, Any]:
        try:
            with open(self.toml_file_location, 'r+') as file:
                return toml.load(file)
        except Exception as e:
            print(f"{cf.RED}Error{cf.RESET}: Failed to read TOML file: {e}")
            sys.exit(1)
        
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split('.')
        value = self.TOML

        try:
            for k in keys:
                value = value[k]
        except KeyError:
            return default
        
        return value