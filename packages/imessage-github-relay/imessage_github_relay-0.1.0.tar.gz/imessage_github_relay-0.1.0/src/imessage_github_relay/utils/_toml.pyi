from os.path import expanduser, expandvars, join
from os import getcwd as cwd
from typing import Any, Dict
from colorama import Fore as cf
import toml
import sys

class _Toml:
    """`TOML FILE handler class.`
    
    Internal Class of `iMessage GitHub Relay`.
    """
    def __init__(self, file: str) -> None:
        """`Create a _Toml object from a given TOML file.`
        
        #### Parameters
        - **`file`**: A file path (can be relative and contain VARS) leading up to the TOML file to read.

        #### Usage

        ```python
        >>> from imessage_github_relay.utils._toml import _TOML
        >>> toml_obj = _TOML('./pyproject.toml')
        ```
        """
        ...
    
    def __enter__(self) -> '_Toml':
        """`Context Entry`"""
        ...
    
    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """`Context Exit`"""
        ...
    
    def _load(self) -> Dict[str, Any]:
        """`Loads the TOML file`"""
        ...
    
    def get(self, key: str, default: Any = None) -> Any:
        """`Tries to find the value of the key in the loaded TOML data.`
        
        Returns `default` if `key` not present in the TOML data.
        """
        ...